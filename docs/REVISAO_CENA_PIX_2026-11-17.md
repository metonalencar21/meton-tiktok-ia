# Revisão visual da cena Pix — 17/11/2026

## Estado

**BLOQUEADO PARA PUBLICAÇÃO.** Esta revisão é desenvolvimento e não aprova vídeo, release ou agendamento.

## Mudanças persistidas

- `scripts/render_identity_probe.py` chegou à revisão 9.
- O celular 3D agora usa um único root animado; carcaça, tela e alerta permanecem agrupados.
- `scripts/validate_identity_probe.py` passou a validar a assinatura PNG real e evidências da montagem do prop.
- O celular foi trazido para a faixa inferior do close depois de duas rejeições visuais: fora do quadro e grande demais.

## Evidências executadas

- Action 13: https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44078085954
  - passou tecnicamente;
  - revisão visual rejeitou o celular por encobrir a personagem.
- Action 14: https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44079374099
  - passou tecnicamente;
  - revisão visual rejeitou porque o celular voltou a ficar fora do quadro.
- Action 15: https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/44080372004
  - passou tecnicamente;
  - quadros reais revisados: celular visível na parte inferior, sem cobrir rosto e olhos;
  - ainda aparece parcialmente cortado e não está preso à mão.

## Avaliação visual criteriosa

Avanços confirmados:

- personagem articulada CGI 3D, com expressões diferentes nos três instantes;
- olhos castanhos legíveis;
- iluminação neon rosa/roxo/azul;
- prop 3D de Pix realmente renderizado e animado, não inserido como slide;
- composição preserva rosto e expressão na revisão 9.

Falhas que continuam impedindo liberação:

- cabelo curto/preso, não longo como a referência oficial;
- camiseta sem mangas, não moletom preto/rosa;
- rosto e silhueta ainda diferentes da personagem oficial;
- celular parcialmente cortado e sem contato convincente com a mão;
- alerta é geométrico e ainda não conta sozinho uma ação de segurança clara;
- não há episódio completo, narração, legendas, cortes ou duração acima de 60 s;
- não existem quatro vídeos diferentes aprovados em `public/release-candidates/`.

## Metricool em 17/11/2026

- marca 7349860 conectada ao TikTok `metonalencar`;
- fuso confirmado: `America/Fortaleza`;
- nenhum post futuro encontrado entre 17/11 e 17/12;
- nenhum agendamento criado ou alterado.

Métricas reais dos quatro vídeos antigos:

- 556 visualizações;
- 2 curtidas;
- 0 comentários;
- 1 compartilhamento;
- alcance, retenção, taxa de conclusão e tempo assistido indisponíveis no retorno atual.

## Próximo passo técnico

Ancorar o celular ao controle de mão do rig e substituir a roupa/cabelo por geometria compatível com a identidade oficial antes de tentar montar um piloto completo. O workflow antigo de slides permanece desativado e não deve ser reativado.
