# configure pneumatics
descorer = DigitalOut(brain.three_wire_port.a)
match_loader = DigitalOut(brain.three_wire_port.b)

if controller.buttonL2.pressing():
    # cylinder up for descorer
    descorer.set(True)
elif controller.buttonL1.pressing():
    # cylinder down for descorer
    descorer.set(False)

if controller.buttonDown.pressing():
    # cylinder up for loader
    match_loader.set(True)
elif controller.buttonUp.pressing():
    # cylinder down for loader
    match_loader.set(False)
