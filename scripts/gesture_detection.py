# Arquivo: scripts/gesture_detection.py
import mediapipe as mp
import cv2

class DetectorGestos:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_draw = mp.solutions.drawing_utils
        
        # Estado para estabilização do gesto
        self.gesto_atual = None
        self.frames_frames_consecutivos = 0
        self.LIMITE_ESTABILIZACAO = 15 # ~0.5 segundos

    def processar(self, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        return results

    def desenhar_landmarks(self, frame, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

    def analisar_gesto(self, results):
        """
        Retorna 'GRAB' (fechada), 'DROP' (aberta) ou None.
        """
        if not results.multi_hand_landmarks:
            self.frames_frames_consecutivos = 0
            self.gesto_atual = None
            return None

        for hand_landmarks in results.multi_hand_landmarks:
            lms = hand_landmarks.landmark
            
            # Verificar dedos (Indicador, Médio, Anelar, Mindinho)
            # Dedo levantado: Ponta (TIP) acima da articulação (PIP) -> Y menor
            # Dedo fechado: Ponta (TIP) abaixo da articulação (PIP) -> Y maior
            
            dedos_fechados = []
            
            # IDs das pontas: 8, 12, 16, 20
            # IDs das dobras (PIP): 6, 10, 14, 18
            # Polegar é especial, vamos ignorar para simplificar Grab vs Drop, focar nos 4 dedos
            
            ids_dedos = [(8,6), (12,10), (16,14), (20,18)]
            
            cnt_fechados = 0
            for tip, pip in ids_dedos:
                # OpenCV Y: 0 é topo, 1 é base. 
                # Se Tip Y > Pip Y, o dedo está para baixo (fechado na palma)
                if lms[tip].y > lms[pip].y:
                    cnt_fechados += 1
            
            novo_gesto = None
            
            # Se 4 dedos estão fechados -> GRAB
            if cnt_fechados == 4:
                novo_gesto = "GRAB"
            # Se 0 dedos estão fechados (todos abertos) -> DROP
            elif cnt_fechados == 0:
                novo_gesto = "DROP"
            
            # Estabilização (Debounce)
            if novo_gesto == self.gesto_atual:
                self.frames_frames_consecutivos += 1
            else:
                self.gesto_atual = novo_gesto
                self.frames_frames_consecutivos = 0
                
            if self.frames_frames_consecutivos > self.LIMITE_ESTABILIZACAO:
                return self.gesto_atual
                
        return None