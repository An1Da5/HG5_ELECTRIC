#pragma region VEXcode Generated Robot Configuration
// Make sure all required headers are included.
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <math.h>
#include <string.h>


#include "vex.h"

using namespace vex;

// Brain should be defined by default
brain Brain;


// START V5 MACROS
#define waitUntil(condition)                                                   \
  do {                                                                         \
    wait(5, msec);                                                             \
  } while (!(condition))

#define repeat(iterations)                                                     \
  for (int iterator = 0; iterator < iterations; iterator++)
// END V5 MACROS


// Robot configuration code.
motor leftMotorA = motor(PORT1, ratio18_1, false);
motor leftMotorB = motor(PORT3, ratio18_1, false);
motor_group LeftDriveSmart = motor_group(leftMotorA, leftMotorB);
motor rightMotorA = motor(PORT2, ratio18_1, true);
motor rightMotorB = motor(PORT4, ratio18_1, true);
motor_group RightDriveSmart = motor_group(rightMotorA, rightMotorB);
drivetrain Drivetrain = drivetrain(LeftDriveSmart, RightDriveSmart, 319.19, 295, 40, mm, 1);

motor conveyorMotorA = motor(PORT5, ratio18_1, false);
motor conveyorMotorB = motor(PORT6, ratio18_1, false);
motor_group conveyor = motor_group(conveyorMotorA, conveyorMotorB);

digital_out descorer = digital_out(Brain.ThreeWirePort.A);
digital_out match_loader = digital_out(Brain.ThreeWirePort.B);


// generating and setting random seed
void initializeRandomSeed(){
  int systemTime = Brain.Timer.systemHighResolution();
  double batteryCurrent = Brain.Battery.current();
  double batteryVoltage = Brain.Battery.voltage(voltageUnits::mV);

  // Combine these values into a single integer
  int seed = int(batteryVoltage + batteryCurrent * 100) + systemTime;

  // Set the seed
  srand(seed);
}



void vexcodeInit() {

  //Initializing random seed.
  initializeRandomSeed(); 
}


// Helper to make playing sounds from the V5 in VEXcode easier and
// keeps the code cleaner by making it clear what is happening.
void playVexcodeSound(const char *soundName) {
  printf("VEXPlaySound:%s\n", soundName);
  wait(5, msec);
}

#pragma endregion VEXcode Generated Robot Configuration

controller Controller = controller(primary);

// Competition instance
competition Competition;

/*---------------------------------------------------------------------------*/
/*                            Pre-Autonomous                                 */
/*---------------------------------------------------------------------------*/
void pre_autonomous() {
    Brain.Screen.clearScreen();
    Brain.Screen.print("Waiting for autonomous to begin...");
    wait(1, seconds);
}

/*---------------------------------------------------------------------------*/
/*                              Autonomous                                   */
/*---------------------------------------------------------------------------*/
void autonomous() {
    Brain.Screen.clearScreen();
    Brain.Screen.print("Autonomous code running...");

    // Auton code - start facing right wall
    Drivetrain.driveFor(reverse, 375, mm);
    Drivetrain.turnFor(left, 45, degrees);
    Drivetrain.driveFor(forward, 245, mm);
    conveyor.setVelocity(100, percent);
    conveyor.spinFor(reverse, 1800, degrees);   // load 1
}

/*---------------------------------------------------------------------------*/
/*                             User Control                                  */
/*---------------------------------------------------------------------------*/
void user_control() {
    Brain.Screen.clearScreen();
    Drivetrain.setDriveVelocity(75, percent);
    while (true) {
        // Tank drive - Axis3 = left stick vertical, Axis2 = right stick vertical
        int leftSpeed  = Controller.Axis3.position();
        int rightSpeed = Controller.Axis2.position();

        leftMotorA.setVelocity(leftSpeed, percent);
        leftMotorA.spin(reverse);
        leftMotorB.setVelocity(leftSpeed, percent);
        leftMotorB.spin(reverse);

        rightMotorA.setVelocity(rightSpeed, percent);
        rightMotorA.spin(reverse);
        rightMotorB.setVelocity(rightSpeed, percent);
        rightMotorB.spin(reverse);

        wait(5, msec);

        // Conveyor belt control
        conveyor.setVelocity(100, percent);
        if (Controller.ButtonR1.pressing()) {
            conveyor.spin(forward);          // pick up / place into high tube
        } else if (Controller.ButtonR2.pressing()) {
            conveyor.spin(reverse);          // place into lower tube
        } else {
            conveyor.stop();
        }

        // Descorer control
        if (Controller.ButtonL2.pressing()) {
            descorer.set(true);   // close
        } else if (Controller.ButtonL1.pressing()) {
            descorer.set(false);  // open
        }

        // Match loader control
        if (Controller.ButtonDown.pressing()) {
            match_loader.set(true);   // open
        } else if (Controller.ButtonUp.pressing()) {
            match_loader.set(false);  // close
        }

        // Quick turns
        if (Controller.ButtonLeft.pressing()) {
            Drivetrain.turnFor(right, 90, degrees);   // turn 90 degrees right
        } else if (Controller.ButtonRight.pressing()) {
            Drivetrain.turnFor(left, 90, degrees);  // turn 90 degrees left
        }

        wait(20, msec);
    }
}

/*---------------------------------------------------------------------------*/
/*                                  Main                                     */
/*---------------------------------------------------------------------------*/
int main() {
    // Initialize random seed
    srand((int)(Brain.Battery.voltage(voltageUnits::mV)
              + Brain.Battery.current(currentUnits::amp) * 100
              + Brain.Timer.systemHighResolution()));

    wait(200, msec);
    Brain.Screen.clearScreen();

    // Register competition callbacks
    Competition.autonomous(autonomous);
    Competition.drivercontrol(user_control);

    // Run pre-autonomous
    pre_autonomous();

    // Idle loop — competition switch drives autonomous/user_control callbacks
    while (true) {
        wait(100, msec);
    }

    return 0;
}
