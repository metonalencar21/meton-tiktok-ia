# Auditoria do gate de liberação — 28/11/2026

## Estado confirmado

- catálogo dos híbridos: `approved=false`, `scheduled=false`,
  `published=false`;
- diretório `public/release-candidates/`: inexistente;
- Metricool brandId `7349860`: nenhum post futuro entre 28/11 e 28/12;
- nenhuma alteração nova nos quatro MP4s desde a revisão de 24/11.

## Falha preventiva corrigida

O gate técnico validava formato, áudio, movimento e evidências visuais, mas ainda
dependia do preparador para garantir dois requisitos. Um manifesto criado à mão
poderia chegar ao gate sem prova de aprovação explícita ou com datas vencidas.

`scripts/validate_release_gate.py` agora também exige:

1. objeto `approval` presente;
2. `user_approved=true`;
3. escopo exato `four_complete_hybrid_videos`;
4. `approved_at` com fuso e sem data futura;
5. quatro horários em ordem, diferentes e com pelo menos duas horas de margem;
6. manutenção das validações anteriores de mídia, identidade, revisão visual,
   rótulo de IA e autopublicação.

## Testes

Passaram localmente os self-tests do preparador e do gate. Também foi confirmado
que o estado atual termina em `BLOQUEADO`, pois não existe manifesto de candidatos
aprovados. Isso é o comportamento correto e não significa publicação.

Nenhum agendamento ou publicação foi executado nesta auditoria.
