import cv2
import time
import os
import sys

def get_device():
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("[Camera] Error: Unable to access the camera.")
            return None
        return cap
    except cv2.error as e:
        print(f"[Camera] OpenCV error: {e}")
        return None
    except Exception as e:
        print(f"[Camera] Unexpected error: {e}")
        return None


def capturar_fotos(intervalo_segundos):
    while True:
        cap = get_device()
        if cap is None:
            print("Retrying camera connection in 5 seconds...")
            time.sleep(5)
            continue  # Retry connection
        
        # Camera connected and ready
        output_dir = "fotos_camara"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        print("Camera connected and capturing photos.")
        
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    print("Error: Could not capture image.")
                    break
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(output_dir, f"foto_{timestamp}.jpg")
                cv2.imwrite(filename, frame)
                time.sleep(intervalo_segundos)

            except Exception as e:
                print(f"Error during photo capture: {e}")
                break  # Break the photo capture loop

        cap.release()
        cv2.destroyAllWindows()


def main():
    # Verificar que el script reciba un parámetro de intervalo en segundos
    if len(sys.argv) != 2:
        print("Ejecutar:\npython captura_fotos.py <intervalo_segundos>")
        sys.exit(1)

    try:
        # Obtener el intervalo de captura en segundos desde el argumento
        intervalo_segundos = float(sys.argv[1])

        # Asegurarse de que el intervalo sea positivo
        if intervalo_segundos <= 0:
            raise ValueError("El intervalo debe ser un número positivo.")

        capturar_fotos(intervalo_segundos)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    