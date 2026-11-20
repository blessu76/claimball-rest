---
title: O ciclo da partida passa para um motor de jogo
description: A animação do tabuleiro da partida agora roda em um motor de jogo, e a partida pausa quando você sai do app.
summary: Passamos o ciclo de animação do tabuleiro principal para o motor de jogo Flame, então o tempo dele fica controlado em um só lugar. O jogo funciona como antes. Se você sair do app durante uma partida, ela pausa e espera você tocar em Continuar. Ainda está em testes e chega em breve para iOS e Android.
slug: match-loop-and-pause
lang: pt-BR
category: devlog
translation_of: en
keywords: Claimball, motor de jogo, pausa, partida, diário
---
Os jogadores não veem uma regra nova aqui. É uma mudança interna que mantém o tabuleiro da partida estável.

## Um só ciclo para o tabuleiro

A animação do tabuleiro antes rodava no próprio temporizador. Agora ela roda no motor de jogo Flame, que controla os quadros do tabuleiro em um só lugar.

## Saiu do app, volta pausado

Se entrar uma ligação, aparecer uma notificação ou você trocar de app, a partida pausa. Ao voltar, toque em Continuar para seguir. Enquanto você está fora, nada se mexe.

## O mesmo jogo

Pontuação, regras, salvamentos e compras não mudaram. O tabuleiro parece e joga igual ao de antes.

## Ainda em testes

Seguimos verificando o novo ciclo em celulares reais.

## O que vem a seguir

O Claimball ainda está em testes e chega em breve para iOS e Android. Ainda não há data de lançamento.

## Perguntas frequentes

### As regras mudaram?
Não. Pontuação, regras, salvamentos e compras continuam iguais. Só mudou a forma como a animação do tabuleiro é executada.

### O que acontece se eu sair durante uma partida?
A partida pausa. Toque em Continuar quando voltar.

### O Claimball já foi lançado?
Ainda não. Ele está em testes e chega em breve para iOS e Android, e ainda não há data de lançamento.
