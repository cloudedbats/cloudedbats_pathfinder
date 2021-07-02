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
        self.pathf_config = {}

    def load_config(self, config_file):
        """ """
        config_path = pathlib.Path(config_file)
        with open(config_path) as file:
            self.pathf_config = yaml.load(file, Loader=yaml.FullLoader)

    def get_sound_capture(self):
        """ """
        return self.pathf_config.get("sound_capture", {})

    def get_sound_playback(self):
        """ """
        return self.pathf_config.get("sound_playback", {})

    def get_pitchshifting(self):
        """ """
        return self.pathf_config.get("sound_pitchshifting", {})
