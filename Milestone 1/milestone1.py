import time
import numpy as np
from xarmclient import XArm

TOLERANCE = 0.02


def wait_until_reached(xarm, goal):
    # Verify robot reaches joint goal
    goal = np.array(goal)

    while True:
        current = np.array(xarm.get_joints()[0])

        if np.all(np.abs(current - goal) < TOLERANCE):
            break

        time.sleep(0.1)


def record_pose(xarm, label):
    input(f"\nMove robot using hand_control to {label}, then press ENTER...")
    joints = tuple(xarm.get_joints()[0])
    print(f"{label} recorded:", joints)
    return joints


def main():
    xarm = XArm()

    # Manual Recording Phase
    print("\nManual Recording Mode")

    xarm.home()
    xarm.grip(0)    # Open gripper

    print("\nEntering hand_control mode.")
    print("Exit hand_control by pressing any key + ENTER")

    xarm.hand_control()

    pick_pose = record_pose(xarm, "PICK POSE")
    lift_pose = record_pose(xarm, "LIFT POSE")
    mid_pose = record_pose(xarm, "MID (ACROSS) POSE")
    place_pose = record_pose(xarm, "PLACE POSE")
    end_pose = record_pose(xarm, "END POSE")

    input("\nPress ENTER to start automated motion.")

    # -------------------------
    # AUTOMATED EXECUTION
    # -------------------------
    print("\nAutomated Pick and Place")

    xarm.home()
    xarm.grip(0)

    # Move to pick
    print("Moving to pick pose.")
    xarm.set_joints(pick_pose)
    wait_until_reached(xarm, pick_pose)

    # Close gripper BEFORE lifting
    print("Closing gripper.")
    xarm.grip(1)
    time.sleep(1)

    # Lift up
    print("Lifting.")
    xarm.set_joints(lift_pose)
    wait_until_reached(xarm, lift_pose)

    # Move across (top of inverted U)
    print("Moving across.")
    xarm.set_joints(mid_pose)
    wait_until_reached(xarm, mid_pose)

    # Move down to place
    print("Moving to place pose.")
    xarm.set_joints(place_pose)
    wait_until_reached(xarm, place_pose)
    
    print("Placing down block.")
    xarm.set_joints(end_pose)
    wait_until_reached(xarm, end_pose)

    # Open gripper to release
    print("Opening gripper...")
    xarm.grip(0)
    time.sleep(1)

    print("Returning home...")
    xarm.home()


if __name__ == "__main__":
    main()