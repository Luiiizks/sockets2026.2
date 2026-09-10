import socket

PORTA = 2048
JANELA_INICIAL = 5

def main():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("0.0.0.0", PORTA))
    servidor.listen(1)

    print(f"Servidor aguardando conexao na porta {PORTA}...")

    conexao, endereco = servidor.accept()

    print(f"Cliente conectado: {endereco}")

    dados = conexao.recv(256).decode().strip()

    print(f"Handshake recebido: {dados}")

    try:
        modo, envio, tamanho = dados.split(",")
        tamanho = int(tamanho)

        if modo not in ["gbn", "rs"]:
            resposta = "Erro modo invalido"

        elif envio not in ["individual", "lote"]:
            resposta = "Erro tipo de envio invalido"

        elif tamanho < 30:
            resposta = "Erro: tamanho maximo deve ser no minimo 30"

        else:
            resposta = (
                f"Handshake OK | "
                f"modo={modo} | "
                f"envio={envio} | "
                f"tamanho_max={tamanho} | "
                f"janela={JANELA_INICIAL}"
            )

    except ValueError:
        resposta = "Erro ao interpretar handshake"

    conexao.send(resposta.encode())
    conexao.close()
    servidor.close()


if __name__ == "__main__":
    main()