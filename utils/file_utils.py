# Arquivo: utils/file_utils.py
import os
import glob

PASTA_ORIGEM_PADRAO = "AirGesture_Source"

def preparar_pastas():
    if not os.path.exists(PASTA_ORIGEM_PADRAO):
        os.makedirs(PASTA_ORIGEM_PADRAO)
        # Cria um arquivo de exemplo para não falhar no primeiro teste
        with open(os.path.join(PASTA_ORIGEM_PADRAO, "documento_exemplo.txt"), "w") as f:
            f.write("Conteudo importante capturado pelo gesto!")

def obter_ultimo_arquivo_modificado(pasta=PASTA_ORIGEM_PADRAO):
    """
    Simula 'pegar o arquivo ativo'. Retorna o caminho do arquivo 
    mais recentemente modificado na pasta monitorada.
    """
    arquivos = glob.glob(os.path.join(pasta, "*"))
    if not arquivos:
        return None
    
    # Ordena por data de modificação e pega o último
    ultimo = max(arquivos, key=os.path.getmtime)
    return ultimo