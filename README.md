# TikTok IA — @metonalencar

Projeto de vídeos educativos originais, sem uso de imagem ou voz real do titular, gerados com ferramentas gratuitas no GitHub Actions.

## Identidade visual B+ (26/10/2026)
- Mascote digital oficial: **NEXO** (robô expressivo, neutro e amigável, rosa neon + turquesa sobre azul-marinho).
- Renderizador: `scripts/visual_bplus.py`; animações contínuas da mascote, olhos, boca e ícones ilustrados.
- Textos na tela são legendas curtas e mudam entre frases narradas; o vídeo não deve ficar em slides estáticos.
- Estética: vídeo vertical com cenas temáticas, contraste legível e movimentos frequentes. A marca continua `METON DIGITAL` e @metonalencar.
- O piloto curto foi testado localmente; a rotina automática roda a validação `Validar piloto B+ NEXO` e gera a nova versão a partir de `scripts/produce.py`.
- **Este renderizador é 2D programático e gratuito, não um serviço de vídeo generativo cinematográfico ou lip sync realista.** A boca acompanha ritmo aproximado, não fonemas exatos.
- Não alterar mídia já copiada e programada no Metricool; para próximas semanas, validar o manifesto `visual_format` e `animated_segments` antes de agendar. O campo `quality_review_required=true` exige avaliação de qualidade.


## Automação
- GitHub Actions gera quatro MP4 verticais H.264/AAC, com narração sintética, todos os domingos às 06h15 de Fortaleza (09h15 UTC).
- As mídias são salvas em public/videos/ANO-WNN/, e o arquivo public/manifest.json fornece título, legenda, data e URL da mídia.
- A rotina ChatGPT + Metricool tenta agendar os quatro vídeos semanalmente, após verificar arquivos, data, originalidade, limite gratuito e duplicação.
- O gerador não publica no TikTok sozinho. Agendamento é confirmado somente quando o Metricool responder com êxito.
- Horários iniciais: terça 18h, quinta 10h, sábado 10h e domingo 18h, em Fortaleza.

## Primeira execução
1. Abra Actions > Gerar videos TikTok IA e verifique se o fluxo foi executado após o envio dos arquivos.
2. Se necessário, toque em Run workflow.
3. Após o término, verifique public/manifest.json e os quatro vídeos disponíveis publicamente.
4. Se houver erro de gravação: Settings > Actions > General > Workflow permissions > Read and write permissions.

## Fontes
- scripts/produce.py: orquestra voz sintética (Edge TTS, gTTS ou fallback eSpeak) e o renderizador B+.
- scripts/visual_bplus.py: mascote NEXO, desenhos temáticos animados e legendas dinâmicas.
- topics.json: 24 roteiros educativos originais para seis semanas; novas pautas são necessárias depois.
- tests/test_bank.py e tests/verify_videos.py: validações automáticas de roteiros e mídia.
- requirements.txt: dependências Python.

## Avisos
- Não inclua chaves, senhas, tokens, dados pessoais nem documentos privados neste repositório público.
- Conteúdo com IA precisa ser identificado: o Metricool deve receber tiktokData.isAigc=true nos posts com vídeo.
- Vídeos de slides podem ser considerados insuficientes para programas de monetização, mesmo com mais de um minuto. Ganhos e elegibilidade não são garantidos.
- Não duplique posts e não compre serviços ou créditos automaticamente.
