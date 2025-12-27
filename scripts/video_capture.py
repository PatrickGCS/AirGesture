# Arquivo: scripts/video_capture.py
import cv2

class WebcamManager:
    def __init__(self, source=0):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError("Não foi possível abrir a webcam.")

    def ler_frame(self):
        """Lê um frame da webcam."""
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame

    def mostrar_frame(self, frame, titulo="AirGesture Cam"):
        cv2.imshow(titulo, frame)

    def liberar(self):
        self.cap.release()
        cv2.destroyAllWindows()