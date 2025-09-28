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
    def create(
        cls, connection: mavutil.mavfile, local_logger: logger
    ) -> Tuple[bool, Union["HeartbeatReceiver", None]]:
        """
        Falliable create (instantiation) method to create a HeartbeatReceiver object.
        """
        # Create a HeartbeatReceiver object
        return True, HeartbeatReceiver(cls.__private_key, connection, local_logger)

    def __init__(
        self, key: object, connection: mavutil.mavfile, local_logger: logger.Logger
    ) -> None:
        assert key is HeartbeatReceiver.__private_key, "Use create() method"

        # Initialization
        self.connection = connection
        self.__log = local_logger

        self.__log.info("HeartbeatReceiver initialized")
        self.missed = 0
        self.state = "DISCONNECTED"

    def run_hb_receiver(self) -> str:
        """
        Checks if the heartbeat received is a heartbeat message
        """
        msg = self.connection.recv_match(type="HEARTBEAT")
        if not msg:
            self.missed += 1
            self.__log.warning("Missed heartbeat! " + str(self.missed) + " in a row.")
            if self.missed >= 5:
                self.state = "DISCONNECTED"
        else:
            self.missed = 0
            self.state = "CONNECTED"
        self.__log.info("STATUS: " + self.state)
        return self.state
