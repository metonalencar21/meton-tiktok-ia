# Gate de aprovação visual — pilotos híbridos — 24/11/2026

## Estado

Os quatro pilotos passaram pela revisão técnica e visual interna do formato
híbrido. **Ainda não estão aprovados para publicação**, porque a direção criativa
exige uma aprovação explícita do usuário após assistir aos MP4s completos.

`approved=false`, `scheduled=false`, `published=false`.

## Arquivos completos para assistir

- [01 — Golpe do Pix urgente](https://github.com/metonalencar21/meton-tiktok-ia/blob/main/public/pilotos/hibrido_01_pix_urgente.mp4)
- [02 — Senhas diferentes](https://github.com/metonalencar21/meton-tiktok-ia/blob/main/public/pilotos/hibrido_02_senhas_diferentes.mp4)
- [03 — Permissões do celular](https://github.com/metonalencar21/meton-tiktok-ia/blob/main/public/pilotos/hibrido_03_permissoes_celular.mp4)
- [04 — Backup das fotos](https://github.com/metonalencar21/meton-tiktok-ia/blob/main/public/pilotos/hibrido_04_backup_fotos.mp4)

## Evidências objetivas

| Episódio | Duração | Movimento quase estático | Maior trecho | Áudio médio / pico |
|---|---:|---:|---:|---:|
| Pix | 90,0 s | 21,2% | 3,0 s | -19,7 / -2,7 dB |
| Senhas | 90,6 s | 5,0% | 2,0 s | -19,9 / -3,7 dB |
| Permissões | 93,8 s | 9,6% | 1,0 s | -19,7 / -3,4 dB |
| Backup | 91,1 s | 8,8% | 2,0 s | -19,7 / -3,2 dB |

Todos: 720x1280, 9:16, H.264, AAC mono, 30 fps, voz neural
`pt-BR-FranciscaNeural`, dez cenas. As legendas dinâmicas usam frases curtas em
até duas linhas e não cortam palavras.

## Revisão visual

- identidade preservada: cabelo castanho comprido, olhos grandes, moletom
  preto/rosa e iluminação neon;
- cinco planos da apresentadora e cinco demonstrações por episódio;
- Pix usa alerta, bloqueio, ligação e resolução;
- Senhas usa vazamento/bloqueio, cofre e confirmação;
- Permissões mostra câmera, microfone, localização e revogação;
- Backup mostra galeria, nuvem, Wi-Fi, progresso e restauração;
- mudança visual relevante em no máximo 1–3 segundos conforme a medição.

## Limitações transparentes

É um formato híbrido CGI **2.5D**, não personagem 3D articulada. Não há lip-sync.
O movimento da apresentadora usa parallax; as ações demonstrativas acontecem nas
interfaces animadas. A aprovação deve considerar exatamente este formato, sem
confundi-lo com animação 3D cinematográfica.

## Aprovação necessária

Uma única resposta explícita do usuário aprovando o **formato híbrido dos quatro
MP4s completos** libera a próxima etapa. Depois disso, ainda será obrigatório:

1. copiar os arquivos aprovados para `public/release-candidates/`;
2. executar `scripts/validate_release_gate.py`;
3. conferir novamente duplicações, perfil e cota gratuita no Metricool;
4. agendar quatro datas futuras com `autoPublish=true` e `isAigc=true`;
5. confirmar individualmente os quatro IDs antes de reativar a rotina semanal.

Metricool consultado em 24/11/2026: nenhum agendamento futuro encontrado para o
brandId `7349860` em `America/Fortaleza`.

## Rastreabilidade

- Pix: Actions `45393864016`, mídia commit `bb76cb8`;
- Senhas: Actions `45393863955`, mídia commit `c1cb3a8`;
- Permissões e Backup: Actions `45393863954`, mídia commit `ddd813c`.
