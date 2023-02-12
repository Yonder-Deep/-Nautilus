import threading

# Constants for the AUV
RADIO_PATH = {'radioNum': 1, 'path': '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0'}
RADIO_PATH_2 = {'radioNum': 2, 'path': '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D30AEU3V-if00-port0'}
RADIO_PATH_3 = {'radioNum': 3, 'path': '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D30AFD0I-if00-port0'}
RADIO_PATH_4 = {'radioNum': 4, 'path': '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D30AFALT-if00-port0'}
RADIO_PATH_5 = {'radioNum': 5, 'path': '/dev/serial/by-id/usb-FTDI_FT230X_Basic_UART_D30AF7PZ-if00-port0'}
RADIO_PATHS = [RADIO_PATH, RADIO_PATH_2, RADIO_PATH_3, RADIO_PATH_4, RADIO_PATH_5]
GPS_PATH = './/dev/serial/by-id/usb-Prolific_Technology_Inc._USB-Serial_Controller-if00-port0'
IMU_PATH = '/dev/serial0'
PING = 0xFFFFFF
SEND_SLEEP_DELAY = 1
RECEIVE_SLEEP_DELAY = 0.2
PING_SLEEP_DELAY = 3
CONNECTION_TIMEOUT = 6

# Encoding headers
POSITION_DATA = 0b000
HEADING_DATA = 0b001
MISC_DATA = 0b010
TEMP_DATA = 0b10011
DEPTH_DATA = 0b011

# Dive PID constants
P_PITCH = 5.0
I_PITCH = 2.0
D_PITCH = 0.0
P_DEPTH = 10.0
I_DEPTH = 2.0
D_DEPTH = 0.0
P_HEADING = 5.0
I_HEADING = 2.0
D_HEADING = 0.0
PID_DATA = 0b010

DEPTH_ENCODE = DEPTH_DATA << 21
HEADING_ENCODE = HEADING_DATA << 21
MISC_ENCODE = MISC_DATA << 21
POSITION_ENCODE = POSITION_DATA << 21
PID_ENCODE = PID_DATA << 21

DEF_DIVE_SPD = 100

MAX_TIME = 600
MAX_ITERATION_COUNT = MAX_TIME / SEND_SLEEP_DELAY / 7

# Header encodings from BS
NAV_ENCODE = 0b100000000000000000000000           # | with XSY (forward, angle sign, angle)
MOTOR_TEST_ENCODE = 0b101000000000000000000
XBOX_ENCODE = 0b111000000000000000000000          # | with XY (left/right, down/up xbox input)
MISSION_ENCODE = 0b000000000000000000000000       # | with X   (mission)
DIVE_ENCODE = 0b110000000000000000000000           # | with D   (depth)
KILL_ENCODE = 0b001000000000000000000000          # | with X (kill all / restart threads)
MANUAL_DIVE_ENCODE = 0b011000000000000000000000

LOCK = threading.Lock()  # checks if connected to BS over radio
RADIO_LOCK = threading.Lock()   # ensures one write to radio at a time

FILE_SEND_PACKET_SIZE = 7  # bytes
DIVE_LOG = "dive_log.txt"


def log(val):
    print("[AUV]\t" + val)
