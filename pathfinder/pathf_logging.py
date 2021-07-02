#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org, https://github.com/cloudedbats
# Copyright (c) 2021-present Arnold Andreasson
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import pathlib
import sys
import logging
from logging import handlers


class PathfinderLogger(object):
    """ """

    def __init__(self, logger="DefaultLogger"):
        """ """
        self.logger_name = logger
        self.logger = logging.getLogger(logger)

    def setup_rotating_log(
        self,
        log_dir_path="",
        log_name="info_log.txt",
        debug_log_name="debug_log.txt",
    ):
        """ """
        try:
            # Create directory for log files.
            logging_dir_path = pathlib.Path(log_dir_path)
            if not logging_dir_path.exists():
                logging_dir_path.mkdir(parents=True)
            # Info and debug logging.
            pathf_logger_info = logging.getLogger(self.logger_name)
            pathf_logger_info.setLevel(logging.INFO)
            pathf_logger_debug = logging.getLogger(self.logger_name)
            pathf_logger_debug.setLevel(logging.DEBUG)
            pathf_logger_stdio = logging.getLogger(self.logger_name)
            pathf_logger_stdio.setLevel(logging.DEBUG)

            # Define rotation log files for info logger.
            log_info_name_path = pathlib.Path(log_dir_path, log_name)
            log_handler = handlers.RotatingFileHandler(
                str(log_info_name_path), maxBytes=128 * 1024, backupCount=10
            )
            log_handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)-8s : %(message)s ")
            )
            log_handler.setLevel(logging.INFO)
            pathf_logger_info.addHandler(log_handler)

            # Define rotation log files for debug logger.
            log_info_name_path = pathlib.Path(log_dir_path, debug_log_name)
            log_handler = handlers.RotatingFileHandler(
                str(log_info_name_path), maxBytes=128 * 1024, backupCount=10
            )
            log_handler.setFormatter(
                logging.Formatter("%(asctime)s %(levelname)-8s : %(message)s ")
            )
            log_handler.setLevel(logging.DEBUG)
            pathf_logger_debug.addHandler(log_handler)

            # Define stdout logging.
            log_handler = logging.StreamHandler(sys.stdout)
            log_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(levelname)s : %(message)s")
            log_handler.setFormatter(formatter)
            pathf_logger_stdio.addHandler(log_handler)

        except Exception as e:
            print("Logging: Failed to setup logging: " + str(e))

    def welcome_message(self):
        """ """
        self.logger.info("")
        self.logger.info("")
        self.logger.info("Welcome to CloudedBats - Pathfinder")
        self.logger.info("Main project page: http://cloudedbats.org")
        self.logger.info("Source code: https://github.com/cloudedbats")
        self.logger.info("================== ^ö^ ====================")
        self.logger.info("")
