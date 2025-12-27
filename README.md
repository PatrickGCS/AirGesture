# AirGesture
Sistema experimental de transferência de arquivos por gestos, utilizando visão computacional com MediaPipe e comunicação em rede, permitindo enviar arquivos entre notebooks de forma intuitiva, sem cabos ou interfaces tradicionais.

**Projeto: Transferência de Arquivos por Gestos com MediaPipe e Python**

**Objetivo:**
Desenvolver um sistema inovador de transferência de arquivos entre dispositivos em uma rede local, utilizando gestos capturados pela câmera do notebook. O sistema permitirá que um usuário, ao realizar um gesto específico, envie um arquivo de forma intuitiva para outro dispositivo na mesma rede.

**Tecnologias Utilizadas:**

* **Linguagem de Programação:** Python
* **Bibliotecas de Visão Computacional:** MediaPipe (para detecção de gestos e poses) e OpenCV (para captura de vídeo e processamento de imagem).
* **Comunicação em Rede:** Sockets TCP/IP ou HTTP para transferência de arquivos.

**Estrutura do Projeto:**

1. **Diretório Principal:**

   * `main.py`: Script principal que inicializa e gerencia o sistema.

2. **Pasta `scripts`:**

   * `gesture_detection.py`: Módulo responsável por capturar e interpretar os gestos usando MediaPipe.
   * `video_capture.py`: Módulo para capturar o vídeo da câmera do notebook.

3. **Pasta `rede`:**

   * `network_communication.py`: Módulo para gerenciar a comunicação entre os dispositivos e a transferência de arquivos.

4. **Pasta `modelos`:**

   * Modelos treinados do MediaPipe para detecção de gestos, já integrados.

5. **Pasta `utils`:**

   * Funções auxiliares para manipulação de arquivos, conversão de dados e outros utilitários.

**Funcionamento:**

1. O usuário executa o script em seu notebook.
2. A câmera do notebook captura o vídeo em tempo real.
3. O módulo de detecção de gestos, usando MediaPipe, identifica o gesto realizado pelo usuário.
4. Ao identificar o gesto de transferência, o dispositivo receptor é determinado (por exemplo, através de um identificador de rede ou IP).
5. O arquivo é transferido de forma automática para o dispositivo alvo, concluindo o processo.

**Benefícios:**

* Interação intuitiva e rápida, sem a necessidade de cabos ou interfaces complicadas.
* Facilidade de uso em ambientes corporativos, melhorando a produtividade.

