# ------------------------------------------
#
#   Project:      Competition Code
#   Author:       HG5_ELECTR!C
#   Description:  Right Side
#
# ------------------------------------------

"""
This is the competition code for our robot when we start on the
right of the field (which is important for the autonomous section).
"""

# library imports
from vex import *
import urandom

# brain should be defined by default
brain = Brain()

# robot configuration code
left_motor_a = Motor(Ports.PORT1, GearSetting.RATIO_36_1, False)
left_motor_b = Motor(Ports.PORT3, GearSetting.RATIO_36_1, False)
left_drive_smart = MotorGroup(left_motor_a, left_motor_b)
right_motor_a = Motor(Ports.PORT2, GearSetting.RATIO_36_1, True)
right_motor_b = Motor(Ports.PORT4, GearSetting.RATIO_36_1, True)
right_drive_smart = MotorGroup(right_motor_a, right_motor_b)
drivetrain = DriveTrain(left_drive_smart, right_drive_smart, 319.19, 295, 40, MM, 1)
conveyor_motor_a = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
conveyor_motor_b = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
conveyor = MotorGroup(conveyor_motor_a, conveyor_motor_b)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

def initializeRandomSeed():
    """
    make random actually random
    """
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
     
# set random seed
initializeRandomSeed()

def play_vexcode_sound(sound_name):
    """
    helper to make playing sounds from the V5 in VEXcode easier and
    keeps the code cleaner by making it clear what is happening
    :param sound_name: string
    """
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

def pre_autonomous():
    """
    actions to do when the program starts
    """
    brain.screen.clear_screen()
    brain.screen.print("Waiting for autonomous to begin...")
    wait(1, SECONDS)

def autonomous():
    """
    starts facing the right wall, loads 3 balls and then scores all 3
    """
    brain.screen.clear_screen()
    brain.screen.print("Autonomous code running...")
    drivetrain.drive_for(REVERSE, 125, MM)
    drivetrain.turn_for(RIGHT, 80, DEGREES)
    drivetrain.drive_for(REVERSE, 690, MM)
    conveyor.set_velocity(100,PERCENT)
    conveyor.spin_for(REVERSE, 1250, DEGREES) # load 3
    drivetrain.turn_for(RIGHT, 45, DEGREES)
    drivetrain.drive_for(REVERSE, 110, MM)
    drivetrain.turn_for(RIGHT, 10, DEGREES)
    conveyor.spin_for(FORWARD, 3240, DEGREES) # score 3 balls

def user_control():
    """
    defines controller buttons for driver controlled secton
    """
    brain.screen.clear_screen()
    controller = Controller()
    while True:
        left_motor_a.set_velocity(controller.axis3.position(), PERCENT)
        left_motor_a.spin(REVERSE)
        left_motor_b.set_velocity(controller.axis3.position(), PERCENT)
        left_motor_b.spin(REVERSE)

        right_motor_a.set_velocity(controller.axis2.position(), PERCENT)
        right_motor_a.spin(REVERSE)
        right_motor_b.set_velocity(controller.axis2.position(), PERCENT)
        right_motor_b.spin(REVERSE)
       
        wait(5, MSEC)

        # move conveyor belt up (pick up or place ball into high tube)
        conveyor.set_velocity(100, PERCENT)
        if controller.buttonR1.pressing():
            conveyor.spin(FORWARD)
        # place ball into lower tube
        elif controller.buttonR2.pressing():
            conveyor.spin(REVERSE)
        else:
            # stop conveyor belt
            conveyor.stop()
        wait(20, MSEC)

"""
while lines 122-123 would conventionally be wrapped in if __name__ == "__main__"
we have not done this as it appeared to be unsupported in the VEX environment
"""

# create competition instance
comp = Competition(user_control, autonomous)
pre_autonomous()
