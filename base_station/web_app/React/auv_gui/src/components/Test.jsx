import React, { useEffect, useState } from "react";
import axios from 'axios';
import {
  Box,
  Button,
  Center,
  Flex,
  FormControl,
  FormLabel,
  Input,
  Select,
  Spacer,
  Stack,
  Text,
  VStack
} from "@chakra-ui/react";

export default function Tests() {
  const [imuData, setImuData] = useState({ magnetometer: '', accelerometer: '', gyroscope: '' });
  const [insData, setInsData] = useState({ heading: '', roll: '', pitch: '' });
  const [motorTest, setMotorTest] = useState({ motor: '', speed: '', duration: '' });
  const [targetHeading, setTargetHeading] = useState('');
  const [pidConstants, setPidConstants] = useState({ heading: { p: '', i: '', d: '' }, pitch: { p: '', i: '', d: '' }, roll: { p: '', i: '', d: '' } });
  const [displayedPidConstants, setDisplayedPidConstants] = useState({ heading: { p: '', i: '', d: '' }, pitch: { p: '', i: '', d: '' }, roll: { p: '', i: '', d: '' } });

  // Input handlers for forms
  const handleInputChange = (e, form, field) => {
    const newForm = { ...form, [field]: e.target.value };
    switch (form) {
      case motorTest:
        setMotorTest(newForm);
        break;
      case pidConstants.heading:
      case pidConstants.pitch:
      case pidConstants.roll:
        const [axis, constant] = field.split('.');
        setPidConstants({
          ...pidConstants,
          [axis]: { ...pidConstants[axis], [constant]: e.target.value }
        });
        break;
      case targetHeading:
        setTargetHeading(e.target.value);
        break;
      default:
        break;
    }
  };

  const handleSetConstants = (axis) => {
    // Update the displayed constants
    setDisplayedPidConstants(prev => ({
      ...prev,
      [axis]: { ...pidConstants[axis] }
    }));

    // Post request to save the constants
    handlePostRequest(`${axis}_pid_constants`, pidConstants[axis]);
  };

  const handlePostRequest = async (url, data) => {
    try {
      const response = await axios.post(`http://localhost:6543/${url}`, data);
      console.log(response.data);
    } catch (error) {
      console.error('Error posting data:', error);
    }
  };

  // Fetch data from server
  useEffect(() => {
    const fetchData = async () => {
      const imuResponse = await axios.get("http://localhost:6543/imu_calibration_data");
      setImuData(imuResponse.data);
      const insResponse = await axios.get("http://localhost:6543/ins_data");
      setInsData(insResponse.data);
    };
    fetchData();
  }, []);

  return (
    <Stack spacing={5}>
      <Center><Text fontSize="4xl">Testing and Calibration</Text></Center>

      <Flex>
        <Box flex="1" bg="blue.500"><Text>Graph 1</Text></Box>
        <Box flex="1" bg="red.500"><Text>Graph 2</Text></Box>
        <Box flex="1" bg="tomato"><Text>Graph 3</Text></Box>
      </Flex>

      <Center><Text fontSize="2xl">Current IMU Calibration:</Text></Center>
      <Center>
        <Flex width="80%">
          <Text>Magnetometer: </Text><Spacer /><Text>{imuData.magnetometer}</Text>
          <Spacer />
          <Text>Accelerometer: </Text><Spacer /><Text>{imuData.accelerometer}</Text>
          <Spacer />
          <Text>Gyroscope: </Text><Spacer /><Text>{imuData.gyroscope}</Text>
        </Flex>
      </Center>

      <Center><Text fontSize="2xl">Current INS Data:</Text></Center>
      <Center>
        <Flex width="80%">
          <Text>Heading: </Text><Spacer /><Text>{insData.heading}</Text>
          <Spacer />
          <Text>Roll: </Text><Spacer /><Text>{insData.roll}</Text>
          <Spacer />
          <Text>Pitch: </Text><Spacer /><Text>{insData.pitch}</Text>
        </Flex>
      </Center>

      <Center>
        <Flex width="90%" gap={6}>
          <FormControl>
            <FormLabel>Motor Testing</FormLabel>
            <VStack spacing={4} align="stretch">
              <Select placeholder="Select Motor" onChange={e => handleInputChange(e, motorTest, 'motor')}>
                <option value="Forward">Forward</option>
                <option value="Backward">Backward</option>
                <option value="Down">Down</option>
                <option value="Left">Left</option>
                <option value="Right">Right</option>
              </Select>
              <Input placeholder="Enter motor speed" onChange={e => handleInputChange(e, motorTest, 'speed')} />
              <Input placeholder="Enter duration of run" onChange={e => handleInputChange(e, motorTest, 'duration')} />
              <Button colorScheme="blue" onClick={() => handlePostRequest('motor_test', motorTest)}>Begin Test</Button>
            </VStack>
          </FormControl>
          <FormControl>
            <FormLabel>Heading Test</FormLabel>
            <VStack spacing={4} align="stretch">
              <Input placeholder="Enter target heading" onChange={e => handleInputChange(e, targetHeading, 'targetHeading')} />
              <Button colorScheme="blue" onClick={() => handlePostRequest('heading_test', { heading: targetHeading })}>Begin Test</Button>
            </VStack>
          </FormControl>
        </Flex>
      </Center>

      <Center>
        <Flex width="90%" gap={4}>
          {Object.keys(pidConstants).map(axis => (
            <FormControl key={axis}>
              <FormLabel>Set {axis.charAt(0).toUpperCase() + axis.slice(1)} PID Constants</FormLabel>
              <VStack spacing={4} align="stretch">
                <Input placeholder="P" onChange={e => handleInputChange(e, pidConstants[axis], `${axis}.p`)} />
                <Input placeholder="I" onChange={e => handleInputChange(e, pidConstants[axis], `${axis}.i`)} />
                <Input placeholder="D" onChange={e => handleInputChange(e, pidConstants[axis], `${axis}.d`)} />
                <Button colorScheme="blue" onClick={() => handleSetConstants(axis)}>Set Constants</Button>
              </VStack>
            </FormControl>
          ))}
        </Flex>
      </Center>

      <Center>
        <Text fontSize="2xl">Entered PID Constants:</Text>
      </Center>
      <Center>
        <Box width="90%">
          {Object.keys(displayedPidConstants).map(axis => (
            <Box key={axis} mb={4}>
              <Text fontSize="lg" fontWeight="bold">{axis.charAt(0).toUpperCase() + axis.slice(1)}:</Text>
              <Text>P: {displayedPidConstants[axis].p} | I: {displayedPidConstants[axis].i} | D: {displayedPidConstants[axis].d}</Text>
            </Box>
          ))}
        </Box>
      </Center>
    </Stack>
  );
}