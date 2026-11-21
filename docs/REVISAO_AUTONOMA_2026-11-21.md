# Revisão autônoma — 21/11/2026

Status: **PROGRESSO TÉCNICO; PROJETO NÃO PRONTO, SEM PUBLICAÇÃO**.

## Evidência revisada

- Action #20: [44902999313](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44902999313), commit `0411a8e`.
- O relatório passou a reconhecer os controles reais `IK-Hand.L`, `IK-Hand.R` e `FK-Head`.
- A revisão dos três PNGs mostrou que o celular Pix desapareceu do enquadramento.
- O próprio JSON confirmou a falha: as três posições mundiais do telefone eram idênticas.
- Action #21: [44903502064](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44903502064), commit `91611f6`.
- A segunda tentativa moveu o telefone para a frente da malha e registrou a posição nos mesmos quadros renderizados, mas a revisão visual continuou sem mostrar o prop e as três posições permaneceram idênticas.

Um Action verde não foi tratado como aprovação visual.

## Correções persistidas

1. `0411a8e`: mapeamento dos controles reais do rig e tentativa de ancoragem no controle da mão direita.
2. `91611f6`: cálculo da posição do telefone nos quadros efetivamente revisados e folga frontal para evitar oclusão.
3. `d7330ed`: o validador agora reprova automaticamente:
   - revisão anterior à 13;
   - ausência dos três controles reais esperados;
   - âncora diferente de `IK-Hand.R`;
   - telefone com menos de três posições distintas nos quadros revisados.

A falha visual encontrada passa a bloquear o CI em vez de ser mascarada por arquivos PNG e codecs válidos.

## Identidade visual

A base articulada continua inadequada como identidade final:

- cabelo curto/preso, não cabelo longo castanho;
- regata, não moletom preto/rosa;
- sem quatro histórias temáticas completas;
- sem narração pt-BR, legendas dinâmicas e montagem de 2–4 s por ação;
- nenhum episódio completo acima de um minuto aprovado;
- `public/release-candidates/` continua sem quatro candidatos aprovados.

## Metricool em 21/11/2026

- brandId `7349860`, TikTok `@metonalencar`, fuso `America/Fortaleza`.
- Nenhum post futuro entre 21/11 e 21/12/2026; nenhuma duplicação criada.
- Quatro vídeos antigos: 556 visualizações, 2 curtidas, 0 comentários e 1 compartilhamento.
- Retenção, tempo assistido e monetização não vieram disponíveis; nada foi estimado.
- Nenhuma mídia foi enviada, agendada ou publicada.

## Próxima execução

Diagnosticar a transformação efetiva dos filhos do `METON-PIX-phone-root` e testar a posição de um osso deformador que acompanhe a mão visível (`DEF-Hand.R` ou `GRAB-Hand.R`), mantendo o novo bloqueio de deslocamento no validador. Somente depois avançar para cabelo longo, moletom, atuação temática original e piloto audiovisual.
