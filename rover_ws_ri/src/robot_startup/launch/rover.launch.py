from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    
    state_ctrl = Node(
        package="locomotion_core",
        executable="rover_state_controller",
    )

    drive_core = Node(
        package="locomotion_core",
        executable="movebase_kinematics",
    )

    du_enable = Node(
        package="locomotion_core",
        executable="rover_enable",
    )
    
    cmd_roboteq1 = Node(
        package="locomotion_core",
        executable="cmd_roboteq",
    )

    cmd_roboteq2 = Node(
        package="locomotion_core",
        executable="cmd_roboteq2",
    )


    ld.add_action(drive_core)
    ld.add_action(du_enable)
    ld.add_action(cmd_roboteq1)
    ld.add_action(cmd_roboteq2)
    ld.add_action(state_ctrl)

    return ld


