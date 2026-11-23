# Revisão audiovisual dos quatro pilotos híbridos — 23/11/2026

## Decisão

**Bloqueados para publicação e agendamento.** Os quatro MP4s existem e têm áudio
neural pt-BR, mas a inspeção do vídeo real mostrou movimento insuficiente e
repetição prolongada de telas. `approved`, `scheduled` e `published` continuam
`false`.

## Evidência técnica e audiovisual

| Episódio | Duração | Formato | Volume médio / pico | Quase estático | Maior trecho quase estático |
|---|---:|---|---:|---:|---:|
| Pix urgente | 90,0 s | 720x1280, H.264/AAC, 30 fps | -19,7 / -2,9 dB | 71,5% | 9,5 s |
| Senhas | 90,6 s | 720x1280, H.264/AAC, 30 fps | -19,9 / -3,7 dB | 71,1% | 10,0 s |
| Permissões | 93,8 s | 720x1280, H.264/AAC, 30 fps | -19,7 / -3,4 dB | 70,6% | 9,5 s |
| Backup | 91,1 s | 720x1280, H.264/AAC, 30 fps | -19,7 / -3,2 dB | 75,1% | 9,5 s |

Método de movimento: amostragem do MP4 a 2 fps, escala 90x160 em tons de cinza,
diferença absoluta média entre quadros; diferença menor que 0,30 é classificada
como quase estática. O contato visual com 20 quadros por episódio confirmou o
resultado: a apresentadora aparece principalmente na abertura e no encerramento,
e as telas intermediárias se repetem em pares. Não há defeito de codec nem áudio
ausente; o bloqueio é criativo e de ritmo visual.

## Correções persistidas no motor

- legendas curtas acompanham a narração em blocos de até sete palavras;
- indicador animado de toque destaca a ação atual nas telas de Pix, senhas,
  permissões e backup;
- cada fase muda o alvo da interação, reduzindo períodos sem ação perceptível;
- o renderizador de Pix não substitui mais globalmente o renderizador de backup;
- o gate técnico agora mede movimento no MP4 e rejeita qualquer trecho quase
  estático acima de 4 segundos ou mais de 58% do vídeo quase estático.

Essas mudanças ainda precisam gerar uma nova versão dos quatro MP4s e passar por
nova revisão audiovisual. Elas não equivalem a aprovação criativa.

## Resultado após duas renderizações corretivas

Os workflows foram consolidados para salvar renders concorrentes com `git pull
--rebase`, evitando que um episódio sobrescreva o outro. Os quatro jobs finais
concluíram com sucesso:

- Pix: Actions `45173098412`, commit de mídia `0669456`;
- Senhas: Actions `45173098375`, commit de mídia `26e984f`;
- Permissões e Backup: Actions `45173098370`, commit de mídia `450c066`.

Nova medição nos MP4s persistidos:

| Episódio | Quase estático | Maior trecho quase estático | Gate de movimento |
|---|---:|---:|---|
| Pix urgente | 40,2% | 3,0 s | passa |
| Senhas | 15,6% | 3,0 s | passa |
| Permissões | 20,3% | 2,0 s | passa |
| Backup | 12,2% | 2,0 s | passa |

A correção eliminou os trechos parados de 9,5–10 segundos, adicionou alvos de
toque perceptíveis e legendas curtas com progresso. A revisão das folhas de
contato, porém, ainda mostra predominância de interfaces 2.5D e a apresentadora
principalmente na abertura/encerramento. Portanto os arquivos continuam como
**pilotos em avaliação**, não candidatos finais; a aprovação visual do usuário
ainda é obrigatória antes de qualquer agendamento.

## Metricool

Consulta ao brandId `7349860`, fuso `America/Fortaleza`, de 23/11 a 23/12/2026:
nenhum post futuro agendado. Portanto não existe duplicação ativa e nenhum ID de
agendamento foi criado nesta revisão.

## Próximo gate

1. Aumentar presença da apresentadora em momentos-chave sem voltar a foto única.
2. Submeter o formato visual ao usuário para uma única aprovação explícita.
3. Somente depois produzir candidatos finais fora de `public/pilotos/`, executar
   `scripts/validate_release_gate.py` e consultar novamente o Metricool.

