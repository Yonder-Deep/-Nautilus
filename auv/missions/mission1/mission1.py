MAX_DEPTH_METERS = 50.0
NEAR_SURFACE_METERS = 0.5


class Mission1():
    """ Dive and collect hydrophone data """

    def __init__(self, auv, motor_controller, pressure_sensor, IMU):
        """ Creates new audio collection mission object. Save parameters as local variables, and assign our state to starting state """

        self.motor_controller = motor_controller
        self.pressure_sensor = pressure_sensor
        self.IMU = IMU

        # Assign our state to starting state.
        self.state = "START"

    def loop(self):
        """ Continuously running loop function, run by AUV main thread. """
        if self.state == "START":
            if self.motor_controller is not None and self.pressure_sensor is not None and self.IMU is not None:
                # Begin our mission (start diving)
                self.motor_controller.update_motor_speeds([0, 0, 50, 50])
                self.state = "DIVING"

        if self.state == "DIVING":
            # Read Depth
            depth = self.pressure_sensor.depth()

            # If we reached max depth
            if depth >= MAX_DEPTH_METERS:
                # Turn off our motors
                self.motor_controller.update_motor_speeds([0, 0, 0, 0])

                # Set state to rising
                self.state = "RISING"

                # Start recording
                self.hydrophone.start_recording()

        if self.state == "RISING":
            # Read Depth
            depth = self.pressure_sensor.depth

            if depth <= NEAR_SURFACE_METERS:
                self.hydrophone.end_recording()
                self.state = "DONE"
