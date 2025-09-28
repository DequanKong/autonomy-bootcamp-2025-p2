"""
Heartbeat receiving logic.
"""
from typing import Tuple, Union
from pymavlink import mavutil
from modules.common.modules.logger import logger


HEARTBEAT_PERIOD = 1.0


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class HeartbeatReceiver:
    """
    HeartbeatReceiver class to receive a heartbeat
    """

    __private_key = object()

    @classmethod
    def create(cls, connection: mavutil.mavfile, local_logger: logger) -> Tuple[bool, Union["HeartbeatReceiver", None]]:
        """
        Falliable create (instantiation) method to create a HeartbeatReceiver object.
        """
        # Create a HeartbeatReceiver object
        return True, HeartbeatReceiver(cls.__private_key, connection, local_logger)

    def __init__(self, key: object, connection: mavutil.mavfile, local_logger: logger.Logger) -> None:
        assert key is HeartbeatReceiver.__private_key, "Use create() method"

        # Initialization
        self.connection = connection
        self.__log = local_logger

        self.__log.info("HeartbeatReceiver initialized")

    def run_hb_receiver(self) -> bool:
        """
        Checks if the heartbeat received is a heartbeat message
        """
        msg = self.connection.recv_match(type="HEARTBEAT")
        if msg is None:
            return False
        return True
