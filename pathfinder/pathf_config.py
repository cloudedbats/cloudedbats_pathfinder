#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2021-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import yaml
import logging


class PathfinderConfig:
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger = logging.getLogger(logger)
        self.clear()

    def clear(self):
        """ """
        self.config = {}

    def load_config(self, config_file):
        """ """
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)

    def get_capture_config(self):
        """ """
        config = {}
        value = self.get_value("sound_capture.device_name")
        config["device_name"] = value
        value = self.get_value("sound_capture.sampling_freq_hz")
        config["sampling_freq_hz"] = value
        value = self.get_value("sound_capture.channels").upper()
        config["channels"] = value
        value = self.get_value("sound_capture.buffer_size")
        config["buffer_size"] = value
        value = self.get_value("sound_capture.period_size")
        config["period_size"] = value
        #
        return config

    def get_pitchshifting_config(self):
        """ """
        config = {}
        value = self.get_value("sound_pitchshifting.pitch_factor")
        config["pitch_factor"] = value
        value = self.get_value("sound_pitchshifting.volume_percent")
        config["volume_percent"] = value
        value = self.get_value("sound_pitchshifting.filter_low_khz")
        config["filter_low_khz"] = value
        value = self.get_value("sound_pitchshifting.filter_high_khz")
        config["filter_high_khz"] = value
        value = self.get_value("sound_capture.sampling_freq_hz")
        config["sampling_freq_in_hz"] = value
        value = self.get_value("sound_playback.sampling_freq_hz")
        config["sampling_freq_out_hz"] = value
        value = self.get_value("sound_capture.channels").upper()
        config["channels"] = value
        value = self.get_value("sound_pitchshifting.in_queue_length")
        config["in_queue_length"] = value
        value = self.get_value("sound_pitchshifting.overlap_factor")
        config["overlap_factor"] = value
        #
        return config

    def get_playback_config(self):
        """ """
        config = {}
        value = self.get_value("sound_playback.device_name")
        config["device_name"] = value
        value = self.get_value("sound_playback.sampling_freq_hz")
        config["sampling_freq_hz"] = value
        value = self.get_value("sound_capture.channels").upper()
        config["channels"] = value
        value = self.get_value("sound_playback.buffer_size")
        config["buffer_size"] = value
        value = self.get_value("sound_playback.period_size")
        config["period_size"] = value
        value = self.get_value("sound_playback.buffer_max_size")
        config["buffer_max_size"] = value
        value = self.get_value("sound_playback.in_queue_length")
        config["in_queue_length"] = value
        #
        return config

    def get_value(self, key_path):
        """ """
        key_parts = key_path.split(".")
        if len(key_parts) >= 2:
            group_name = key_parts[0]
            default_name = group_name + "_default"
            key = key_parts[1]
            # Get default.
            default_dict = self.config.get(default_name, {})
            default_value = default_dict.get(key, "")
            # Get value.
            group_dict = self.config.get(group_name, {})
            if group_dict:
                value = group_dict.get(key, default_value)
            else:
                value = default_value
            # Return.
            return value
        else:
            return ""
