# Arquivo: rede/network_communication.py
import socket
import os
import struct

class ClienteNuvem:
    def __init__(self, ip_servidor, porta=5001):
        self.ip_servidor = ip_servidor
        self.porta = porta
        self.buffer_size = 4096

    def conectar(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.ip_servidor, self.porta))
            return s
        except Exception as e:
            print(f"[Rede] Erro ao conectar: {e}")
            return None

    def enviar_arquivo(self, caminho_arquivo):
        """UPLOAD: Pega o arquivo local e manda para a nuvem."""
        if not os.path.exists(caminho_arquivo):
            return False

        nome_arquivo = os.path.basename(caminho_arquivo)
        tamanho_arquivo = os.path.getsize(caminho_arquivo)

        s = self.conectar()
        if not s: return False
        
        try:
            # Protocolo 'U' para Upload
            s.send(b'U')
            
            # Metadados
            nome_bytes = nome_arquivo.encode('utf-8')
            s.send(struct.pack("I", len(nome_bytes)))
            s.send(nome_bytes)
            s.send(struct.pack("Q", tamanho_arquivo))
            
            # Dados
            with open(caminho_arquivo, "rb") as f:
                while True:
                    dados = f.read(self.buffer_size)
                    if not dados: break
                    s.send(dados)
            
            return True
        except Exception as e:
            print(f"[Upload] Erro: {e}")
            return False
        finally:
            s.close()

    def baixar_arquivo(self, pasta_destino):
        """DOWNLOAD: Solicita o arquivo da nuvem e salva localmente."""
        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        s = self.conectar()
        if not s: return False
        
        try:
            # Protocolo 'D' para Download
            s.send(b'D')
            
            # Verifica resposta (K = OK, E = Vazio)
            resp = s.recv(1)
            if resp == b'E':
                print("[Rede] Nuvem vazia.")
                return False
            elif resp != b'K':
                return False
                
            # Metadados
            tamanho_nome = struct.unpack("I", s.recv(4))[0]
            nome_arquivo = s.recv(tamanho_nome).decode('utf-8')
            tamanho_arquivo = struct.unpack("Q", s.recv(8))[0]
            
            caminho_final = os.path.join(pasta_destino, nome_arquivo)
            
            # Dados
            recebido = 0
            with open(caminho_final, "wb") as f:
                while recebido < tamanho_arquivo:
                    dados = s.recv(self.buffer_size)
                    if not dados: break
                    f.write(dados)
                    recebido += len(dados)
            
            print(f"[Rede] Arquivo baixado: {caminho_final}")
            return True
            
        except Exception as e:
            print(f"[Download] Erro: {e}")
            return False
        finally:
            s.close()