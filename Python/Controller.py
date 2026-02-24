# ------------------------------------------
#
#   Project:      Controller Code
#   Author:       HG5_ELECTR!C
#   Description:  VEXcode V5 Python Test Code
#
# ------------------------------------------

"""
This is the test code for our robot - it is used solely during training
and does not include a competition instance.
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
descorer = DigitalOut(brain.three_wire_port.a)
match_loader = DigitalOut(brain.three_wire_port.b)

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

def user_control():
    """
    begins project code and defines controller buttons
    """
    brain.screen.clear_screen()
    controller = Controller()
    drivetrain.set_drive_velocity(100, PERCENT)
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

        # moving the descorer
        if controller.buttonL2.pressing():
            # open descorer
            descorer.set(True)
        elif controller.buttonL1.pressing():
            # close descorer
            descorer.set(False)

        # moving the loader
        if controller.buttonDown.pressing():
            # open loader
            match_loader.set(True)
        elif controller.buttonUp.pressing():
            # close loader
            match_loader.set(False)

"""
while line 116 would conventionally be wrapped in if __name__ == "__main__"
we have not done this as it appeared to be unsupported in the VEX environment
"""

user_control()
