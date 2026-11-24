import json
import socket

PORTA = 2048
TAMANHO_PAYLOAD = 4
TIMEOUT = 2.5
CHAVE = "redes"


def escolher_modo():
    while True:
        modo = input("Escolha o modo (gbn/rs): ").strip().lower()
        if modo in ["gbn", "rs"]:
            return modo
        print("Modo invalido.")


def escolher_envio():
    while True:
        envio = input("Escolha o envio (individual/lote): ").strip().lower()
        if envio in ["individual", "lote"]:
            return envio
        print("Opcao invalida.")


def escolher_tamanho():
    while True:
        valor = input("Digite o tamanho maximo da mensagem [30]: ").strip()
        if not valor:
            return 30
        try:
            tamanho = int(valor)
            if tamanho >= 30:
                return tamanho
        except ValueError:
            pass
        print("Digite um numero inteiro maior ou igual a 30.")


def calcular_checksum(texto):
    return sum(texto.encode()) % 256


def criptografar(texto):
    dados = texto.encode()
    chave = CHAVE.encode()
    return bytes(dados[i] ^ chave[i % len(chave)] for i in range(len(dados))).hex()


def criar_pacotes(mensagem):
    partes = [mensagem[i:i + TAMANHO_PAYLOAD] for i in range(0, len(mensagem), TAMANHO_PAYLOAD)]
    pacotes = []
    for i, parte in enumerate(partes):
        pacotes.append({
            "tipo": "DADOS", "sequencia": i, "total": len(partes),
            "conteudo": criptografar(parte), "checksum": calcular_checksum(parte),
            "fim_lote": False, "fim_mensagem": i == len(partes) - 1
        })
    return pacotes


def enviar_json(conexao, dados):
    conexao.sendall((json.dumps(dados) + "\n").encode())


def receber_linha(conexao, buffer):
    while "\n" not in buffer:
        dados = conexao.recv(1024).decode()
        if not dados:
            return None, buffer
        buffer += dados
    linha, buffer = buffer.split("\n", 1)
    return json.loads(linha), buffer


def escolher_falha(pergunta, total):
    while True:
        try:
            numero = int(input(pergunta))
            if numero == -1 or 0 <= numero < total:
                return numero
        except ValueError:
            pass
        print("Digite -1 ou um numero de pacote valido.")


def enviar_pacote(cliente, pacote, erro, perda, tentativas, fim_lote):
    seq = pacote["sequencia"]
    tentativas[seq] += 1
    if seq == perda and tentativas[seq] == 1:
        print(f"Perda simulada | seq={seq}")
        return

    envio = pacote.copy()
    envio["fim_lote"] = fim_lote
    if seq == erro and tentativas[seq] == 1:
        alterado = bytearray.fromhex(pacote["conteudo"])
        alterado[0] ^= 1
        envio["conteudo"] = alterado.hex()
        print(f"Erro simulado | seq={seq}")

    enviar_json(cliente, envio)
    print(f"Pacote enviado | seq={seq} | checksum={envio['checksum']} | tentativa={tentativas[seq]}")


def enviar_gbn(cliente, pacotes, janela, erro, perda):
    base = 0
    buffer = ""
    tentativas = [0] * len(pacotes)
    while base < len(pacotes):
        fim = min(base + janela, len(pacotes))
        for i in range(base, fim):
            enviar_pacote(cliente, pacotes[i], erro, perda, tentativas, i == fim - 1)
        try:
            resposta, buffer = receber_linha(cliente, buffer)
        except socket.timeout:
            print(f"Timeout | reenviando a partir do pacote {base}")
            continue
        if resposta is None:
            return False
        print(f"{resposta['tipo']} recebido | seq={resposta['sequencia']} | status={resposta['status']}")
        if resposta["tipo"] == "ACK":
            base = max(base, resposta["sequencia"] + 1)
        else:
            base = max(base, resposta["sequencia"])
    return True


def enviar_rs(cliente, pacotes, janela, erro, perda):
    pendentes = set(range(len(pacotes)))
    tentativas = [0] * len(pacotes)
    buffer = ""
    while pendentes:
        inicio = min(pendentes)
        grupo = [i for i in range(inicio, min(inicio + janela, len(pacotes))) if i in pendentes]
        for i in grupo:
            enviar_pacote(cliente, pacotes[i], erro, perda, tentativas, i == grupo[-1])
        esperando = set(grupo)
        while esperando:
            try:
                resposta, buffer = receber_linha(cliente, buffer)
            except socket.timeout:
                print("Timeout | reenviando pacotes pendentes")
                break
            if resposta is None:
                return False
            seq = resposta["sequencia"]
            print(f"{resposta['tipo']} recebido | seq={seq} | status={resposta['status']}")
            if resposta["tipo"] == "ACK":
                pendentes.discard(seq)
            esperando.discard(seq)
    return True


def enviar_mensagem(cliente, modo, envio, tamanho, janela_servidor):
    mensagem = input("Digite a mensagem (ou 'sair' para encerrar): ")
    if mensagem.strip().lower() == "sair":
        enviar_json(cliente, {"tipo": "ENCERRAR"})
        return False
    while not mensagem or len(mensagem) > tamanho:
        print(f"A mensagem deve ter entre 1 e {tamanho} caracteres.")
        mensagem = input("Digite a mensagem novamente: ")

    janela = janela_servidor if envio == "lote" else 1
    pacotes = criar_pacotes(mensagem)
    print(f"Total de pacotes: {len(pacotes)}")
    if input("Simular erro/perda? (s/n): ").strip().lower() == "s":
        erro = escolher_falha("Pacote com erro (-1 para nenhum): ", len(pacotes))
        perda = escolher_falha("Pacote perdido (-1 para nenhum): ", len(pacotes))
        while erro != -1 and perda == erro:
            print("Escolha pacotes diferentes para erro e perda.")
            perda = escolher_falha("Pacote perdido (-1 para nenhum): ", len(pacotes))
    else:
        erro, perda = -1, -1

    cliente.settimeout(TIMEOUT)
    if modo == "gbn":
        return enviar_gbn(cliente, pacotes, janela, erro, perda)
    return enviar_rs(cliente, pacotes, janela, erro, perda)


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", PORTA))
    print("Conectado ao servidor.")
    modo = escolher_modo()
    envio = escolher_envio()
    tamanho = escolher_tamanho()
    cliente.sendall(f"{modo},{envio},{tamanho}".encode())
    resposta = cliente.recv(256).decode().strip()
    print("Resposta do servidor:", resposta)
    if not resposta.startswith("Handshake OK"):
        cliente.close()
        return
    janela = int(resposta.split("janela=")[1])
    while enviar_mensagem(cliente, modo, envio, tamanho, janela):
        print()
    cliente.close()


if __name__ == "__main__":
    main()
