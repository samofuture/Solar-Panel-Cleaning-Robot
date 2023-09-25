from roboclaw_python.roboclaw_3 import Roboclaw as rc

# Useful resource for roboclaw library: https://resources.basicmicro.com/using-the-roboclaw-python-library/

if __name__ == '__main__':
    left_motors = rc("/dev/ttyS0", 38400)
    
    left_motors.Open()
    left_motors.ForwardMixed(0x80, 63)
    left_motors.BackwardM1(0x80, )