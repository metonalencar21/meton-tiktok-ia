# Revisão visual da prova do rig — 15/11/2026

Status: **REPROVADO COMO IDENTIDADE FINAL; APROVADO SOMENTE COMO BASE DE MOVIMENTO**.

## Evidência examinada

- Action: [43715637479](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43715637479)
- Artefato: `prova-identidade-rig-3d`, contendo três PNGs reais, contato visual e JSON.
- Frames renderizados: 128, 190 e 251.
- Resolução da prova: 270x480 vertical.
- Motor: Eevee, não Workbench.
- Tempo total do job: 6 min 11 s, incluindo instalação, download do rig, três renders e montagem.
- Nenhum arquivo foi colocado em `public/release-candidates/`.
- Nenhuma mídia foi enviada ao Metricool.

## O que a prova confirmou

1. Há atuação tridimensional real: posição das mãos, inclinação da cabeça, tronco e expressão mudam entre os quadros.
2. O rig tem qualidade técnica suficiente para animação corporal e facial.
3. A paleta pink/roxo/azul e materiais castanho/preto podem ser aplicados automaticamente.
4. O render headless gratuito funciona no GitHub Actions com EGL/Mesa/Xvfb.
5. Três quadros de baixa resolução cabem no runner; isso ainda não comprova viabilidade de episódios completos.

## Reprovações visuais

A prova **não corresponde à personagem oficial**:

- cabelo curto/preso, sem o cabelo castanho longo da referência;
- roupa sem mangas, não o moletom preto com detalhes rosa;
- olhos ficaram claros/estourados pela combinação de material e luz;
- silhueta e rosto diferem da apresentadora CGI original;
- enquadramento mostra a personagem pequena e com espaço vazio excessivo;
- cenário é um estúdio mínimo, sem objetos tecnológicos e profundidade equivalentes à referência;
- não há celular, interface, situação temática, legenda, narração ou sincronização labial.

Por isso, logs verdes, movimento e render real **não autorizam** piloto, gate de release, cron ou agendamento.

## Decisão técnica

O rig Rain pode continuar apenas como referência de arquitetura de animação e como fonte de movimentos/controladores sob CC-BY 4.0. Não deve aparecer em vídeo público com sua aparência atual.

Próxima correção obrigatória:

1. resolver cabelo longo, moletom e rosto/olhos antes de animar episódios;
2. aproximar câmera para plano médio e close, evitando personagem minúscula;
3. criar prop de celular e pelo menos três ações temáticas;
4. produzir nova prova curta e revisá-la visualmente;
5. medir render de uma sequência, não apenas três quadros.

O workflow antigo de slides permanece desativado e o piloto Pix 2.5D continua não aprovado.
