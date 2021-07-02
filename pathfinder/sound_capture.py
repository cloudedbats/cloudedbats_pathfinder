#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2021-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy
import alsaaudio


class SoundCapture:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.config = None
        self.out_queue_list = []
        self.card_index = None
        self.sampling_freq_hz = None
        self.channels = None
        self.buffer_size = None
        self.main_loop = None
        self.capture_executor = None
        self.logger = logging.getLogger(logger)

    def setup(self, config, card_index):
        """ """
        self.config = config
        self.card_index = card_index
        # List of out data queues.
        self.out_queue_list = []
        # Setup for sound capture.
        self.sampling_freq_hz = self.config.get("sampling_freq_hz", "192000")
        self.channels = self.config.get("channels", "2")
        self.buffer_size = int(self.config.get("buffer_size", "4096"))

    def add_out_queue(self, out_queue):
        """ """
        self.out_queue_list.append(out_queue)

    async def start(self):
        """ """
        # Use executor for the IO-blocking part.
        self.main_loop = asyncio.get_event_loop()
        self.capture_executor = self.main_loop.run_in_executor(None, self.run_capture)

    async def stop(self):
        """ """
        self.capture_active = False
        if self.capture_executor:
            self.capture_executor.cancel()
            self.capture_executor = None

    def run_capture(self):
        """ """
        pmc_capture = None
        self.capture_active = True
        try:
            pmc_capture = alsaaudio.PCM(
                alsaaudio.PCM_CAPTURE,
                alsaaudio.PCM_NORMAL,
                # alsaaudio.PCM_NONBLOCK,
                channels=int(self.channels),
                rate=int(self.sampling_freq_hz),
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=int(self.buffer_size),
                device="sysdefault",
                cardindex=int(self.card_index),
            )
            # Empty numpy buffer.
            in_buffer_int16 = numpy.array([], dtype=numpy.int16)
            while self.capture_active:
                # Read from capture device.
                length, data = pmc_capture.read()
                if length < 0:
                    self.logger.debug("Sound capture overrun: " + str(length))
                elif len(data) > 0:
                    # Convert from string-byte array to int16 array.
                    in_data_int16 = numpy.frombuffer(data, dtype=numpy.int16)

                    # # Temporary solution for stereo sound cards that can't
                    # # run in mono mode (or maybe related to a bug in alsaaudio).
                    # # Extract one channel if the data array is doubled in size.
                    # if (length * 2) == in_data_int16.size:
                    #     in_data_int16 = in_data_int16[1::2].copy()

                    # Concatenate
                    in_buffer_int16 = numpy.concatenate(
                        (in_buffer_int16, in_data_int16)
                    )
                    while len(in_buffer_int16) >= self.buffer_size:
                        # Copy "buffer_size" part and save remaining part.
                        data_int16 = in_buffer_int16[0 : self.buffer_size]
                        in_buffer_int16 = in_buffer_int16[self.buffer_size :]

                        # Put data on queues in the queue list.
                        for data_queue in self.out_queue_list:
                            # Copy data.
                            data_int16_copy = data_int16.copy()
                            # Put together.
                            data_dict = {
                                "status": "data",
                                "data": data_int16_copy,
                            }
                            try:
                                if not data_queue.full():
                                    self.main_loop.call_soon_threadsafe(
                                        data_queue.put_nowait, data_dict
                                    )
                            #
                            except Exception as e:
                                # Logging error.
                                message = "Failed to put data on queue: " + str(e)
                                self.logger.error(message)
                                if not self.main_loop.is_running():
                                    # Terminate.
                                    self.capture_active = False
                                    break
        #
        except Exception as e:
            self.logger.error("EXCEPTION Sound capture: " + str(e))
        finally:
            self.capture_active = False
            if pmc_capture:
                pmc_capture.close()
            self.logger.debug("Sound capture ended.")
