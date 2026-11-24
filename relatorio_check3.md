# Relatório – Checkpoint 3

## Comunicação Cliente-Servidor via Sockets

### Disciplina

Infraestrutura de Redes e Comunicação

### Integrantes

- Gabriel Pontes
- Gabriel Roma
- Gabriel Victor
- João Pedro Silva Barbosa
- Joel Costa Oliveira
- Kaique Alves
- Luiz Flavius
- Mell Brayner
- Pedro Henrique Ramos

---

## 1. Objetivo

O objetivo deste terceiro checkpoint é implementar a simulação de erros e perdas na comunicação entre cliente e servidor, além dos mecanismos necessários para garantir a transmissão correta das mensagens.

Nesta etapa, foram adicionados temporizador, retransmissão e tratamento de falhas nos modos Go-Back-N (GBN) e Repetição Seletiva (RS).

## 2. Funcionalidades implementadas

Nesta etapa foram implementados:

- simulação determinística de erros e perdas;
- temporizador para aguardar confirmações;
- retransmissão de pacotes;
- tratamento de erros com respostas `ERRO`;
- controle de retransmissão nos modos `gbn` e `rs`;
- criptografia simétrica simples;
- manutenção do checksum para verificação de integridade.

As funcionalidades dos checkpoints anteriores foram mantidas.

## 3. Protocolo de aplicação

O protocolo continua utilizando o handshake inicial e pacotes em formato JSON, com carga útil original de até 4 caracteres.

Cada pacote possui número de sequência, conteúdo criptografado, checksum e informações de controle.

O servidor verifica os pacotes recebidos e envia respostas de confirmação (`ACK`) ou de erro (`ERRO`).

No modo `gbn`, o cliente retransmite a partir do pacote com problema. No modo `rs`, são retransmitidos apenas os pacotes que ainda não foram confirmados.

## 4. Simulação de erros e perdas

A simulação é realizada no cliente, permitindo escolher quais pacotes apresentarão falhas.

- **Erro:** oo conteúdo criptografado do pacote é alterado na primeira tentativa, mantendo o checksum original.
- **Perda:** o pacote escolhido deixa de ser enviado na primeira tentativa.

Caso uma confirmação não seja recebida dentro do tempo definido, o cliente realiza a retransmissão.

As falhas são determinísticas, pois os pacotes são escolhidos pelo usuário.

## 5. Pontos extras

Foram implementados dois recursos adicionais:

- **Checksum:** cálculo manual da soma dos bytes do conteúdo, utilizando módulo 256 para verificar a integridade.
- **Criptografia simétrica:** utilização de uma chave compartilhada entre cliente e servidor, aplicando a operação XOR para criptografar e descriptografar as mensagens.

Os dois algoritmos foram implementados sem bibliotecas externas específicas.

## 6. Como executar

Primeiro, execute o servidor:

```bash
python3 server.py
```

Em outro terminal, execute o cliente:

```bash
python3 client.py
```

No cliente:

1. escolha o modo `gbn` ou `rs`;
2. escolha o envio `individual` ou `lote`;
3. informe o tamanho máximo da mensagem;
4. digite a mensagem desejada;
5. escolha se deseja simular erro ou perda;
6. informe o número dos pacotes que apresentarão falhas.

Para não simular uma das falhas, utilize `-1` na seleção do pacote correspondente.

Para encerrar a comunicação, digite `sair`.

## 7. Testes

Foram verificados os seguintes cenários:

- envio sem erros e perdas;
- envio individual e em lote;
- comunicação nos modos GBN e RS;
- erro de integridade;
- perda de pacote;
- erro e perda na mesma transmissão;
- retransmissão e reconstrução da mensagem original.

Nos cenários testados, o servidor conseguiu reconstruir corretamente as mensagens após as retransmissões necessárias.

## 8. Uso de Inteligência Artificial

Nesta etapa, a Inteligência Artificial foi utilizada como ferramenta de apoio para:

- pesquisa e revisão de conceitos relacionados a erros, perdas e retransmissão;
- organização dos requisitos da entrega final;
- revisão e testes do funcionamento da aplicação;
- organização do README e do relatório.

As sugestões foram analisadas e o funcionamento foi verificado por meio de testes.

### Principais prompts utilizados

> “Como funciona a retransmissão de pacotes nos modos Go-Back-N e Repetição Seletiva quando ocorre perda?”

> “Quais testes posso realizar para verificar erros, perdas e retransmissões na comunicação?”

> “Ajude a atualizar o README com as funcionalidades da entrega final.”

> “Ajude a estruturar o relatório do terceiro checkpoint de forma simples e objetiva.”

## 9. Conclusão

Com a implementação das funcionalidades desta etapa, a aplicação passou a simular falhas de comunicação e realizar retransmissões conforme o modo escolhido.

Assim, o projeto reúne os mecanismos de confiabilidade solicitados, além das funcionalidades desenvolvidas nos checkpoints anteriores.
