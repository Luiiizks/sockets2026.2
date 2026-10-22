import json
import socket

PORTA = 2048
TAMANHO_PAYLOAD = 4


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

        if valor == "":
            return 30

        try:
            tamanho = int(valor)

            if tamanho >= 30:
                return tamanho

            print("O tamanho deve ser no minimo 30.")

        except ValueError:
            print("Digite um numero inteiro.")


def calcular_checksum(texto):
    return sum(texto.encode()) % 256


def criar_pacotes(mensagem, janela):
    partes = [
        mensagem[i:i + TAMANHO_PAYLOAD]
        for i in range(0, len(mensagem), TAMANHO_PAYLOAD)
    ]

    pacotes = []

    for i, parte in enumerate(partes):
        pacote = {
            "tipo": "DADOS",
            "sequencia": i,
            "total": len(partes),
            "conteudo": parte,
            "checksum": calcular_checksum(parte),
            "fim_lote": (i + 1) % janela == 0 or i == len(partes) - 1,
            "fim_mensagem": i == len(partes) - 1
        }

        pacotes.append(pacote)

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

    return linha, buffer


def enviar_mensagem(cliente, modo, envio, tamanho_maximo, janela_servidor):
    mensagem = input("Digite a mensagem (ou 'sair' para encerrar): ")

    if mensagem.lower() == "sair":
        enviar_json(cliente, {"tipo": "ENCERRAR"})
        return False

    while not mensagem or len(mensagem) > tamanho_maximo:
        print(f"A mensagem deve ter entre 1 e {tamanho_maximo} caracteres.")
        mensagem = input("Digite a mensagem novamente: ")

    janela = janela_servidor if envio == "lote" else 1
    pacotes = criar_pacotes(mensagem, janela)

    print(f"Total de pacotes: {len(pacotes)}")

    buffer = ""

    for inicio in range(0, len(pacotes), janela):
        lote = pacotes[inicio:inicio + janela]

        for pacote in lote:
            enviar_json(cliente, pacote)

            print(
                f"Pacote enviado | "
                f"seq={pacote['sequencia']} | "
                f"conteudo='{pacote['conteudo']}' | "
                f"checksum={pacote['checksum']}"
            )

        quantidade_respostas = len(lote) if modo == "rs" else 1

        for _ in range(quantidade_respostas):
            linha, buffer = receber_linha(cliente, buffer)

            if linha is None:
                return False

            resposta = json.loads(linha)

            print(
                f"{resposta['tipo']} recebido | "
                f"seq={resposta['sequencia']} | "
                f"status={resposta['status']}"
            )

    return True


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect(("localhost", PORTA))

    print("Conectado ao servidor.")

    modo = escolher_modo()
    envio = escolher_envio()
    tamanho = escolher_tamanho()

    cliente.send(f"{modo},{envio},{tamanho}".encode())

    resposta = cliente.recv(256).decode().strip()

    print("Resposta do servidor:", resposta)

    if not resposta.startswith("Handshake OK"):
        cliente.close()
        return

    janela_servidor = int(resposta.split("janela=")[1])

    while enviar_mensagem(
        cliente,
        modo,
        envio,
        tamanho,
        janela_servidor
    ):
        print()

    cliente.close()


if __name__ == "__main__":
    main()