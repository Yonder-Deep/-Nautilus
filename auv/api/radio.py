"""
The radio class enables communication over wireless serial radios.
"""
import serial
import os
from .crc32 import Crc32
from static import constants

TIMEOUT_DURATION = 0
DEFAULT_BAUDRATE = 57600  # 115200


class Radio:
    def __init__(self, serial_path, baudrate=DEFAULT_BAUDRATE):
        """
        Initializes the radio object.

        serial_path: Absolute path to serial port for specified device.
        """

        # Establish connection to the serial radio.
        self.ser = serial.Serial(
            serial_path,
            baudrate=baudrate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=TIMEOUT_DURATION,
        )

    def write(self, message) -> None:
        """
        Sends provided message over serial connection.

        message: A string message that is sent over serial connection.
        """
        # Process different types of messages
        if isinstance(message, str):
            print("MSG BIG WRITE")
            encoded = str.encode(message + "\n")
            self.ser.write(encoded)

        elif isinstance(message, int):
            # print("bytes written")
            # message = Crc32.generate(message)
            message_double = Crc32.generate(message)
            byte_arr = message_double.to_bytes((constants.COMM_BUFFER_WIDTH), "big")
            self.ser.write(byte_arr)

    def read(self, n_bytes=1) -> bytes:
        """
        Returns array of bytes
        """
        return self.ser.read(n_bytes)

    def readlines(self) -> list[bytes]:
        """
        Returns a list of lines from buffer.
        """
        return self.ser.readlines()

    def readline(self) -> str:
        """
        Returns a string from the serial connection.
        """
        return self.ser.readline()

    def is_open(self) -> bool:
        """
        Returns a boolean if the serial connection is open.
        """
        return self.ser.is_open

    def flush(self) -> None:
        """
        Clears the buffer of the serial connection.
        """
        self.ser.flush()

    def close(self) -> None:
        """
        Closes the serial connection
        """
        self.ser.close()
