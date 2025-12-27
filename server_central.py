import socket
import threading
import os
import time
import struct
import shutil

# Configurações
HOST = '0.0.0.0'
PORT = 5001
STORAGE_DIR = 'nuvem_storage'
TIMEOUT_ARQUIVO = 90  # 1.5 minutos em segundos

def limpar_arquivos_antigos():
    """Thread que verifica periodicamente arquivos expirados."""
    while True:
        time.sleep(10) # Verifica a cada 10 segundos
        agora = time.time()
        if not os.path.exists(STORAGE_DIR):
            continue

        for nome_arquivo in os.listdir(STORAGE_DIR):
            caminho = os.path.join(STORAGE_DIR, nome_arquivo)
            if os.path.isfile(caminho):
                criacao = os.path.getmtime(caminho)
                idade = agora - criacao
                
                if idade > TIMEOUT_ARQUIVO:
                    try:
                        os.remove(caminho)
                        print(f"[Limpeza] Arquivo '{nome_arquivo}' expirou (>1.5m) e foi deletado.")
                    except Exception as e:
                        print(f"[Erro Limpeza] Não foi possível deletar {nome_arquivo}: {e}")

def handle_client(conn, addr):
    print(f"[Conexão] Novo cliente: {addr}")
    try:
        # Protocolo Simples: O cliente envia 1 byte indicando a ação
        # 'U' = Upload (Cliente enviando para servidor)
        # 'D' = Download (Cliente pedindo arquivo)
        
        acao = conn.recv(1).decode('utf-8')

        if acao == 'U': # UPLOAD (Grab)
            # 1. Receber tamanho do nome
            tamanho_nome_bin = conn.recv(4)
            if not tamanho_nome_bin: return
            tamanho_nome = struct.unpack("I", tamanho_nome_bin)[0]
            
            # 2. Nome do arquivo
            nome_arquivo = conn.recv(tamanho_nome).decode('utf-8')
            
            # 3. Tamanho do arquivo
            tamanho_arquivo_bin = conn.recv(8)
            tamanho_arquivo = struct.unpack("Q", tamanho_arquivo_bin)[0]
            
            print(f"[Upload] Recebendo '{nome_arquivo}' ({tamanho_arquivo} bytes)...")
            
            caminho_final = os.path.join(STORAGE_DIR, nome_arquivo)
            
            recebido = 0
            with open(caminho_final, "wb") as f:
                while recebido < tamanho_arquivo:
                    chunk = conn.recv(4096)
                    if not chunk: break
                    f.write(chunk)
                    recebido += len(chunk)
            
            print("[Upload] Concluído.")
            
        elif acao == 'D': # DOWNLOAD (Drop)
            # Pega o arquivo mais recente da pasta
            arquivos = [os.path.join(STORAGE_DIR, f) for f in os.listdir(STORAGE_DIR) 
                        if os.path.isfile(os.path.join(STORAGE_DIR, f))]
            
            if not arquivos:
                # Envia sinal de erro/vazio
                conn.send(b'E') # Empty
                print("[Download] Solicitação recebida, mas a nuvem está vazia.")
            else:
                conn.send(b'K') # OK
                # Pega o mais recente
                ultimo_arquivo = max(arquivos, key=os.path.getmtime)
                nome_arquivo = os.path.basename(ultimo_arquivo)
                tamanho_arquivo = os.path.getsize(ultimo_arquivo)
                
                print(f"[Download] Enviando '{nome_arquivo}' para o cliente...")
                
                # Envia metadados
                nome_bytes = nome_arquivo.encode('utf-8')
                conn.send(struct.pack("I", len(nome_bytes)))
                conn.send(nome_bytes)
                conn.send(struct.pack("Q", tamanho_arquivo))
                
                # Envia conteúdo
                with open(ultimo_arquivo, "rb") as f:
                    shutil.copyfileobj(f, conn.makefile('wb'))
                
                print("[Download] Enviado. Deletando da nuvem (Recortar)...")
                # Lógica de "Recortar": deleta após enviar
                os.remove(ultimo_arquivo)

    except Exception as e:
        print(f"[Erro] {e}")
    finally:
        conn.close()

def main():
    if not os.path.exists(STORAGE_DIR):
        os.makedirs(STORAGE_DIR)
        
    # Inicia thread de limpeza
    cleaner = threading.Thread(target=limpar_arquivos_antigos, daemon=True)
    cleaner.start()
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    
    print(f"=== SERVIDOR DE NUVEM AIRGESTURE ===")
    print(f"Rodando em {HOST}:{PORT}")
    print(f"Arquivos expiram em {TIMEOUT_ARQUIVO} segundos.")
    
    try:
        while True:
            conn, addr = server.accept()
            # Cria uma thread para cada cliente para não travar
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.start()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")

if __name__ == "__main__":
    main()