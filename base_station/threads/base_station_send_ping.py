# System imports
import serial
import time
import threading

# Custom imports
from api import Radio
from static import constants
from static import global_vars


class BaseStation_Send_Ping(threading.Thread):
    def __init__(self, radio, out_q=None):
        self.radio = radio
        self.out_q = out_q
        threading.Thread.__init__(self)

    def run(self):
        """ Constructor for the AUV """
        # Try to assign us a new Radio object
        self.main_loop()

    def main_loop(self):
        """ Main connection loop for the AUV. """
        print("Starting main ping sending connection loop.")
        while True:
            time.sleep(constants.PING_SLEEP_DELAY)
            print("[BS] Trying to send ping")
            # will break if global_vars.radio is ever None please add check for that at some point
            is_radio_open = global_vars.radio.is_open()
            if global_vars.radio is None or is_radio_open is False:
                global_vars.connect_to_radio(self.out_q)
            else:
                try:
                    # Always send a connection verification packet
                    if not global_vars.downloading_file:
                        print("[BS] Actually sent ping")
                        constants.radio_lock.acquire()
                        global_vars.radio.write(constants.PING)
                        constants.radio_lock.release()

                except Exception as e:
                    print("[BS] Exception thrown in bs send ping")
