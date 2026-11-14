---
title: Como verificamos que o marcador de pouso diz a verdade
description: O marcador de pouso só é útil se estiver certo. Veja como testamos que ele mostra as casas que realmente são pintadas.
summary: O marcador de pouso do Claimball só ajuda se estiver certo, então testamos se ele coincide com as casas que realmente são pintadas. Jogamos muitas partidas completas simuladas com diferentes sementes aleatórias e comparamos cada marcador com o resultado, e também quebramos a regra de propósito para confirmar que o teste falha. O jogo ainda está em teste e chega em breve ao iOS e ao Android.
slug: marker-keeps-its-word
lang: pt
category: devlog
keywords: Claimball, marcador de pouso, testes, jogo justo, diário
---
O marcador de pouso mostra onde a bola vai cair, então precisa estar certo todas as vezes. É assim que ele é testado nas versões de teste internas do TestFlight, que ainda não foram lançadas ao público.

## Uma promessa na tela

Se o marcador indicasse uma casa e o jogo pintasse outra, você deixaria de confiar nele, e o jogo pareceria injusto. Por isso o marcador precisa coincidir com o que realmente acontece.

## Uma regra para os dois

O marcador e o impacto real devem concordar. Verificamos isso jogando partidas completas simuladas, muitas e muitas vezes com diferentes sementes aleatórias, e comparando cada marcador com as casas que foram realmente pintadas. Eles precisam concordar todas as vezes.

## Testando o teste

Um teste que nunca falha prova pouco. Por isso também quebramos a regra de propósito, por exemplo mexendo um valor de leve, e garantimos que o teste percebe e falha.

## Rivais e regras especiais também

A mesma comparação roda com cada rival de IA e com as variantes do Desafio Diário, já que elas mudam a velocidade e o comportamento.

## Honestos sobre os limites

Essas verificações rodam em partidas simuladas. Jogar em celulares de verdade é uma rodada de testes separada.

## O que vem a seguir

O Claimball ainda está em teste e chega em breve ao iOS e ao Android. Ainda não há data de lançamento.

## Perguntas frequentes

### Por que o marcador de pouso precisa ser preciso?
Se o marcador indicasse uma casa e o jogo pintasse outra, você deixaria de confiar nele, e o jogo pareceria injusto.

### Como vocês testam o marcador?
Jogamos partidas completas simuladas muitas e muitas vezes com diferentes sementes aleatórias e comparamos cada marcador com as casas que foram realmente pintadas. Eles precisam concordar todas as vezes.

### O teste cobre os rivais e o Desafio Diário?
Sim. A mesma comparação roda com cada rival de IA e com as variantes do Desafio Diário, já que elas mudam a velocidade e o comportamento. Essas verificações rodam em partidas simuladas, e jogar em celulares de verdade é uma rodada de testes separada.

### O Claimball já foi lançado?
Ainda não. Ele está em teste e chega em breve ao iOS e ao Android, e ainda não há data de lançamento.
