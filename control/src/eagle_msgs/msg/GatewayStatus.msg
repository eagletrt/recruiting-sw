# INTERNAL sim interface (can_gateway -> referee / debugging).
std_msgs/Header header
bool emergency_brake
bool mission_finished       # last AS_CMD.MissionFinished received
float32 throttle_request    # last AS_CMD, [0, 1]
float32 brake_request       # last AS_CMD, [0, 1]
