---
title: Como termina uma partida empatada em Claimball
description: Um empate costumava terminar com um resultado confuso. Veja como funciona o confronto decisivo agora e o que mudou nas versões de teste mais recentes.
slug: sudden-death-and-draws
lang: pt-BR
category: devlog
translation_of: en
published: 2026-11-03T21:05+09:00
keywords: Claimball, confronto decisivo, empate, jogo casual, diário
---
Uma partida de Claimball dura 90 segundos em uma grade de caderno, e na maioria das vezes um lado simplesmente tem mais território quando o relógio para. Esta publicação trata do outro caso: a partida termina igual.

## O que acontece em um empate

Quando o tempo acaba com o mesmo número de quadrados, a partida vai para o confronto decisivo. O relógio para e o próximo ponto decide a partida. Se ainda houver uma bola no ar aos 90 segundos, a partida espera ela cair antes de contar.

## O bug que corrigimos

Em nossas versões de teste, um confronto decisivo podia terminar com os quadrados ainda iguais, por exemplo 29 a 29, enquanto a tela de resultado dizia que você perdeu. O vencedor era decidido corretamente, mas os números na tela não mostravam isso, então parecia errado.

Primeiro fizemos esse resultado aparecer como empate. Depois decidimos que um confronto decisivo nunca deve parecer um empate: o jogador que faz o ponto decisivo agora toma um quadrado do rival, se necessário, e o tabuleiro mostra 30 a 28 em vez de 29 a 29. A tela de resultado sempre concorda com os números finais.

## Também nas versões de teste mais recentes

O logo e o número do Combo máximo agora mantêm a ordem correta em idiomas escritos da direita para a esquerda, como o árabe, e a página de Notas de versão do site lista o que mudou em cada versão.

## O que vem a seguir

Claimball ainda está em testes e chega em breve para iOS e Android. Ainda não há data de lançamento.
