# TikTok IA: status e critérios de publicação — 08/11/2026

## Identidade oficial
A referência permanece docs/DIRECAO_CRIATIVA.md: personagem feminina em CGI 3D, cabelos castanhos longos, olhos expressivos, moletom preto com detalhes rosa, ambientes tecnológicos neon. Slides, NEXO 2D e boneco geométrico foram rejeitados.

## Mudanças concluídas nesta etapa
- Ativos CGI reutilizáveis no GitHub: public/assets/personagem-mestre.jpg e public/assets/personagem-pix-alerta.jpg.
- Renderer de teste: scripts/piloto_visual_personagem.py, com cenas alternadas, interface de celular em movimento, alertas, legenda curta, microdeformação de boca, voz neural Edge TTS em português e montagem automática via FFmpeg.
- Execução do GitHub Actions finalizada com sucesso: .github/workflows/piloto-personagem-cinematica.yml.
- Vídeo real criado: public/pilotos/piloto_personagem_cinematica.mp4 (17,6 s, vertical 720 × 1280, H.264/AAC).
- Metadados: public/pilotos/piloto_personagem_cinematica.json; quadros extraídos e revisados: public/pilotos/personagem_cinematica_preview.jpg.
- Rotinas temporárias de importação removidas da branch principal após salvar as duas imagens.

## Limites que não devem ser escondidos
- O estilo é CGI com movimento de camadas 2.5D e rostos de imagens 3D previamente renderizadas. NÃO é um modelo 3D articulado completo nem um vídeo cinematográfico gerativo. A boca não usa sincronização fonética exata.
- Dois retratos e 17,6 segundos não são suficientes para quatro vídeos distintos por semana. É preciso ampliar a biblioteca de poses e situações, e depois gerar um episódio completo de 65 a 85 segundos.
- O plano gratuito do Runway nesta integração gera imagens mas não vídeos. Os créditos gratuitos não podem ser tratados como fonte infinita de novas cenas. Não usar assinatura ou token privado.
- O teste não foi agendado ou publicado no Metricool, nem aprovado pelo usuário. Não declarar monetização ou engajamento sem métricas reais.

## Qualidade obrigatória para reativar a rotina
1. Usuário aprova o visual da personagem e as cenas de um piloto completo.
2. Episódio de mais de 60 segundos com história visual e mais de oito tomadas específicas do tema, não apenas fotos com zoom ou slides narrados.
3. Voz inteligível pt-BR, texto legível em tela pequena, boca e expressão coerentes, mãos e celular sem distorções graves.
4. Verificação técnica H.264/AAC, vertical, 30 fps, duração e áudio, além de revisão do próprio MP4.
5. Verificação no Metricool da inexistência de duplicatas, limite gratuito, identificação nativa IA, autoPublish e datas futuras.
6. Só então religar geração semanal e agendamento; até lá o workflow anterior gerar-videos.yml permanece sem cron e a rotina acompanha o projeto sem postar.

Links internos: public/pilotos/piloto_personagem_cinematica.mp4 | public/pilotos/personagem_cinematica_preview.jpg | scripts/piloto_visual_personagem.py
