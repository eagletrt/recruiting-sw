# INTERNAL sim interface (can_gateway -> vehicle_sim). Candidates must use CAN instead.
std_msgs/Header header
float32 throttle          # [0, 1]
float32 brake             # [0, 1]
bool emergency_brake
