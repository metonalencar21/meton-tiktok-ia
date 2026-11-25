# Preparação segura pós-aprovação — 25/11/2026

## Resultado desta execução

Foi adicionado `scripts/prepare_release_candidates.py`, uma etapa intermediária
que prepara os quatro MP4s para o gate técnico **sem agendar nem publicar**.

O script só aceita a promoção quando o catálogo registra, ao mesmo tempo:

- aprovação explícita do usuário para os quatro vídeos completos;
- aprovação individual e revisão audiovisual completa de cada episódio;
- evidências descritivas de identidade, movimento, variedade, áudio, legendas e
  storytelling;
- quatro datas futuras, distintas e em ordem, no fuso `America/Fortaleza`.

Quando esses requisitos forem atendidos, ele copiará as mídias para
`public/release-candidates/`, produzirá folhas de contato e escreverá
`semana-atual.json`. Isso apenas habilita o gate técnico existente. A revisão
visual e as quatro confirmações reais do Metricool continuam obrigatórias.

## Testes executados

- self-test do novo preparador: passou;
- self-test de `scripts/validate_release_gate.py`: passou;
- compilação Python dos dois scripts: passou;
- catálogo atual, com `approved=false`: promoção bloqueada corretamente;
- datas repetidas: bloqueadas corretamente.

O workflow `.github/workflows/validar-liberacao.yml` agora executa os dois
self-tests em cada alteração do gate ou dos candidatos.

## Estado preservado

Os quatro pilotos continuam com `approved=false`, `scheduled=false` e
`published=false`. Nenhum arquivo foi promovido para candidato, nenhum post foi
agendado e nenhum conteúdo foi publicado.

O Metricool foi consultado em 25/11/2026 para o brandId `7349860`: não havia
post futuro entre 25/11 e 25/12 no fuso `America/Fortaleza`. Portanto não há
duplicata futura a remover ou alterar.

## Próxima transição permitida

Somente após a aprovação explícita do formato híbrido dos quatro MP4s completos:

1. registrar a evidência de aprovação e as revisões individuais no catálogo;
2. executar o preparador com quatro horários futuros;
3. executar o gate técnico e revisar os MP4s candidatos;
4. reconferir perfil, duplicatas e limite gratuito no Metricool;
5. agendar um por vez com `autoPublish=true` e `tiktokData.isAigc=true`, aceitando
   a etapa apenas quando cada retorno trouxer confirmação e ID reais.

O ciclo recorrente não será reativado antes de essa primeira semana completar
todas as etapas acima.
