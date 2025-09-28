"""
Heartbeat worker that receives heartbeats periodically.
"""

import os
import pathlib
import time
from pymavlink import mavutil

from utilities.workers import queue_proxy_wrapper
from utilities.workers import worker_controller
from modules.heartbeat import heartbeat_receiver
from ..common.modules.logger import logger

# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================


def heartbeat_receiver_worker(
    connection: mavutil.mavfile,
    heartbeat_time: float,
    output_queue: queue_proxy_wrapper.QueueProxyWrapper,
    controller: worker_controller.WorkerController,
) -> None:
    """
    Worker process.

    connection: connection instance
    heartbeat_time: interval in which worker tries to receive heartbeats
    output_queue: output to the main process
    controller: how the main process communicates to this worker process.
    main_logger: Logger of output_queue
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
    # Instantiate class object (heartbeat_receiver.HeartbeatReceiver)
    check, hb_receiver_instance = heartbeat_receiver.HeartbeatReceiver.create(
        connection, local_logger
    )
    if not check:
        local_logger.error("Failed to create Heartbeat Receiver (invalid connection or logger).")
        return

    status = "DISCONNECTED"
    # Worker starts
    local_logger.info("HeartbeatReceiver worker started.")
    # Do work in infinite loop
    while not controller.is_exit_requested():
        controller.check_pause()
        status = hb_receiver_instance.run_hb_receiver()
        if status:
            output_queue.queue.put(f"{status} at {time.strftime('%H:%M:%S')}")
        time.sleep(heartbeat_time)
    local_logger.info("HeartbeatReceiver worker stopped.")
