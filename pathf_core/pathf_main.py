#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Main project: https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging

import pathf_core


class PathfinderMain:
    """ """

    def __init__(self, logger="DefaultLogger") -> None:
        """ """
        self.gather_result = None
        self.logger_name = logger
        self.logger = logging.getLogger(logger)

    async def main(self):
        """ """
        config = pathf_core.config
        # Log sound capture devices.
        capture_info = pathf_core.capture.get_capture_devices("")
        self.logger.info("Sound capture devices: ")
        for info in capture_info:
            self.logger.info(" - " + info.get("name", ""))
        # Select sound capture device.
        part_of_device_name = config.get("sound_capture.device_name")
        capture_info = pathf_core.capture.get_capture_devices(part_of_device_name)
        self.logger.info("Selected capture devices: ")
        capture_card_index = None
        try:
            capture_card_index = capture_info[0]["index"]
            self.logger.info(" - " + capture_info[0].get("name", ""))
        except:
            self.logger.info(" - FAILED.")
        # Log sound playback devices.
        playback_info = pathf_core.playback.get_playback_devices("")
        self.logger.info("Sound playback devices: ")
        for info in playback_info:
            self.logger.info(" - " + info.get("name", ""))
        # Select sound playback device.
        part_of_device_name = config.get("sound_playback.device_name")
        playback_info = pathf_core.playback.get_playback_devices(part_of_device_name)
        self.logger.info("Selected playback devices: ")
        playback_card_index = None
        try:
            self.logger.info(" - " + playback_info[0].get("name", ""))
            playback_card_index = playback_info[0]["index"]
        except:
            self.logger.info(" - FAILED.")

        if (capture_card_index != None) and (playback_card_index != None):
            # Setup.
            pathf_core.capture.setup(
                capture_card_index,
                channels=config.get("sound_capture.channels"),
                sampling_freq_hz=config.get("sound_capture.sampling_freq_hz"),
                frames=config.get("sound_capture.frames"),
                buffer_size=config.get("sound_capture.buffer_size"),
            )
            pathf_core.pitchshifting.setup(
                channels=config.get("sound_pitchshifting.channels"),
                sampling_freq_in=config.get("sound_capture.sampling_freq_hz"),
                sampling_freq_out=config.get("sound_playback.sampling_freq_hz"),
                pitch_factor=config.get("sound_pitchshifting.pitch_factor"),
                volume_percent=config.get("sound_pitchshifting.volume_percent"),
                filter_low_khz=config.get("sound_pitchshifting.filter_low_khz"),
                filter_high_khz=config.get("sound_pitchshifting.filter_high_khz"),
                overlap_factor=config.get("sound_pitchshifting.overlap_factor"),
                in_queue_length=config.get("sound_pitchshifting.in_queue_length"),
            )
            pathf_core.playback.setup(
                playback_card_index,
                channels=config.get("sound_playback.channels"),
                sampling_freq_hz=config.get("sound_playback.sampling_freq_hz"),
                frames=config.get("sound_playback.frames"),
                buffer_size=config.get("sound_playback.buffer_size"),
                buffer_max_size=config.get("sound_playback.buffer_max_size"),
                in_queue_length=config.get("sound_playback.in_queue_length"),
            )

            # Connect via queues.
            # Sound capture -> queue -> pitch shifting -> queue -> sound playback.
            pitch_queue = pathf_core.pitchshifting.get_queue()
            playback_queue = pathf_core.playback.get_queue()
            pathf_core.capture.add_out_queue(pitch_queue)
            pathf_core.pitchshifting.add_out_queue(playback_queue)

            # Get coroutines.
            pitchshifting_coro = pathf_core.pitchshifting.start()
            playback_coro = pathf_core.playback.start()
            capture_coro = pathf_core.capture.start()
            try:
                # # Run it all in three parallel tasks.
                tasks = asyncio.gather(
                    capture_coro,
                    pitchshifting_coro,
                    playback_coro,
                )
                self.gather_result = await tasks
                print("Pathfinder ended: ", self.gather_result)
            except Exception as e:
                print("Exception, pathfinder terminated: " + str(e))

            pathf_core.audio.terminate()
        else:
            if capture_card_index == None:
                self.logger.error("Can't find sound card for sound capture.")
            if playback_card_index == None:
                self.logger.error("Can't find sound cards for playback.")

        print("Pathfinder ended. ")
