import subprocess
import time
import sys
import os

def main():
    print("=== MODO DE TESTE LOCAL (LOCALHOST) ===")
    print("Este script irá rodar o Servidor e o Cliente na mesma máquina.")
    
    # Caminhos para garantir que o Python encontre os arquivos
    server_script = "server_central.py"
    client_script = "main.py"
    
    if not os.path.exists(server_script) or not os.path.exists(client_script):
        print(f"Erro: Certifique-se de que {server_script} e {client_script} estão nesta pasta.")
        return

    # 1. Iniciar o Servidor (em processo separado / background)
    print(f"\n[1] Iniciando Servidor Local (Nuvem)...")
    # sys.executable garante que usamos o mesmo Python que está rodando este script
    processo_servidor = subprocess.Popen(
        [sys.executable, server_script],
        cwd=os.getcwd(),
        shell=False # False é mais seguro para fechar o processo depois
    )
    
    # Dá um tempo para o servidor iniciar e abrir a porta 5001
    time.sleep(2)
    
    # 2. Iniciar o Cliente
    print(f"[2] Iniciando Cliente AirGesture...")
    print("    -> Conectando em 127.0.0.1 (Localhost)")
    print("    -> Pressione 'q' na janela da câmera para encerrar tudo.\n")
    
    try:
        # Roda o cliente e espera ele fechar (bloqueia o script aqui)
        subprocess.run(
            [sys.executable, client_script, "--server-ip", "127.0.0.1"],
            check=True
        )
    except KeyboardInterrupt:
        print("\nInterrupção detectada...")
    except Exception as e:
        print(f"\nErro ao rodar cliente: {e}")
    finally:
        # 3. Limpeza ao fechar
        print("\n[3] Encerrando Servidor Local...")
        processo_servidor.terminate()
        # Em Windows, às vezes terminate() não mata subprocessos filhos imediatamente,
        # mas para scripts python simples costuma funcionar.
        processo_servidor.wait()
        print("Teste finalizado. Até logo!")

if __name__ == "__main__":
    main()