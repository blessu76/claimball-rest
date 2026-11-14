---
title: Celulares pequenos, texto grande e uma rede de segurança
description: Antes de avançar, verificamos as telas do Claimball em um celular estreito com texto grande e adicionamos uma rede de segurança para que um arquivo com problema não pare o app.
summary: Antes de avançar, verificamos o menu, as estatísticas e o ranking do Claimball em um celular estreito com o texto ampliado em 50 por cento, em inglês, árabe e coreano. Também adicionamos um protetor global de erros e um valor seguro de reserva para que o app continue abrindo se um item salvo não puder ser lido. Ainda está em testes e chega em breve ao iOS e ao Android.
slug: small-screens-and-safety-nets
lang: pt-BR
category: devlog
translation_of: en
keywords: Claimball, acessibilidade, telas pequenas, confiabilidade, diário
copy_review: iris 2026-11-14
---
Um jogo que abre mal ou corta o próprio texto não é divertido, por melhores que sejam as regras. Esta é uma rodada de verificações nas builds de teste interno do TestFlight, que ainda não foram lançadas ao público.

## Telas estreitas, texto grande

Testamos o menu, a tela de histórico e a tela de ranking na largura de um celular estreito com o texto ampliado em 50 por cento, em inglês, árabe e coreano, e garantimos que nada transborde nem se sobreponha.

## Uma rede de segurança para erros

Se algo inesperado der errado, um protetor global de erros o captura em vez de deixar o app cair.

## Abre mesmo que um salvamento não possa ser lido

Se um item salvo não puder ser lido na inicialização, o jogo recorre a um valor padrão seguro para esse item e abre mesmo assim, em vez de parar numa tela em branco.

## Traduções

Uma verificação de tradução roda a cada build e aponta textos faltando ou quebrados. As traduções em si foram feitas com IA e ainda não foram revisadas por falantes nativos.

## O que vem a seguir

O Claimball ainda está em testes e chega em breve ao iOS e ao Android. Ainda não há data de lançamento.

## Perguntas frequentes

### Como vocês verificam telas pequenas e texto grande?
Testamos o menu, a tela de histórico e a tela de ranking na largura de um celular estreito com o texto ampliado em 50 por cento, em inglês, árabe e coreano, e garantimos que nada transborde nem se sobreponha.

### E se algo der errado no app?
Se algo inesperado der errado, um protetor global de erros o captura em vez de deixar o app cair. Se um item salvo não puder ser lido na inicialização, o jogo recorre a um valor padrão seguro para esse item e abre mesmo assim.

### As traduções foram revisadas?
Uma verificação de tradução roda a cada build e aponta textos faltando ou quebrados. As traduções em si foram feitas com IA e ainda não foram revisadas por falantes nativos.

### O Claimball já foi lançado?
Ainda não. Ele continua em testes e chega em breve ao iOS e ao Android, e ainda não há data de lançamento.
