from time import sleep
import time
from usbiss.spi import SPI
import opcng as opc
import csv
import asyncio

# Configurar puerto serial
PORT = 'COM6' #windows
# PORT = '/dev/ttyUSB0' # linux

# Intervalo de meidicón (Cada n segundos)
SEGUNDOS = 1

def get_device(com_port: str):
    spi = SPI(com_port)
    spi.mode = 1
    spi.max_speed_hz = 500000
    spi.lsbfirst = False
    dev = opc.OPCN2(spi)
    return dev

def get_device_info(dev):
    print(f'serial: {dev.serial()}')
    sleep(1)
    print(f'firmware version: {dev.serial()}')
    sleep(1)
    print(f'Power state: {dev.power_state()}')

def get_hist(interval, serial_port):
    csv_filename = 'pm_data_' + time.strftime('%Y%m%d_%H%M%S') + '.csv'
    field_names = ['timestamp', "timestamp_linux", 'Bin 0', 'Bin 1', 'Bin 2', 'Bin 3', 'Bin 4', 'Bin 5', 'Bin 6', 'Bin 7',
                    'Bin 8', 'Bin 9', 'Bin 10', 'Bin 11', 'Bin 12', 'Bin 13', 'Bin 14', 'Bin 15', 'Bin1 MToF', 'Bin3 MToF',
                    'Bin5 MToF', 'Bin7 MToF', 'SFR', 'Temperature', 'Sampling Period', 'Checksum', 'PM1', 'PM2.5', 'PM10']

    with open(csv_filename, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        while True:
            try:
                dev = get_device(serial_port)
                sleep(1)
                dev.on()
                sleep(1)
                print("Saving pm records...")
                while True:
                    sleep(interval)
                    temp = dev.histogram()
                    if temp:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        timestamp_linux = int(time.time())
                        temp.update({'timestamp': timestamp, "timestamp_linux": timestamp_linux})
                        writer.writerow(temp)
                        #print(f'Saved data at {timestamp}: {temp}')
            except Exception as e:
                print(f"Error: {e}")
                print("Retrying pm connection in 10 seconds...")
                time.sleep(10)


if __name__ == "__main__":
    get_hist(1,PORT)
