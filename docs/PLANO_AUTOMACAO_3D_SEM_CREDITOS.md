# Plano técnico — TikTok IA 3D sem custos recorrentes

Estado: proposta de implementação, **não aprovada nem comprovada tecnicamente**. Data: 01/11/2026.

## O objetivo do usuário

Manter **quatro episódios por semana**, gerados, conferidos e agendados automaticamente, sem ações manuais semanais nem custos de assinatura, para @metonalencar (Metricool brandId 7349860, America/Fortaleza). A referência visual OBRIGATÓRIA é docs/DIRECAO_CRIATIVA.md: apresentadora FEMININA estilizada em 3D com cabelo castanho comprido, olhos expressivos, moletom preto e detalhes rosa; cenários rosa/roxo/ciano. Nunca trocar pelo robô 2D, slides ou ícones genéricos.

## Problema de origem

O projeto atual já gera MP4s e sabe agendar no Metricool, mas não possui animador 3D. Os renderizadores Pillow/FFmpeg e o storyboard 2.5D NÃO cumprem a referência. Renderização e publicação não devem recomeçar no estilo rejeitado. Alterar arquivo no GitHub não altera o MP4 que já foi importado no Metricool.

O Runway conectado está no plano Free e não oferece modelos de vídeo pela integração; créditos de testes que não se renovam são inadequados para rotina semanal.

## Arquitetura pretendida

1. **Modelo permanente de personagem 3D — trabalho único, reutilizável:**
   - Criar/adaptar um modelo feminino com cabelo, roupa, face e paleta da arte original.
   - Rig com bones, expressões faciais e controles de boca. Os modelos gratuitos do Blender Studio (p.ex. Rain CC BY) são referência de viabilidade, **não identidade visual aprovada**. Respeitar licença e atribuição. Não usar modelo de terceiros com licença incerta.
   - Uma vez aprovado o personagem-base, ele deve ser reutilizado em todos os vídeos sem nova aprovação a cada episódio.
2. **Biblioteca fixa de cenas e ações 3D:**
   - Cenários de café, quarto, escritório e interface de celular; props de mensagens, Wi-Fi, senha, QR code, Pix, backup.
   - Movimentos reais e gestos: olhar, falar, apontar, tocar no telefone, caminhar, recuar, reagir e trocar expressões.
   - Câmeras e tomadas diferentes a cada 2–4s quando narrativa justificar. Evitar reapresentar a mesma tela com títulos diferentes.
3. **Orquestrador editorial:**
   - Roteiros originais com ganchos e ações por cena (estrutura JSON de cenas, personagens e objetos).
   - Cada pauta mapeada para um episódio com ações apropriadas, em vez de template único e estático.
   - Narração neural PT-BR quando disponível e sincronização de boca via alinhamento fonético/shape keys; falhar com relatório quando voz falhar.
4. **Execução agendada no GitHub Actions:**
   - Baixar Blender gratuito no Ubuntu runner e produzir em modo headless por scripts Python.
   - Renderizar tomadas de forma otimizada em CPU; testar custo de renderização, limite de duração, qualidade e viabilidade para quatro vídeos por semana. Não usar provedores não oficiais de GPU nem contornar limites.
   - Montar som, trilha livre e cortes no FFmpeg; verificar vídeo 9:16 H.264/AAC, 30fps, duração compatível, sincronização de áudio, legibilidade.
   - Publicar MP4s em public/ e manifesto com atributo de *teste visual* independente de codec. Não declarar qualidade apenas pelo manifesto.
5. **Metricool gratuito / automação existente:**
   - Checar posts e analytics para não duplicar.
   - Agendar automaticamente só quando a qualidade do **arquivo MP4 efetivo** foi validada por uma avaliação visual inicial e por critérios técnicos, além de haver autorização do usuário para o formato-base. Usar autoPublish=true, TikTok, rótulo de IA isAigc=true e cota grátis de 20 publicações reais/mês.
   - Reportar erros e não repetir chamadas bloqueadas. Não comprar plano, não usar API paga.
6. **Análise de desempenho:**
   - Buscar dados reais de views, comentários, compartilhamentos, retenção/tempo médio quando disponíveis.
   - Alterar aberturas, enquadramentos e ritmo sem adulterar a identidade aprovada; não estimar ganhos sem dados.

## Validação de viabilidade ANTES de religar o cron

- [ ] Garantir licença e acesso a modelo feminino 3D com qualidade próxima à arte enviada.
- [ ] Criar um piloto real com pelo menos três movimentos distintos (gesto de personagem, boca e interação com celular), sem cortes que sejam apenas zoom em ilustrações.
- [ ] Renderizar um episódio de teste em GitHub Actions dentro de limites técnicos e sem custos.
- [ ] Inspecionar de fato frames e áudio; descartar deformações nas mãos/cabelo e falta de sincronização.
- [ ] Apresentar um único piloto audiovisual ao usuário. Aprovação única do formato, não aprovação semanal.
- [ ] Só após aprovação e teste de escala, religar cron e postagem de quatro vídeos/semana.

## Limitações que NÃO devem ser escondidas

- Automatizar uma personagem 3D com rig é possível, mas resultado não será necessariamente igual à animação cinematográfica generativa da referência.
- O modelo inicial precisa ser criado/ajustado uma única vez; a imagem 2D não se transforma automaticamente em uma malha 3D fiel e já rigada.
- Renderização CPU de vários minutos de 3D por semana pode exceder o limite de execução de um único job; medir e otimizar ou dividir por episódio.
- Nenhuma API de vídeo generativo gratuita e ilimitada foi confirmada como viável em operação permanente sem interação humana.
- Não garantir monetização ou viralização; o projeto otimiza por retenção e engajamento mensurados, com amostra real.

## Estado atual

- **Geração semanal antiga pausada** no workflow gerar-videos.yml.
- **Post antigo** "Mais espaço sem apagar memórias" transformado em draft=true, autoPublish=false em 01/11/2026.
- A rotina semanal no ChatGPT monitora sem novos agendamentos, aguardando piloto fiel.
- Este documento é um plano. **Não afirmar que a nova produção 3D está em funcionamento** até que as caixas acima sejam validadas.
