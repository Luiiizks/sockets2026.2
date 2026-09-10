# Relatório – Checkpoint 1

## Comunicação Cliente-Servidor via Sockets

### Disciplina

Infraestrutura de Redes e Comunicação

---

## 1. Objetivo

O objetivo deste primeiro checkpoint é estabelecer uma comunicação entre cliente e servidor utilizando sockets e realizar o handshake inicial da aplicação.

Durante o handshake são definidos os parâmetros básicos que serão utilizados nas próximas etapas do projeto.

---

## 2. Funcionalidades implementadas

Nesta etapa foram implementados:

- conexão entre cliente e servidor via socket TCP;
- escolha do modo de operação (`gbn` ou `rs`);
- escolha entre envio `individual` ou em `lote`;
- definição do tamanho máximo da mensagem;
- utilização de 30 caracteres como tamanho padrão;
- definição da janela inicial pelo servidor, com valor 5;
- validação das informações enviadas no handshake.

---

## 3. Protocolo do handshake

O cliente envia os parâmetros iniciais utilizando o seguinte formato:

```text
modo,envio,tamanho_maximo
```

Exemplo:

```text
gbn,lote,30
```

O servidor recebe os valores, realiza as validações e retorna uma confirmação contendo também o tamanho da janela.

Exemplo:

```text
Handshake OK | modo=gbn | envio=lote | tamanho_max=30 | janela=5
```

Neste checkpoint, os modos GBN e Repetição Seletiva são apenas definidos durante o handshake. O funcionamento completo desses modos será implementado nas próximas etapas.

---

## 4. Como executar

Primeiro, execute o servidor:

```bash
python3 server.py
```

Em outro terminal, execute o cliente:

```bash
python3 client.py
```

No cliente, serão solicitados:

1. modo de operação;
2. tipo de envio;
3. tamanho máximo da mensagem.

Caso nenhum tamanho seja informado, o valor padrão utilizado será 30.

---

## 5. Uso de Inteligência Artificial

Nesta etapa, a Inteligência Artificial foi utilizada como ferramenta de apoio para:

- auxiliar na interpretação e organização dos requisitos;
- pesquisar conceitos e exemplos relacionados a sistemas cliente-servidor;
- auxiliar na organização do README e do relatório;
- revisar a estrutura geral da solução.

As informações utilizadas foram revisadas antes de serem incorporadas ao projeto.

### Principais prompts utilizados

> “Quais são os requisitos necessários para o primeiro checkpoint de uma aplicação cliente-servidor utilizando sockets?”

> “Pesquise e explique de forma simples como funciona um handshake entre cliente e servidor.”

> “Ajude a organizar um README com instruções de execução para uma aplicação cliente-servidor em Python.”

> “Ajude a estruturar o relatório do primeiro checkpoint de forma simples e objetiva.”

---

## 6. Próxima etapa

No próximo checkpoint, o projeto será ampliado para permitir a troca de mensagens entre cliente e servidor sem a ocorrência de erros ou perdas.
