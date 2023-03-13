#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Main project: https://github.com/cloudedbats
# Copyright (c) 2023-present Arnold Andreasson
# License: MIT License (see LICENSE or http://opensource.org/licenses/mit).

import asyncio
import logging
import pathf_core


async def main():
    """ """
    logging_dir = "../pathfinder_logging"
    settings_dir = "../pathfinder_settings"

    # Pathfinder logger.
    pathf_core.logger.setup_rotating_log(
        logging_dir=logging_dir,
        log_name="info_log.txt",
        debug_log_name="debug_log.txt",
    )
    logger = logging.getLogger("Pathfinder")
    logger.info("\n\n")
    logger.info("Welcome to Cloudedbats - Pathfinder")
    logger.info("https://github.com/cloudedbats/cloudedbats_pathfinder")
    logger.info("======================== ^ö^ ========================")
    logger.info("")

    # Pathfinder configuration.
    pathf_core.config.load_config(
        config_dir=settings_dir,
        config_file="pathfinder_config.yaml",
        config_default_dir="",
        config_default_file="pathfinder_config_default.yaml",
    )

    # Pathfinder startup.
    logger.debug("Pathfinder startup.")
    await pathf_core.pathf_main.main()

    # # Pathfinder shutdown.
    # # Get a list of all running tasks.
    # running_tasks = asyncio.all_tasks()
    # # Remove current task.
    # current_task = asyncio.current_task()
    # running_tasks.remove(current_task)
    # # Cancel all remaining tasks.
    # logger.debug("Pathfinder shutdown. Number of tasks: " + str(len(running_tasks)))
    # for task in running_tasks:
    #     task_name = task.get_name()
    #     logger.debug("- Cancel task: " + task_name)
    #     task.cancel()


if __name__ == "__main__":
    """ """
    asyncio.run(main())
