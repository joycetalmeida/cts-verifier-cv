import subprocess
import time

class DeviceConnection:
    def __init__(self, serial_number=None):
        """
        Initialize the AndroidDevice class with an specified serial number.
        :param str serial_number: The serial number provided. Optional parameter.
        """
        self.serial_number = serial_number
        self.connected_device = None

    def execute_adb_command(self, command):
        """
        Execute ADB command using subprocess.
        :param str command: ADB command to be executed on the device.
        """
        full_command = ['adb']
        if self.serial_number:
            full_command.extend(['-s', self.serial_number]) 
        full_command.extend(command.split())

        try:
            result = subprocess.run(full_command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {' '.join(full_command)}")
            print(f"Error message: {e.stderr}")
            return None

    def connect_device(self):
        """
        Connect to the specified Android device or the first available one if no serial number is given.
        """
        try:
            devices = self.execute_adb_command('devices')
            if devices:
                print("Connected devices:")
                print(devices)
                device_lines = [line for line in devices.splitlines() if "device" in line and not "devices" in line]

                if not device_lines:
                    print("No devices found. Please connect your device and enable USB debugging.")
                    return False

                if self.serial_number:
                    for line in device_lines:
                        if self.serial_number in line:
                            self.connected_device = self.serial_number
                            print(f"Device connected with serial: {self.serial_number}")
                            break
                    else:
                        print(f"Device with serial {self.serial_number} not found.")
                        return False
                else:
                    self.connected_device = device_lines[0].split()[0]
                    print(f"Connected to the first available device: {self.connected_device}")

                return True
            else:
                print("Failed to list devices.")
                return False
        except Exception as e:
            print(f"An error occurred while connecting to device: {str(e)}")
            return False

    def navigate_to_home(self):
        """
        Navigate to the home screen of the Android device.
        """
        try:
            print("Navigating to Home screen...")
            self.execute_adb_command('shell input keyevent 3')
            time.sleep(2)
        except Exception as e:
            print(f"Failed to navigate to home: {str(e)}")

    def launch_app(self, package_name, activity_name):
        """
        Launch a specific app by intent with the package and activity name.
        :param str package_name: the app package to be launched.
        :param str activity_name: the app activity to be launched.
        """
        try:
            print(f"Opening app {package_name}/{activity_name}...")
            self.execute_adb_command(f'shell am start -n {package_name}/{activity_name}')
            time.sleep(2)
        except Exception as e:
            print(f"Failed to open app {package_name}/{activity_name}: {str(e)}")

    def press_back(self):
        """
        Simulate the back button press.
        """
        try:
            print("Going back...")
            self.execute_adb_command('shell input keyevent 4')
            time.sleep(2)
        except Exception as e:
            print(f"Failed to go back: {str(e)}")
