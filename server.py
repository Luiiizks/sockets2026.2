import json
import socket
import sys

PORTA = 2048
JANELA_INICIAL = 5
CHAVE = "redes"


def calcular_checksum(texto):
    return sum(texto.encode()) % 256


def descriptografar(texto):
    dados = bytes.fromhex(texto)
    chave = CHAVE.encode()
    return bytes(dados[i] ^ chave[i % len(chave)] for i in range(len(dados))).decode()


def enviar_json(conexao, dados):
    conexao.sendall((json.dumps(dados) + "\n").encode())


def enviar_resposta(conexao, tipo, sequencia, status):
    enviar_json(conexao, {"tipo": tipo, "sequencia": sequencia, "status": status})


def reconstruir_mensagem(recebidos, total):
    if len(recebidos) != total:
        return None
    return "".join(recebidos[i] for i in range(total))


def main():
    janela = int(sys.argv[1]) if len(sys.argv) > 1 else JANELA_INICIAL
    if not 1 <= janela <= 5:
        print("A janela deve estar entre 1 e 5.")
        return

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
            resposta = f"Handshake OK | modo={modo} | envio={envio} | tamanho_max={tamanho} | janela={janela}"
    except ValueError:
        resposta = "Erro ao interpretar handshake"

    conexao.sendall(resposta.encode())
    if not resposta.startswith("Handshake OK"):
        conexao.close()
        servidor.close()
        return

    buffer = ""
    recebidos = {}
    esperado = 0
    total_mensagem = 0
    descartando_lote = False

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

            seq = pacote["sequencia"]
            total_mensagem = pacote["total"]
            try:
                conteudo = descriptografar(pacote["conteudo"])
            except (ValueError, UnicodeDecodeError):
                conteudo = ""
            print(f"Pacote recebido | seq={seq} | total={total_mensagem} | conteudo='{conteudo}' | checksum={pacote['checksum']}")

            if modo == "gbn" and descartando_lote:
                if pacote["fim_lote"]:
                    descartando_lote = False
                continue

            if calcular_checksum(conteudo) != pacote["checksum"]:
                enviar_resposta(conexao, "ERRO", seq, "checksum")
                if modo == "gbn" and not pacote["fim_lote"]:
                    descartando_lote = True
                continue

            if modo == "rs":
                recebidos[seq] = conteudo
                enviar_resposta(conexao, "ACK", seq, "ok")
            else:
                if seq == esperado:
                    recebidos[seq] = conteudo
                    esperado += 1
                    if pacote["fim_lote"]:
                        enviar_resposta(conexao, "ACK", seq, "ok")
                elif seq > esperado:
                    enviar_resposta(conexao, "ERRO", esperado, "fora_de_ordem")
                    if not pacote["fim_lote"]:
                        descartando_lote = True
                elif pacote["fim_lote"]:
                    enviar_resposta(conexao, "ACK", esperado - 1, "ok")

            mensagem = reconstruir_mensagem(recebidos, total_mensagem)
            if mensagem is not None:
                print("Mensagem completa:", mensagem)
                recebidos = {}
                esperado = 0
                total_mensagem = 0
                descartando_lote = False

    conexao.close()
    servidor.close()


if __name__ == "__main__":
    main()
