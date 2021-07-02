#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2021-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging
import numpy
import alsaaudio


class SoundPlayback:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.config = None
        self.queue = None
        self.card_index = None
        self.sampling_freq_hz = None
        self.channels = None
        self.buffer_size = None
        self.playback_active = False
        self.playback_queue_active = False
        self.playback_executor = None
        self.buffer_int16 = None
        self.logger = logging.getLogger(logger)

    def setup(self, config, card_index):
        """ """
        self.config = config
        self.card_index = card_index
        # Setup queue for data in.
        queue_maxsize = int(self.config.get("queue_maxsize", "100"))
        self.queue = asyncio.Queue(maxsize=queue_maxsize)
        # Setup for sound playback.
        self.sampling_freq_hz = self.config.get("sampling_freq_hz", "48000")
        self.channels = self.config.get("channels", "2")
        self.buffer_size = int(self.config.get("buffer_size", "4096"))

    def get_queue(self):
        """ """
        return self.queue

    async def start(self):
        """ """
        # Use executor for the IO-blocking part.
        main_loop = asyncio.get_event_loop()
        self.playback_executor = main_loop.run_in_executor(None, self.run_playback)
        await asyncio.sleep(0.1)
        # Clear queue.
        while not self.queue.empty():
            self.queue.get_nowait()
            self.queue.task_done()
        # Copy data from queue to buffer.
        self.playback_queue_active = True
        while self.playback_queue_active:
            try:
                data_dict = await self.queue.get()
                if "data" in data_dict:
                    self.add_data(data_dict["data"])
            except asyncio.CancelledError:
                break
            except Exception as e:
                # Logging error.
                message = "SoundPlayback, failed to read data queue: " + str(e)
                self.logger.debug(message)

    async def stop(self):
        """ """
        self.playback_active = False
        self.playback_queue_active = False
        if self.playback_executor:
            self.playback_executor.cancel()
            self.playback_executor = None

    def add_data(self, data):
        """ """
        # self.logger.debug("DEBUG DATA ADDED. Length: ", len(data))
        if self.buffer_int16 is None:
            self.buffer_int16 = numpy.array([], dtype=numpy.int16)
        self.buffer_int16 = numpy.concatenate((self.buffer_int16, data))

    def run_playback(self):
        """ """
        pmc_play = None
        self.playback_active = True
        try:
            # Setup ALSA for playback.
            pmc_play = alsaaudio.PCM(
                alsaaudio.PCM_PLAYBACK,
                alsaaudio.PCM_NORMAL,
                channels=int(self.channels),
                rate=int(self.sampling_freq_hz),
                format=alsaaudio.PCM_FORMAT_S16_LE,
                periodsize=int(self.buffer_size),
                device="sysdefault",
                cardindex=int(self.card_index),
            )
            # To be used when no data in buffer.
            silent_buffer = numpy.zeros((self.buffer_size, 1), dtype=numpy.float16)
            # Loop over the IO blocking part.
            while self.playback_active:
                try:
                    # Use silent buffer as default.
                    buffer_int16 = silent_buffer
                    #
                    if (self.buffer_int16 is not None) and (
                        self.buffer_int16.size > self.buffer_size
                    ):
                        # Copy part to be used.
                        buffer_int16 = self.buffer_int16[: self.buffer_size]
                        # Remove used part.
                        self.buffer_int16 = self.buffer_int16[self.buffer_size :]
                    # else:
                    #     self.logger.debug("SILENCE")
                    # Convert to byte buffer and write.
                    buffer_bytes = buffer_int16.tobytes()
                    pmc_play.write(buffer_bytes)

                except asyncio.CancelledError:
                    break
                except Exception as e:
                    self.logger.error("EXCEPTION PLAYBACK-1: " + str(e))
        #
        except asyncio.CancelledError:
            pass
        except Exception as e:
            self.logger.error("EXCEPTION PLAYBACK-2: " + str(e))
        finally:
            self.playback_active = False
            if pmc_play:
                pmc_play.close()
            self.logger.debug("PLAYBACK ENDED.")
