# Base articulada 3D gratuita — exploração de 14/11/2026

Status: **base técnica candidata; identidade visual ainda não adaptada nem aprovada**.

## Resultado reproduzível

O workflow [Explorar rig 3D livre para a personagem oficial](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/43592227332) baixou diretamente o objeto Git LFS oficial, verificou tamanho e SHA-256, abriu o arquivo no Blender headless e executou `scripts/inspect_character_rig.py`.

- Fonte: benchmark oficial Rain da Blender Foundation.
- Licença: CC-BY 4.0; qualquer uso exige atribuição.
- SHA-256 validado: `34639c2fb8d2fe42179a2e1832b78b35933a1df602b0de55f6943ac6b4f75655`.
- A fonte não é incorporada ao repositório e não contém segredos.
- Nenhuma mídia foi publicada, agendada ou enviada ao Metricool.

## Capacidade encontrada

| Item | Resultado |
|---|---:|
| Armatures | 6 |
| Malhas | 127 |
| Vértices | 109.810 |
| Ossos deformadores | 806 |
| Controles estimados | 3.642 |
| Shape keys sem Basis | 448 |
| Materiais | 41 |
| Actions | 25 |
| Câmeras | 1 |
| Luzes | 8 |

O personagem principal expõe o armature `RIG-rain` com 2.216 bones, incluindo controles de olhos, pálpebras, sobrancelhas, bochechas e lábios. Isso resolve apenas o gargalo de **capacidade de articulação**; não resolve fidelidade estética.

## Pontos de adaptação já identificados

Malhas separadas relevantes:

- `GEO-rain_hair_main`
- `GEO-rain_hair_ponytail`
- `GEO-rain_hair_strand`
- `GEO-rain_head`
- `GEO-rain_eyes`
- `GEO-rain_top`
- `GEO-rain_body`

Materiais relevantes:

- `MAT-rain.hair`
- `MAT-rain.eyes`
- `MAT-rain.top`
- `MAT-rain.body`
- `MAT-rain.hairband`

Controles faciais confirmados incluem `ACT-Eyelid_Upper`, `ACT-Eyelid_Lower`, `ACT-Lips_Corner`, `ACT-Lip_Roll_Upper`, `ACT-Lip_Roll_Lower`, `ACT-Cheek_Inner`, `ACT-Cheek_Outer`, `AIM-Eye.L` e `AIM-Eye.R`.

## Restrições que continuam obrigatórias

Rain é somente uma base de rig. **Não é a personagem oficial** e não pode aparecer em publicação sem transformação e revisão. Ainda faltam:

1. cabelo longo castanho compatível com a referência;
2. olhos castanhos grandes e expressão acolhedora;
3. moletom preto com detalhes e emblema rosa;
4. estúdio tecnológico roxo/rosa neon;
5. biblioteca de atuação: falar, apontar, reagir, segurar/tocar celular, recuar e confirmar;
6. teste de render CPU sustentável;
7. piloto audiovisual completo e revisão visual;
8. quatro episódios diferentes aprovados pelo gate e pelo controle visual.

O workflow antigo de slides permanece desativado. Esta exploração não altera `approved=false`, não cria candidatos em `public/release-candidates/` e não autoriza agendamento.
