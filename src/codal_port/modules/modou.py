# 在这里写上你的代码 :-)
from microbit import i2c, pin1, pin8, pin14, pin15, pin16
from machine import time_pulse_us
from micropython import const
from neopixel import NeoPixel
from utime import sleep_us
from gc import collect

collect()
neo = NeoPixel(pin1, 3)

# light definition
LIGHT1 = const(8)
LIGHT2 = const(9)
LIGHT3 = const(7)
LIGHT4 = const(5)

# led definition
LED1 = const(0)
LED2 = const(1)
LED3 = const(2)

# stardard color
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (160, 32, 240)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# wheel definition
LEFT = const(0)
RIGHT = const(1)

def pwm_init():
    i2c.write(0x40, bytearray([0x00, 0x00]))
    # set frequence to 50hz
    i2c.write(0x40, bytearray([0x00]))
    old_mode = i2c.read(0x40, 1)[0]
    new_mode = (old_mode & 0x7F) | 0x10
    i2c.write(0x40, bytearray([0x00, new_mode]))
    i2c.write(0x40, bytearray([0xFE, 126]))
    i2c.write(0x40, bytearray([0x00, old_mode]))
    sleep_us(5)
    i2c.write(0x40, bytearray([0x00, (old_mode | 0xA1)]))

def pwm_set(ch, on, off):
    buffer = [0, 0, 0, 0, 0]
    buffer[0] = int(0x06 + 4 * ch)
    buffer[1] = int(on & 0xFF)
    buffer[2] = int((on >> 8) & 0xFF)
    buffer[3] = int(off & 0xFF)
    buffer[4] = int((off >> 8) & 0xFF)
    i2c.write(0x40, bytearray(buffer))

def set_header_angle(angle):
    if angle < 0 or angle > 180:
        raise ValueError('invalid header angle, use 0~180')
    # 50hz: 20,000 us
    v_us = (angle * 10 + 600.0)
    value = v_us * 4096.0 / 20000.0
    pwm_set(6, 0, int(value))

def set_led_color(n, color):
    if n < LED1 or n > LED3:
        raise ValueError('invalid led name, use LED1, LED2, LED3')
    neo[n] = color
    neo.show()

def set_light(light, brightness):
    if (light != LIGHT1) \
    and (light != LIGHT2) \
    and (light != LIGHT3) \
    and (light != LIGHT4):
        raise ValueError('invalid light name, e.g. LIGHT1')

    if brightness < 0 or brightness > 100:
        raise ValueError('invalid brightness value, use 0~100')

    level = brightness * 40.96
    pwm_set(light, 0, int(level))

def set_wheel(wheel, speed):
    if wheel != LEFT and wheel != RIGHT:
        raise ValueError('invalid wheel name: use LEFT or RIGHT')

    if speed < -100 or speed > 100:
        raise ValueError('invalid speed value: use -100~100')

    level = speed * 40.96
    if wheel == LEFT and level > 0:
        pwm_set(2, 0, int(level))
        pwm_set(3, 0, 0)

    elif wheel == LEFT and level <= 0:
        pwm_set(2, 0, 0)
        pwm_set(3, 0, int(-level))

    elif wheel == RIGHT and level > 0:
        pwm_set(0, 0, 0)
        pwm_set(1, 0, int(level))

    elif wheel == RIGHT and level <= 0:
        pwm_set(0, 0, int(-level))
        pwm_set(1, 0, 0)

def run(left_speed, right_speed):
    set_wheel(LEFT, left_speed)
    set_wheel(RIGHT, right_speed)

def stop():
    run(0, 0)

def sonar():
    pin15.read_digital()
    pin14.write_digital(1)
    sleep_us(10)
    pin14.write_digital(0)
    ts = time_pulse_us(pin15, 1, 25000)
    return ts * 9 / 6 / 58

def tracking():
    left = pin16.read_digital()
    right = pin8.read_digital()
    if left == 0 and right == 0:
        return '11'
    elif left == 0 and right == 1:
        return '10'
    elif left == 1 and right == 0:
        return '01'
    else:
        return '00'

def init():
    pwm_init()
    for ch in range(16):
        pwm_set(ch, 0, 0)
    set_led_color(LED1, BLACK)
    set_led_color(LED2, BLACK)
    set_led_color(LED3, BLACK)









