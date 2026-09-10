# Projeto de Comunicação via Sockets

Trabalho prático da disciplina de **Infraestrutura de Redes e Comunicação**.

Nesta primeira etapa, foi implementada a comunicação básica entre cliente e servidor utilizando sockets TCP em Python, com foco no handshake inicial.

## Funcionalidades

- conexão entre cliente e servidor via socket;
- escolha do modo `gbn` ou `rs`;
- escolha entre envio `individual` ou `lote`;
- definição do tamanho máximo da mensagem;
- tamanho padrão de 30 caracteres;
- janela inicial definida pelo servidor com valor 5.

## Tecnologias

- Python 3
- Biblioteca `socket`

## Arquivos

```text
client.py
server.py
README.md
```

## Como executar

Primeiro, execute o servidor:

```bash
python3 server.py
```

Depois, em outro terminal, execute o cliente:

```bash
python3 client.py
```

No cliente, escolha:

1. modo de operação (`gbn` ou `rs`);
2. tipo de envio (`individual` ou `lote`);
3. tamanho máximo da mensagem.

Caso nenhum tamanho seja informado, será utilizado o valor padrão de `30`.

## Handshake

O cliente envia:

```text
modo,envio,tamanho_maximo
```

Exemplo:

```text
gbn,lote,30
```

O servidor responde:

```text
Handshake OK | modo=gbn | envio=lote | tamanho_max=30 | janela=5
```

## Próximas etapas

Nas próximas entregas serão adicionados o envio de mensagens, fragmentação em pacotes, confirmações, retransmissão e simulação de erros e perdas.

## Equipe

- Gabriel Pontes
- Gabriel Roma
- Gabriel Victor
- João Pedro Silva Barbosa
- Joel Costa Oliveira
- Kaique Alves
- Luiz Flavius
- Mell Brayner
- Pedro Henrique Ramos
