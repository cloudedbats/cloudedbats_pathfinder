#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2021-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import asyncio
import logging

import pathfinder


async def main():
    """ """
    # Set up logging and print welcome message.
    log_dir_path = "../pathfinder_logging"
    log_name = "pathfinder_log.txt"
    debug_log_name = "pathfinder_debug_log.txt"
    pathfinder.logger.setup_rotating_log(
        log_dir_path=log_dir_path, log_name=log_name, debug_log_name=debug_log_name
    )
    pathfinder.logger.welcome_message()

    # Load config.
    pathfinder.config.load_config("pathfinder_config.yaml")
    capture_config = pathfinder.config.get_sound_capture()
    playback_config = pathfinder.config.get_sound_playback()
    pitchshifting_config = pathfinder.config.get_pitchshifting()

    # Scan for sound cards.
    cards = pathfinder.sound_cards
    cards.update_card_lists()
    # Sound capture card.
    device_name = capture_config.get("device_name", "")
    capture_card_index = cards.get_capture_card_index_by_name(device_name)
    # Sound playback card.
    device_name = playback_config.get("device_name", "")
    playback_card_index = cards.get_capture_card_index_by_name(device_name)

    # Setup.
    pathfinder.sound_capture.setup(capture_config, capture_card_index)
    pathfinder.sound_pitchshifting.setup(pitchshifting_config)
    pathfinder.sound_pitchshifting.calc_params()
    pathfinder.sound_playback.setup(playback_config, playback_card_index)

    # Connect via queues.
    # Sound capture -> queue -> pitch shifting -> queue -> sound playback.
    pitch_queue = pathfinder.sound_pitchshifting.get_queue()
    playback_queue = pathfinder.sound_playback.get_queue()
    pathfinder.sound_capture.add_out_queue(pitch_queue)
    pathfinder.sound_pitchshifting.add_out_queue(playback_queue)
    # Get coroutines.
    sound_pitchshifting_coro = pathfinder.sound_pitchshifting.start()
    sound_playback_coro = pathfinder.sound_playback.start()
    sound_capture_coro = pathfinder.sound_capture.start()

    try:
        # Run it all in three parallell tasks.
        tasks = asyncio.gather(
            sound_capture_coro,
            sound_pitchshifting_coro,
            sound_playback_coro,
        )
        gather_result = await tasks
        print("Pathfinder ended: ", gather_result)
    except Exception as e:
        print("Exception, pathfinder terminated: " + str(e))
        # logger.warning("Exception, pathfinder terminated: " + str(e))
    # Stop pending tasks.
    await pathfinder.sound_capture.stop()
    await pathfinder.sound_pitchshifting.stop()
    await pathfinder.sound_playback.stop()
    print("Pathfinder ended.")
