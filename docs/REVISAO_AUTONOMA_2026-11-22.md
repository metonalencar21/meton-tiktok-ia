# Revisão autônoma — 22/11/2026

Status: **AVANÇO VISUAL COMPROVADO; PROJETO NÃO PRONTO, SEM PUBLICAÇÃO**.

## Actions e correções desta execução

- [Action #22 — 44904136156](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44904136156): falhou corretamente no novo bloqueio de telefone estático.
- `556dd87`: passou a rastrear `DEF-Hand.R`, registrar projeção normalizada na câmera e usar fallback animado dentro do quadro.
- `602710f`: o validador passou a exigir três posições diferentes, profundidade positiva e projeção segura do telefone.
- Actions #23 e #24 falharam; o log do #24 mostrou o terceiro quadro em `x=1.191577`, fora da câmera.
- `85ac90f`: recentrou o fallback e reduziu o deslocamento lateral.
- [Action #25 — 45022545257](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/45022545257): passou tecnicamente, mas a inspeção dos PNGs ainda não mostrou o telefone. Isso provou que posição lógica e render real não eram equivalentes.
- `5df1d6b`: removeu as FCurves antigas do `phone_root` antes do render, impedindo a reavaliação que devolvia o prop para fora do quadro.
- [Action #26 — 45023190753](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/45023190753): passou o validador atual e gerou artefato revisado visualmente.

## Evidência audiovisual real do #26

Os três PNGs do contato visual mostram:

1. telefone Pix 3D visível nos três quadros;
2. três posições distintas;
3. tela azul e alerta rosa presentes;
4. personagem, mãos, cabeça e câmera mudando entre os quadros;
5. cenário neon preservado.

O relatório confirma revisão 16, `phone_anchor=DEF-Hand.R`, três posições mundiais distintas e projeções dentro da câmera:

- quadro 1: `(0.389405, 0.146551)`;
- quadro 2: `(0.391215, 0.240413)`;
- quadro 3: `(0.616723, 0.145997)`.

## Reprovações que permanecem

- o telefone ainda flutua à frente do tronco; não há pega convincente pela mão;
- cabelo curto/preso, não cabelo longo castanho;
- regata, não moletom preto/rosa;
- base de benchmark, não atuação temática original completa;
- sem narração pt-BR, legendas dinâmicas e cortes de 2–4 s;
- sem vídeo completo acima de um minuto;
- sem quatro episódios diferentes;
- nenhum candidato em `public/release-candidates/semana-atual.json`.

Por isso, o sucesso do Action #26 **não libera piloto, release gate, cron ou publicação**.

## Metricool em 22/11/2026

- brandId `7349860`, TikTok `@metonalencar`, fuso `America/Fortaleza`;
- nenhum post futuro entre 22/11 e 22/12/2026;
- nenhuma duplicação criada;
- quatro vídeos antigos: 556 visualizações, 2 curtidas, 0 comentários e 1 compartilhamento;
- retenção, tempo assistido e monetização indisponíveis;
- nenhuma mídia enviada, agendada ou publicada.

## Próxima correção

Substituir o fallback flutuante por uma pega visual convincente: alinhar o telefone à palma deformada, orientar o aparelho com a mão e adicionar prova por pixels/máscara do prop renderizado. Depois, construir cabelo longo e moletom deformáveis antes de produzir sequência audiovisual.
