"""
Heartbeat sending logic.
"""

from pymavlink import mavutil

# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class HeartbeatSender:
    """
    HeartbeatSender class to send a heartbeat
    """

    __private_key = object()

    @classmethod
    def create(cls,connection: mavutil.mavfile,local_logger) -> "tuple[True, HeartbeatSender] | tuple[False, None]":
        """
        Falliable create (instantiation) method to create a HeartbeatSender object.
        """
        if connection is None or local_logger is None:
            return False, None
        return True, HeartbeatSender(cls.__private_key, connection, local_logger)
        
    def __init__(self, key: object,connection: mavutil.mavfile,local_logger):
        assert key is HeartbeatSender.__private_key, "Use create() method"

        self.connection = connection
        self._log = local_logger
        self._log.debug("HeartbeatSender initialized with connection %s", connection)
        
    def run_hb_sender(self):
        """
        Attempt to send a heartbeat message.
        """
        try:
            self._log.debug("Sending HEARTBEAT...")
            self.connection.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,           
                mavutil.mavlink.MAV_AUTOPILOT_INVALID,  
                0,                                      
                0,                                     
                mavutil.mavlink.MAV_STATE_ACTIVE       
            )
            return True
        except Exception as e:
            self._log.error("Failed to send HEARTBEAT: %s", e)
            return False


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================