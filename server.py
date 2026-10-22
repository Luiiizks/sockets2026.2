import json
import socket

PORTA = 2048
JANELA_INICIAL = 5


def calcular_checksum(texto):
    return sum(texto.encode()) % 256


def enviar_json(conexao, dados):
    conexao.sendall((json.dumps(dados) + "\n").encode())


def enviar_resposta(conexao, tipo, sequencia, status):
    enviar_json(conexao, {
        "tipo": tipo,
        "sequencia": sequencia,
        "status": status
    })


def reconstruir_mensagem(recebidos, total):
    if len(recebidos) != total:
        return None

    return "".join(recebidos[i] for i in range(total))


def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    servidor.bind(("0.0.0.0", PORTA))
    servidor.listen(1)

    print(f"Servidor aguardando conexao na porta {PORTA}...")

    conexao, endereco = servidor.accept()

    print(f"Cliente conectado: {endereco}")

    dados = conexao.recv(256).decode().strip()

    print("Handshake recebido:", dados)

    try:
        modo, envio, tamanho = dados.split(",")
        tamanho = int(tamanho)

        if modo not in ["gbn", "rs"]:
            resposta = "Erro: modo invalido"

        elif envio not in ["individual", "lote"]:
            resposta = "Erro: tipo de envio invalido"

        elif tamanho < 30:
            resposta = "Erro: tamanho maximo deve ser no minimo 30"

        else:
            resposta = (
                f"Handshake OK | modo={modo} | envio={envio} | "
                f"tamanho_max={tamanho} | janela={JANELA_INICIAL}"
            )

    except ValueError:
        resposta = "Erro ao interpretar handshake"

    conexao.send(resposta.encode())

    if not resposta.startswith("Handshake OK"):
        conexao.close()
        servidor.close()
        return

    buffer = ""
    recebidos = {}
    total_mensagem = 0

    while True:
        dados = conexao.recv(1024).decode()

        if not dados:
            break

        buffer += dados

        while "\n" in buffer:
            linha, buffer = buffer.split("\n", 1)

            if not linha.strip():
                continue

            pacote = json.loads(linha)

            if pacote["tipo"] == "ENCERRAR":
                print("Cliente encerrou a comunicacao.")

                conexao.close()
                servidor.close()

                return

            sequencia = pacote["sequencia"]
            conteudo = pacote["conteudo"]
            checksum = pacote["checksum"]
            total_mensagem = pacote["total"]

            print(
                f"Pacote recebido | "
                f"seq={sequencia} | "
                f"total={total_mensagem} | "
                f"conteudo='{conteudo}' | "
                f"checksum={checksum}"
            )

            if checksum != calcular_checksum(conteudo):
                enviar_resposta(conexao, "ERRO", sequencia, "checksum")
                continue

            recebidos[sequencia] = conteudo

            if modo == "rs":
                enviar_resposta(conexao, "ACK", sequencia, "ok")

            elif pacote["fim_lote"] or pacote["fim_mensagem"]:
                enviar_resposta(conexao, "ACK", sequencia, "ok")

            mensagem = reconstruir_mensagem(recebidos, total_mensagem)

            if mensagem is not None:
                print("Mensagem completa:", mensagem)

                recebidos = {}
                total_mensagem = 0

    conexao.close()
    servidor.close()


if __name__ == "__main__":
    main()