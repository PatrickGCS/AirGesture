# Arquivo: main.py
import argparse
import time
import cv2
import sys
import os
from scripts.video_capture import WebcamManager
from scripts.gesture_detection import DetectorGestos
from rede.network_communication import ClienteNuvem
from utils.file_utils import obter_ultimo_arquivo_modificado, preparar_pastas

def main():
    parser = argparse.ArgumentParser(description="Cliente AirGesture - Nuvem")
    parser.add_argument("--server-ip", type=str, required=True, 
                        help="IP da máquina onde roda o server_central.py")
    
    args = parser.parse_args()
    
    # Prepara pastas locais
    preparar_pastas()
    pasta_recebidos = "AirGesture_Downloads"

    # Inicialização
    cam = WebcamManager()
    detector = DetectorGestos()
    cliente = ClienteNuvem(args.server_ip)
    
    # Cooldowns
    COOLDOWN = 3
    ultimo_acao = 0
    
    msg_status = "Aguardando Gesto..."
    cor_status = (0, 255, 0) # Verde

    print(f"=== CLIENTE AIRGESTURE ===")
    print(f"Conectado à nuvem em: {args.server_ip}")
    print("GESTOS:")
    print("  - Mão FECHADA (Fist): PEGAR (Upload do arquivo mais recente em AirGesture_Source)")
    print("  - Mão ABERTA (Palm):  SOLTAR (Download da nuvem para AirGesture_Downloads)")

    try:
        while True:
            frame = cam.ler_frame()
            if frame is None: break
            
            # Detecção
            resultados = detector.processar(frame)
            gesto = detector.analisar_gesto(resultados)
            
            agora = time.time()
            
            # Lógica de Ação
            if agora - ultimo_acao > COOLDOWN:
                if gesto == "GRAB":
                    # Ação: UPLOAD
                    arquivo_alvo = obter_ultimo_arquivo_modificado()
                    if arquivo_alvo:
                        msg_status = f"Enviando: {os.path.basename(arquivo_alvo)}"
                        cor_status = (0, 165, 255) # Laranja
                        
                        # Feedback visual imediato
                        cv2.putText(frame, "GRAB DETECTADO!", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_status, 2)
                        cam.mostrar_frame(frame)
                        cv2.waitKey(1)
                        
                        sucesso = cliente.enviar_arquivo(arquivo_alvo)
                        if sucesso:
                            msg_status = "Sucesso: Arquivo na Nuvem!"
                            cor_status = (0, 0, 255) # Vermelho
                        else:
                            msg_status = "Erro no Envio"
                    else:
                        msg_status = "Nenhum arquivo encontrado!"
                    
                    ultimo_acao = time.time()

                elif gesto == "DROP":
                    # Ação: DOWNLOAD
                    msg_status = "Verificando Nuvem..."
                    cor_status = (255, 0, 255) # Roxo
                    
                    cv2.putText(frame, "DROP DETECTADO!", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, cor_status, 2)
                    cam.mostrar_frame(frame)
                    cv2.waitKey(1)
                    
                    sucesso = cliente.baixar_arquivo(pasta_recebidos)
                    if sucesso:
                        msg_status = "Arquivo Baixado e Recortado!"
                        cor_status = (0, 255, 0)
                    else:
                        msg_status = "Nuvem Vazia ou Erro."
                    
                    ultimo_acao = time.time()
                else:
                    msg_status = "Aguardando..."
                    cor_status = (255, 255, 255)
            else:
                restante = int(COOLDOWN - (agora - ultimo_acao))
                msg_status = f"Aguarde {restante}s..."
                cor_status = (100, 100, 100)

            # Desenho
            detector.desenhar_landmarks(frame, resultados)
            cv2.putText(frame, f"Status: {msg_status}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor_status, 2)
            
            if gesto:
                cv2.putText(frame, f"Gesto: {gesto}", (10, 450), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            cam.mostrar_frame(frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        cam.liberar()
        sys.exit(0)

if __name__ == "__main__":
    main()