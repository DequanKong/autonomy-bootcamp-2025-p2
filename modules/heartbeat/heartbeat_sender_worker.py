"""
Heartbeat worker that sends heartbeats periodically.
"""

import os
import pathlib
import time

from pymavlink import mavutil

from utilities.workers import worker_controller
from utilities.workers import queue_proxy_wrapper
from modules.heartbeat import heartbeat_sender
from modules.common.modules.logger import logger


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
def heartbeat_sender_worker(
    connection: mavutil.mavfile,
    controller: worker_controller.WorkerController,
    # Add other necessary worker arguments here
) -> None:
    """
    Worker process.

    args... describe what the arguments are
    """
    # =============================================================================================
    #                          ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
    # =============================================================================================

    # Instantiate logger
    worker_name = pathlib.Path(__file__).stem
    process_id = os.getpid()
    result, local_logger = logger.Logger.create(f"{worker_name}_{process_id}", True)
    if not result:
        print("ERROR: Worker failed to create logger")
        return

    # Get Pylance to stop complaining
    assert local_logger is not None

    local_logger.info("Logger initialized", True)

    # =============================================================================================
    #                          ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
    # =============================================================================================

    # Instantiate class object (heartbeat_sender.HeartbeatSender)
    check, hb_sender_instance = heartbeat_sender.HeartbeatSender.create(connection, local_logger)
    if not check:
        local_logger.error("Failed to create HeartbeatSender (invalid connection or logger).")
        return

    local_logger.info("HeartbeatSender worker started.")

    HEARTBEAT_PERIOD = 1.0  # interval in seconds between heartbeats

    # Main loop: do work.
    while not controller.is_exit_requested():
        controller.check_pause()
        sent = hb_sender_instance.run_hb_sender()
        if not sent:
            local_logger.error("Failed to send heartbeat.")

        # wait until next heartbeat
        time.sleep(HEARTBEAT_PERIOD)
    local_logger.info("HeartbeatSender worker stopped.")


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
