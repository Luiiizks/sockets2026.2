# Projeto de Comunicação via Sockets

Trabalho prático da disciplina de **Infraestrutura de Redes e Comunicação**.

Após os três checkpoints, a aplicação realiza a comunicação entre cliente e servidor utilizando sockets TCP em Python, com handshake inicial, envio de mensagens em pacotes e mecanismos de controle de erros, perdas e retransmissões.

## Funcionalidades

- Conexão entre cliente e servidor via sockets TCP;
- escolha do modo `gbn` (Go-Back-N) ou `rs` (Repetição Seletiva);
- escolha entre envio `individual` ou `lote`;
- tamanho máximo da mensagem configurável, com padrão de 30 caracteres;
- janela inicial de 5 pacotes definida pelo servidor;
- divisão das mensagens em pacotes de até 4 caracteres;
- envio de pacotes em formato JSON;
- confirmação de recebimento com `ACK` e sinalização de erro com `ERRO`;
- reconstrução da mensagem original no servidor;
- simulação de erros e perdas de pacotes;
- temporizador e retransmissão nos modos GBN e RS;
- verificação de integridade com checksum;
- criptografia simétrica simples utilizando XOR.

## Tecnologias

- Python 3
- Biblioteca `socket`
- Biblioteca `json`

## Arquivos

```text
client.py
server.py
README.md
relatorio-checkpoint1.md
relatorio-checkpoint2.md
relatorio-checkpoint3.md
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

1. Modo de operação (`gbn` ou `rs`);
2. tipo de envio (`individual` ou `lote`);
3. tamanho máximo da mensagem;
4. mensagem que deseja enviar;
5. se deseja simular erros ou perdas.

Caso nenhum tamanho seja informado, será utilizado o valor padrão de `30`.

Para simular falhas, informe o número do pacote desejado, começando em `0`. Utilize `-1` caso não queira simular determinado tipo de falha.

Para encerrar a comunicação, digite `sair`.

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

## Protocolo de comunicação

As mensagens são divididas em pacotes com carga útil original de até 4 caracteres.

Cada pacote possui metadados como número de sequência, total de pacotes, conteúdo, checksum e informações de controle.

Exemplo de pacote:

```json
{
  "tipo": "DADOS",
  "sequencia": 0,
  "total": 3,
  "conteudo": "hexadecimal",
  "checksum": 192,
  "fim_lote": false,
  "fim_mensagem": false
}
```

O campo `conteudo` transporta os dados criptografados em hexadecimal.

O servidor responde utilizando `ACK` para confirmações ou `ERRO` quando identifica uma falha.

## Modos de transmissão

**Go-Back-N (GBN):** trabalha com confirmações acumuladas e, quando necessário, retransmite a partir do pacote com problema.

**Repetição Seletiva (RS):** confirma os pacotes individualmente e retransmite apenas os que continuam pendentes.

No envio em lote, o cliente utiliza a janela informada pelo servidor. No envio individual, utiliza uma janela de tamanho 1.

## Simulação de erros e perdas

A aplicação permite simular falhas de forma determinística:

- **Erro:** o conteúdo criptografado do pacote escolhido é alterado na primeira transmissão, provocando uma falha de integridade.
- **Perda:** o pacote escolhido não é enviado na primeira tentativa.

O cliente utiliza um temporizador de `2,5 segundos` para aguardar as confirmações e realizar retransmissões quando necessário.

## Checksum e criptografia

O checksum é calculado manualmente por meio da soma dos bytes do conteúdo, utilizando módulo 256.

A criptografia utiliza uma operação XOR com uma chave compartilhada entre cliente e servidor. A implementação tem finalidade educacional.

## Testes

Foram realizados testes com:

- GBN e RS;
- envio individual e em lote;
- mensagens sem falhas;
- erro de integridade;
- perda de pacotes;
- erro e perda combinados;
- retransmissão e reconstrução da mensagem original.

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
