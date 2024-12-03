import sys
from modulos import camara, opcn2, gps_recorder
import multiprocessing
import serial.tools.list_ports


def find_devices():
    hardwareId = {"04D8:FFEE": "OPC",
                  "1A86:7523": "GPS"}

    ports = serial.tools.list_ports.comports()

    devices_port = {}

    if ports:
        for port in ports:
            for key in hardwareId:
                if key in port.hwid:
                    devices_port[hardwareId[key]] = port.device
    
    return devices_port

def run_camera(interval):
    """
    Create and run the camera instance in a separate process.
    """
    try:
        camara.capturar_fotos(interval)
    except Exception as e:
        print(f"Camera process encountered an error: {e}")


def run_opc(serial_port, interval):
    """
    Create and run the OPC instance in a separate process.
    """
    try:
        opcn2.get_hist(interval, serial_port)
    except Exception as e:
        print(f"OPC process encountered an error: {e}")

def run_gps(serial_port):
    """
    Create and run gps
    """
    try:
        gps_recorder.run_gps(serial_port)
    except Exception as e:
        print(f"GPS process encountered an error: {e}")

def main(device_port: dict, waiting_time: dict):
    """
    Run everything in separate processes.
    """
    processes = []
    
    try:
        # Camera process
        try:
            camera_process = multiprocessing.Process(target=run_camera, args=(waiting_time["camera"],))
            camera_process.start()
            processes.append(camera_process)
            print("Camera process started successfully.")
        except Exception as e:
            print(f"An error occurred while starting the camera process: {e}")

        # OPC process
        try:
            opc_process = multiprocessing.Process(target=run_opc, args=(device_port["OPC"], waiting_time["opc"]))
            opc_process.start()
            processes.append(opc_process)
            print("OPC process started successfully.")
        except Exception as e:
            print(f"An error occurred while starting the OPC process: {e}")

        # GPS process
        try:
            gps_process = multiprocessing.Process(target=run_gps, args=(device_port["GPS"],))
            gps_process.start()
            processes.append(gps_process)
            print("GPS process started successfully.")
        except Exception as e:
            print(f"An error occurred while starting the GPS process: {e}")
        
        # Wait for all started processes to complete
        for process in processes:
            process.join()

    except Exception as e:
        print(f"An unexpected error occurred in the main function: {e}")


if __name__ == "__main__":
    try:
        devices = find_devices()
        if not devices:
            raise Exception("Make sure the GPS and OPC are connected")
        
        print("All devices have been found correctly")
        waiting_time = {"camera": 1, "opc": 1}
        for key in waiting_time:
            val = int(input(f"Seconds to wait between {key} records: "))
            waiting_time[key] = val
        
        main(devices, waiting_time)
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to exit...")
