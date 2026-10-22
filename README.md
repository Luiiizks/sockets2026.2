# Projeto de Comunicação via Sockets

Trabalho prático da disciplina de **Infraestrutura de Redes e Comunicação**.

Após o primeiro e o segundo checkpoint, a aplicação realiza a comunicação entre cliente e servidor utilizando sockets TCP em Python, com handshake inicial e troca de mensagens em pacotes, considerando um canal sem erros ou perdas.

## Funcionalidades

Até o momento, foram implementados:

- conexão entre cliente e servidor via socket;
- handshake inicial;
- escolha do modo `gbn` ou `rs`;
- escolha entre envio `individual` ou `lote`;
- definição do tamanho máximo da mensagem;
- tamanho padrão de 30 caracteres;
- janela inicial definida pelo servidor com valor 5;
- divisão da mensagem em pacotes de até 4 caracteres;
- número de sequência em cada pacote;
- quantidade total de pacotes;
- checksum para verificação de integridade;
- envio dos pacotes em formato JSON;
- confirmação de recebimento com `ACK`;
- confirmação individual no modo `rs`;
- confirmação por lote no modo `gbn`;
- reconstrução da mensagem completa no servidor.

## Tecnologias

- Python 3
- Biblioteca `socket`
- Biblioteca `json`

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
3. tamanho máximo da mensagem;
4. mensagem que deseja enviar.

Caso nenhum tamanho seja informado, será utilizado o valor padrão de `30`.

Para encerrar a comunicação, digite:

```text
sair
```

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

## Pacotes

Após o handshake, a mensagem é dividida em pacotes com carga útil de até 4 caracteres.

Exemplo:

```text
Mensagem: teste final

Pacote 0: test
Pacote 1: e fi
Pacote 2: nal
```

Cada pacote possui informações como:

- número de sequência;
- quantidade total de pacotes;
- conteúdo;
- checksum;
- indicação de fim de lote;
- indicação de fim da mensagem.

Os pacotes são enviados em formato JSON.

Exemplo:

```json
{
  "tipo": "DADOS",
  "sequencia": 0,
  "total": 3,
  "conteudo": "test",
  "checksum": 192,
  "fim_lote": false,
  "fim_mensagem": false
}
```

## Modos de confirmação

- `gbn`: no envio em lote, o servidor envia uma confirmação ao final do lote;
- `rs`: o servidor envia uma confirmação individual para cada pacote recebido.

No envio `individual`, a janela utilizada é igual a 1.

## Próxima etapa

Na próxima entrega serão adicionados:

- simulação de erros;
- simulação de perdas;
- temporizador;
- retransmissão de pacotes;
- comportamento completo dos modos `gbn` e `rs`.

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
