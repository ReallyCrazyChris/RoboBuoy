
from machine import PWM, Pin

# PWM control of ESC motor controlers 
motorLeft = PWM(Pin(2), duty=58, freq=50)
motorRight = PWM(Pin(13), duty=58, freq=50)

def driveMotors(vl=58,vr=58):
    # clamp max and min motor speeds  
    pwmLeft = min(95, max(58, vl)) 
    pwmRight = min(95, max(58, vr)) 
    # Drive the motors
    motorLeft.duty(pwmLeft)
    motorRight.duty(pwmRight)
    print('vl',vl,'vr',vr,'pwmL',pwmLeft,'pwmR',pwmRight)

def stopMotors():
    motorLeft.duty(58) 
    motorRight.duty(58)  


