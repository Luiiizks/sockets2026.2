# Relatório – Checkpoint 2

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

O objetivo deste segundo checkpoint é permitir a troca de mensagens entre cliente e servidor considerando um canal sem erros ou perdas.

Nesta etapa, o protocolo de aplicação foi ampliado para permitir a divisão da mensagem em pacotes, envio dos dados, confirmação de recebimento e reconstrução da mensagem no servidor.

---

## 2. Funcionalidades implementadas

Nesta etapa foram implementados:

- manutenção do handshake desenvolvido no primeiro checkpoint;
- divisão da mensagem em pacotes de até 4 caracteres;
- número de sequência;
- quantidade total de pacotes;
- checksum;
- envio dos pacotes em formato JSON;
- envio individual ou em lote;
- confirmação por `ACK`;
- confirmação individual no modo `rs`;
- confirmação por lote no modo `gbn`;
- reconstrução da mensagem original no servidor.

Nesta etapa não são simulados erros ou perdas.

---

## 3. Protocolo de aplicação

O handshake continua utilizando o formato:

```text
modo,envio,tamanho_maximo
```

Exemplo:

```text
gbn,lote,30
```

Após o handshake, os dados são enviados em pacotes no formato JSON.

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

Cada pacote possui uma carga útil de no máximo 4 caracteres.

O campo `sequencia` indica a posição do pacote e o campo `total` informa a quantidade total de pacotes da mensagem.

O `checksum` é utilizado para verificar a integridade do conteúdo recebido.

---

## 4. Funcionamento

O funcionamento da aplicação nesta etapa ocorre da seguinte forma:

1. o servidor é iniciado;
2. o cliente conecta ao servidor;
3. ocorre o handshake inicial;
4. o usuário digita a mensagem;
5. a mensagem é dividida em pacotes de até 4 caracteres;
6. os pacotes são enviados ao servidor;
7. o servidor imprime os metadados recebidos;
8. o servidor responde com `ACK`;
9. ao receber todos os pacotes, o servidor reconstrói e imprime a mensagem completa.

No modo `rs`, o servidor confirma cada pacote individualmente.

No modo `gbn`, durante o envio em lote, o servidor envia uma confirmação ao final do lote.

---

## 5. Como executar

Primeiro, execute o servidor:

```bash
python3 server.py
```

Em outro terminal:

```bash
python3 client.py
```

No cliente, informe:

1. modo `gbn` ou `rs`;
2. envio `individual` ou `lote`;
3. tamanho máximo da mensagem;
4. mensagem desejada.

Exemplo:

```text
Escolha o modo (gbn/rs): gbn
Escolha o envio (individual/lote): lote
Digite o tamanho maximo da mensagem [30]: 30
Digite a mensagem: teste final
```

O servidor deverá receber os pacotes e, ao final, apresentar:

```text
Mensagem completa: teste final
```

Para encerrar, digite:

```text
sair
```

---

## 6. Uso de Inteligência Artificial

Nesta etapa, a Inteligência Artificial foi utilizada como ferramenta de apoio para:

- pesquisar e revisar conceitos relacionados ao protocolo cliente-servidor;
- auxiliar na organização dos requisitos do segundo checkpoint;
- revisar a estrutura do protocolo de aplicação;
- organizar a atualização do README;
- auxiliar na estruturação do relatório.

As informações utilizadas foram revisadas antes de serem incorporadas à documentação.

### Principais prompts utilizados

> “No segundo checkpoint, como deve funcionar o envio dos pacotes quando ainda não existem erros e perdas?”

> “Como posso testar se o envio individual e o envio em lote estão funcionando corretamente?”

> “Ajude a atualizar o README para representar as funcionalidades do segundo checkpoint.”

> “Ajude a estruturar o relatório do segundo checkpoint de forma simples e objetiva.”

---

## 7. Próxima etapa

No próximo checkpoint serão implementadas a simulação de erros e perdas, temporizador e retransmissão dos pacotes de acordo com o modo de operação escolhido.
