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
    try:
        # Asynchronously obtain instances
        print("Obtaining devices...")
        # Prepare multiprocessing for running both instances
        camera_process = multiprocessing.Process(target=run_camera, args=(waiting_time["camera"],))
        opc_process = multiprocessing.Process(target=run_opc, args=(device_port["OPC"], waiting_time["opc"]))
        gps_process = multiprocessing.Process(target=run_gps, args=(device_port["GPS"],))

        # Start both processes
        camera_process.start()
        opc_process.start()
        gps_process.start()

        # Wait for processes to complete
        camera_process.join()
        opc_process.join()
        gps_process.join()

    except Exception as e:
        print(f"An error occurred in the main function: {e}")


if __name__ == "__main__":
    devices = find_devices()
    if not devices:
        raise Exception("Make sure the gps and opc are conencted")
    
    print("All devices have been found correctly")
    waiting_time = {"camera":1, "opc":1}
    for key in waiting_time:
        val = int(input(f"Seconds to wait between {key} records: "))
        waiting_time[key] = val
 
    main(devices, waiting_time)