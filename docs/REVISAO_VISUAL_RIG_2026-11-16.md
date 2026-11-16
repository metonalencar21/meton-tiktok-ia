# Revisão visual e mapa de atuação do rig — 16/11/2026

Status: **AVANÇO TÉCNICO COMPROVADO; REPROVADO COMO IDENTIDADE FINAL E COMO PILOTO**.

## Mudanças persistidas

- Commit `6edd73f`: inventário semântico de mãos, braços, cabeça, olhar, boca e tronco.
- Commit `1a42b31`: primeira tentativa de plano médio e neutralização de emissão.
- Commit `2dfb68a`: close real, luzes reduzidas e compositor do benchmark desativado.
- Commit `c39cfad`: substituição dos shaders de olhos por BSDF previsível.
- Commit `4a0758b`: rastreamento de slots, polígonos e nós de materiais visíveis.
- Commit `f773225`: desativação, somente na prova, da córnea Glossy/Refraction incompatível com Eevee headless.

## Actions e evidências

- [Mapa de controles — 43864795150](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43864795150): sucesso.
- [Prova de close — 43865740920](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43865740920): sucesso técnico, revisão visual reprovada.
- [Prova de shaders oculares — 43867055940](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43867055940): sucesso técnico, olhos ainda encobertos.
- [Mapa de materiais — 43867808523](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43867808523): sucesso; identificou a córnea separada `GEO-rain_eye_cornea` com Glossy + Refraction.
- [Prova sem a córnea incompatível — 43868339767](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43868339767): sucesso; três quadros reais revisados.

Os artefatos são temporários de desenvolvimento e não pertencem a
`public/release-candidates/`.

## O que foi confirmado visualmente

1. O plano médio/close agora mostra rosto, mãos e tronco com dimensão suficiente para revisão.
2. Os olhos castanhos e pupilas ficaram visíveis na prova 5; o halo branco das provas anteriores veio da casca de córnea refrativa.
3. A atuação existente muda cabeça, pálpebras, boca, mãos e postura entre os três instantes.
4. O mapa encontrou controles utilizáveis para prop e atuação, incluindo `IK-Hand.L`, `IK-Hand.R`, `FK-Head`, controles de olhar e controles faciais.
5. O fluxo gratuito Blender + Eevee continua executável no GitHub Actions.

## Reprovações que permanecem

- cabelo preso/curto, sem o cabelo castanho longo da referência;
- regata sem mangas, não o moletom preto com acabamento rosa e emblema;
- rosto e silhueta ainda não reproduzem a apresentadora oficial;
- ausência de celular, Pix, mensagens, senhas, permissões, backup ou outra situação temática;
- ausência de fala, sincronização labial, narração, legendas e sequência editada;
- apenas três quadros de uma animação de benchmark, não um piloto audiovisual original;
- nenhuma evidência de quatro episódios diferentes acima de um minuto;
- a correção de córnea usada na prova é diagnóstica; o modelo final precisa de um shader transparente/refrativo compatível, não simplesmente esconder a geometria.

Por isso, os Actions verdes **não liberam** piloto, release gate, cron ou Metricool.

## Estado do Metricool em 16/11/2026

- brandId `7349860`, perfil TikTok `@metonalencar`, fuso `America/Fortaleza`.
- Nenhum post futuro entre 16/11 e 16/12/2026; nenhuma duplicação criada.
- Quatro vídeos antigos encontrados nas métricas: 556 visualizações, 2 curtidas, 0 comentários e 1 compartilhamento no total.
- Alcance, taxa de conclusão, tempo total e tempo médio assistido vieram nulos; não há base para inventar retenção.
- Nenhuma mídia foi enviada, agendada ou publicada nesta execução.

## Próxima correção obrigatória

1. construir cabelo longo e moletom como geometria deformável coerente, preservando o rig;
2. parentear um celular real ao controle `IK-Hand.R`/GRAB e testar três ações temáticas: receber alerta, conferir destinatário e bloquear/confirmar;
3. renderizar uma sequência curta de movimento, não só quadros, com close e plano médio;
4. somente depois adicionar voz pt-BR, legendas dinâmicas e roteiro de 2–4 s por ação;
5. manter `public/release-candidates/` vazio até existir material audiovisual realmente aprovado.

O piloto Pix 2.5D de 08/11 continua não aprovado, e o workflow antigo de slides permanece desativado.
