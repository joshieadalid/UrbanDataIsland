import csv
import time
from serial import Serial
from pyubx2 import UBXReader, NMEA_PROTOCOL

CSV_FILENAME = 'gps_data_' + time.strftime('%Y%m%d_%H%M%S') + '.csv'
PORT = 'COM5' #windows
# PORT = '/dev/ttyUSB0' # linux
BAUD_RATE = 38400
FIELD_NAMES = ['timestamp', 'date', 'time', 'lat', 'lon', 'alt', 'altUnit', 'NS', 'EW', 'quality', 'numSV',
               'HDOP', 'sep', 'sepUnit', 'diffAge', 'diffStation', 'status', 'spd', 'cog', 'mv', 'mvEW',
               'posMode', 'navStatus', '_payload', '_checksum', '_validate', '_talker', '_immutable', '_msgID',
               '_logger', '_userdefined', 'NS', '_hpnmeamode', '_defsource', '_mode']

def run_gps(gps_serial_port):
    with open(CSV_FILENAME, mode='w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELD_NAMES)
        writer.writeheader()

        while True:
            try:
                with Serial(gps_serial_port, BAUD_RATE, timeout=3) as stream:
                    ubr = UBXReader(stream, protfilter=NMEA_PROTOCOL)

                    print("Saving gps records...")
                    while True:
                        _, parsed_data = ubr.read()

                        if parsed_data is not None and hasattr(parsed_data, 'lat'):
                            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                            data = parsed_data.__dict__
                            data.update({'timestamp': timestamp})
                            writer.writerow(data)
                            #print(f'Saved data at {timestamp}: {parsed_data}')
            except Exception as e:
                print(f"Error: {e}")
                print("Retrying gps connection in 5 seconds...")
                time.sleep(5)  # Espera 5 segundos antes de intentar reconectar


if __name__ == "__main__":
    run_gps(PORT)