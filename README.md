# TikTok IA — @metonalencar

Projeto de vídeos educativos originais, sem uso de imagem ou voz real do titular, gerados com ferramentas gratuitas no GitHub Actions.

## Rejeição do formato publicado (01/11/2026)
- O usuário verificou que o post publicado sobre Wi-Fi público ainda era um slide narrado e rejeitou tanto esse modelo quanto mudanças cosméticas de ícones e robôs pequenos. Metadados B+ e testes de codec não comprovam valor criativo.
- O modelo novo exige HISTÓRIA VISUAL: encenação da situação, elementos e pessoas/personagens que ajam na tela, enquadramentos distintos e cortes visuais frequentes, legendas breves e ligação direta entre fala e cena.
- NÃO agendar novos vídeos automaticamente até o usuário avaliar um piloto audiovisual realmente melhor. No Metricool, 01/11/2026, `Mais espaço sem apagar memórias` foi colocado em rascunho, autoPublish=false. A inteligibilidade da narração é condição de aprovação, não basta MP4 com áudio válido.
- A publicação do Metricool usa uma cópia da mídia enviada quando agendada; mudar `public/` no GitHub não substitui essa cópia. Necessário revisar a mídia do POST real antes de publicar.
- Prototipagem experimental fora do agendador; piloto ilustrativo de cenas com duas redes, atendente, configuração e personagem criado em 01/11/2026. Não apresentar o piloto como vídeo cinematográfico ou aprovado.

## Piloto funcional com voz neural (01/11/2026)
- Primeira geração integrada validada no GitHub Actions: [execução 41311957813](https://github.com/metonalencar21/meton-tiktok-ia/actions/runs/41311957813).
- Vídeo para escuta e avaliação: [Cuidado com a voz clonada — piloto](https://github.com/metonalencar21/meton-tiktok-ia/blob/main/public/pilotos/voz-falsa-piloto.mp4), 84 segundos, Edge TTS pt-BR, voz Francisca.
- Novo formato técnico: `STORY 2D CENAS HUMANAS`, com personagem ilustrado, encenações de telefone/áudio/Pix e alternância de tomadas. Ainda não é produção cinematográfica; aceitação depende de avaliação humana.
- A falha de `edge-tts` era sintaxe de argumento negativo: usar `--rate=-12%` em vez de `--rate -12%`. A falha histórica de gravação foi conflito de rebase de arquivos MP4; o gerador atual evita esse rebase.
- Não há postagem automática: piloto salvo somente no GitHub. O rascunho no Metricool continua desativado até aprovação de qualidade.

## Identidade visual B+ (26/10/2026)
- Mascote digital oficial: **NEXO** (robô expressivo, neutro e amigável, rosa neon + turquesa sobre azul-marinho).
- Renderizador: `scripts/visual_bplus.py`; animações contínuas da mascote, olhos, boca e ícones ilustrados.
- Textos na tela são legendas curtas e mudam entre frases narradas; o vídeo não deve ficar em slides estáticos.
- Estética: vídeo vertical com cenas temáticas, contraste legível e movimentos frequentes. A marca continua `METON DIGITAL` e @metonalencar.
- O piloto curto foi testado localmente; a rotina automática roda a validação `Validar piloto B+ NEXO` e gera a nova versão a partir de `scripts/produce.py`. A versão com a nova voz ainda precisa de escuta real.
- **Este renderizador é 2D programático e gratuito, não um serviço de vídeo generativo cinematográfico ou lip sync realista.** A boca acompanha ritmo aproximado, não fonemas exatos.
- Não alterar mídia já copiada e programada no Metricool; para próximas semanas, validar o manifesto `visual_format` e `animated_segments` antes de agendar. O campo `quality_review_required=true` exige avaliação de qualidade.


## Duração e potencial de monetização (01/11/2026)
- Objetivo editorial: cerca de 75 a 110 segundos de conteúdo real e envolvente, com início forte, dicas contextualizadas e encerramento conciso. Não alongar artificialmente.
- Regra técnica: nunca aceitar áudio nem vídeo com menos de 70 segundos; 70s é margem interna acima da exigência do TikTok de mais de um minuto. Marcar vídeos acima de 110s para revisão de retenção, sem truncar informação.
- Duração **não garante monetização**. O Programa de Recompensas do Criador exige originalidade, qualidade, elegibilidade da conta e visualizações qualificadas; a aceitação definitiva é decidida pelo TikTok.
- Narração inteligível e história visual são condições de revisão obrigatória. Manter rascunhos sem publicação automática até aprovação do piloto.

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
- scripts/produce.py: exige voz neural Edge TTS em português do Brasil (Francisca), a -12% de velocidade, com pausas reais entre blocos e volume normalizado. Não há fallback gTTS/eSpeak: se falhar, não há vídeo novo.
- scripts/visual_bplus.py: mascote NEXO, desenhos temáticos animados e legendas dinâmicas.
- topics.json: 24 roteiros educativos originais para seis semanas; novas pautas são necessárias depois.
- tests/test_bank.py e tests/verify_videos.py: validações automáticas de roteiros e mídia.
- requirements.txt: dependências Python.

## Avisos
- Não inclua chaves, senhas, tokens, dados pessoais nem documentos privados neste repositório público.
- Conteúdo com IA precisa ser identificado: o Metricool deve receber tiktokData.isAigc=true nos posts com vídeo.
- Vídeos de slides podem ser considerados insuficientes para programas de monetização, mesmo com mais de um minuto. Ganhos e elegibilidade não são garantidos.
- Não duplique posts e não compre serviços ou créditos automaticamente.
