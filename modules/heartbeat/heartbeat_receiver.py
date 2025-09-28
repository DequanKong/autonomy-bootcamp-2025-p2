"""
Heartbeat receiving logic.
"""
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
    def create(cls,connection: mavutil.mavfile,local_logger: logger):
        """
        Falliable create (instantiation) method to create a HeartbeatReceiver object.
        """
        # Create a HeartbeatReceiver object
        return True, HeartbeatReceiver(cls.__private_key, connection, local_logger)

    def __init__(self,key: object,connection: mavutil.mavfile,local_logger: logger.Logger):
        assert key is HeartbeatReceiver.__private_key, "Use create() method"

        # Initialization
        self.connection = connection
        self._log = local_logger
        
        self._log.info("HeartbeatReceiver initialized")
        
    def run_hb_receiver(self):
        msg = self.connection.recv_match(
            type="HEARTBEAT"
        )
        if msg is None:
            return False
        return True
    