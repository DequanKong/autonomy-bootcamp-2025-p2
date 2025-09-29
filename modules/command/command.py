"""
Decision-making logic.
"""

import math
from typing import Union, Tuple
from pymavlink import mavutil

from ..common.modules.logger import logger
from ..telemetry import telemetry


class Position:
    """
    3D vector struct.
    """

    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


# =================================================================================================
#                            ↓ BOOTCAMPERS MODIFY BELOW THIS COMMENT ↓
# =================================================================================================
class Command:  # pylint: disable=too-many-instance-attributes
    """
    Command class to make a decision based on recieved telemetry,
    and send out commands based upon the data.
    """

    __private_key = object()

    @classmethod
    def create(
        cls,
        connection: mavutil.mavfile,
        target: Position,
        local_logger: logger.Logger,
    ) -> Tuple[bool, Union["Telemetry", None]]:
        """
        Falliable create (instantiation) method to create a Command object.
        """
        command = cls(cls.__private_key, connection, target, local_logger)
        local_logger.info("Command initialized")
        return True, command

    def __init__(
        self,
        key: object,
        connection: mavutil.mavfile,
        target: Position,
        local_logger: logger.Logger,
    ) -> None:
        assert key is Command.__private_key, "Use create() method"

        # Do any intializiation here
        self.connection = connection
        self.target = target
        self.logger = local_logger
        self.velocity_data = []

    def run_cmd(self, telemetry_data: telemetry.TelemetryData) -> str:
        """
        Make a decision based on received telemetry data.
        """
        # Calculate average velocity in x, y, z
        vx, vy, vz = telemetry_data.x_velocity, telemetry_data.y_velocity, telemetry_data.z_velocity
        self.velocity_data.append([vx, vy, vz])
        sum_vx = 0
        sum_vy = 0
        sum_vz = 0
        for v in self.velocity_data:
            sum_vx += v[0]
            sum_vy += v[1]
            sum_vz += v[2]
        avg_vx = sum_vx / (len(self.velocity_data) * 1.0)
        avg_vy = sum_vy / (len(self.velocity_data) * 1.0)
        avg_vz = sum_vz / (len(self.velocity_data) * 1.0)
        # Log average velocity for this trip so far
        self.logger.info(f"Average Velocity: {avg_vx}, {avg_vy}, {avg_vz}")

        # Use COMMAND_LONG (76) message, assume the target_system=1 and target_componenet=0
        # The appropriate commands to use are instructed below

        # Adjust height using the comand MAV_CMD_CONDITION_CHANGE_ALT (113)
        # String to return to main: "CHANGE_ALTITUDE: {amount you changed it by, delta height in meters}"

        if abs(self.target.z - telemetry_data.z) > 0.5:  # need to adjust altitude
            self.connection.mav.command_long_send(
                1,  # target_system
                0,  # target_component
                mavutil.mavlink.MAV_CMD_CONDITION_CHANGE_ALT,  # command
                0,  # confirmation
                1,  # param1: descend/ascend rate (m/s)
                0,
                0,
                0,
                0,
                0,  # param2-param6 unused
                self.target.z,  # param7: target altitude (m)
            )
            return f"CHANGE ALTITUDE: {self.target.z - telemetry_data.z}m"

        # Adjust direction (yaw) using MAV_CMD_CONDITION_YAW (115). Must use relative angle to current state
        # String to return to main: "CHANGING_YAW: {degree you changed it by in range [-180, 180]}"
        # Positive angle is counter-clockwise as in a right handed system

        # calculate angle in rad, then convert to degrees
        target_yaw_deg = math.degrees(
            math.atan2(self.target.y - telemetry_data.y, self.target.x - telemetry_data.x)
        )
        now_yaw_deg = math.degrees(telemetry_data.yaw)
        yaw_angle = (target_yaw_deg - now_yaw_deg + 180) % 360 - 180

        if (abs(yaw_angle)) > 5:  # need to adjust direction
            direction = -1  # if angle positive, counter-clockwise
            if yaw_angle <= 0:
                direction = 1  # if angle negative, clockwise
            self.connection.mav.command_long_send(
                1,  # target_system
                0,  # target_component
                mavutil.mavlink.MAV_CMD_CONDITION_YAW,  # command
                0,  # confirmation
                yaw_angle,  # degrees
                5,  # angular speed
                direction,  # direction
                1,  # relative offset
                0,
                0,
                0,  # param5-param7 not used
            )
            return f"CHANGE YAW: {yaw_angle}"
        return ""


# =================================================================================================
#                            ↑ BOOTCAMPERS MODIFY ABOVE THIS COMMENT ↑
# =================================================================================================
