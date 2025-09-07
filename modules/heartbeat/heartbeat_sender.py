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
    def create(
        cls,
        connection: mavutil.mavfile,
        args,  # Put your own arguments here
    ) -> "tuple[True, HeartbeatSender] | tuple[False, None]":
        """
        Falliable create (instantiation) method to create a HeartbeatSender object.
        """
        pass  # Create a HeartbeatSender object

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        args,  # Put your own arguments here
    ):
        assert key is HeartbeatSender.__private_key, "Use create() method"

        # Do any intializiation here

    def run(
        self,
        args,  # Put your own arguments here
    ):
        """
        Attempt to send a heartbeat message.
        """
        self.connection.mav.heartbeat_send(
            type=mavutil.mavlink.MAV_TYPE_GENERIC,
            autopilot=mavutil.mavlink.MAV_AUTOPILOT_GENERIC,
            base_mode=0,
            custom_mode=0,
            system_status=mavutil.mavlink.MAV_STATE_ACTIVE
        )
        pass  # Send a heartbeat message


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
