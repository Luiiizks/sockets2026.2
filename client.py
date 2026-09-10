import socket


PORTA = 2048


def escolher_modo():
    while True:
        modo = input("Escolha o modo (gbn/rs): ").strip().lower()

        if modo in ["gbn", "rs"]:
            return modo

        print("Modo invalido. Digite 'gbn' ou 'rs'.")


def escolher_envio():
    while True:
        envio = input("Escolha o envio (individual/lote): ").strip().lower()

        if envio in ["individual", "lote"]:
            return envio

        print("Opcao invalida. Digite 'individual' ou 'lote'.")


def escolher_tamanho():
    while True:
        valor = input("Digite o tamanho maximo da mensagem [30]: ").strip()

        # 30 é o valor padrão
        if valor == "":
            return 30

        try:
            tamanho = int(valor)

            if tamanho >= 30:
                return tamanho

            print("O tamanho deve ser no minimo 30.")

        except ValueError:
            print("Digite um numero inteiro valido.")


def main():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente.connect(("localhost", PORTA))
    print("Conectado ao servidor.")

    modo = escolher_modo()
    envio = escolher_envio()
    tamanho = escolher_tamanho()

    handshake = f"{modo},{envio},{tamanho}"

    cliente.send(handshake.encode())

    resposta = cliente.recv(256).decode()

    print("Resposta do servidor:")
    print(resposta)

    cliente.close()


if __name__ == "__main__":
    main()