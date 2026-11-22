# Direção criativa oficial — @metonalencar

## Atualização de 22/11/2026 — formato híbrido em avaliação

O usuário achou a prévia híbrida de Pix mais interessante que os testes anteriores e autorizou continuar a produção. O formato escolhido para testar agora preserva a MESMA apresentadora feminina CGI e combina aberturas/encerramentos com ela, animações demonstrativas de celular, alertas, cortes e narração neural pt-BR. Não confundir esta autorização para PRODUZIR com aprovação final para PUBLICAR; o usuário havia pedido para assistir aos novos vídeos antes.

Foi produzido em 22/11 no GitHub, sem postagem:
- Vídeo 02: public/pilotos/hibrido_02_senhas_diferentes.mp4, 90,6 s, 10 trechos, voz neural. Prévia hibrido_02_senhas_preview.jpg. Workflow hibrido-02-senhas.yml.
- Vídeo 03: public/pilotos/hibrido_03_permissoes_celular.mp4, 93,8 s, 10 trechos, voz neural. Prévia hibrido_03_preview.jpg. Workflow hibridos-03-04.yml.
- Vídeo 04: public/pilotos/hibrido_04_backup_fotos.mp4, 91,1 s, 10 trechos, voz neural. Prévia hibrido_04_preview.jpg. Workflow hibridos-03-04.yml.

Os três pilotos usam personagem CGI (imagem 2.5D) com demonstrações de interfaces móveis animadas, não atuação 3D cinematográfica e nem lip-sync profissional. A aparência da personagem segue a identidade. O usuário ainda precisa avaliar o vídeo completo, incluindo ritmo de cenas, áudio e clareza; os metadados continuam approved:false, scheduled:false e published:false.

**Próxima ação:** concluir um episódio 01 de Pix no mesmo formato híbrido (o Pix CGI 95,3 s de 08/11 não é automaticamente equivalente), inspecionar os quatro e, somente após aprovação de qualidade e confirmação de funcionamento da rotina, considerar publicação pelo Metricool sem duplicações. Não reativar a antiga geração de slides.

---

**Referência principal:** a arte de identidade do canal reenviada pelo usuário no chat em 01/11/2026 (painel rosa intitulado "IDENTIDADE DO CANAL / MASCOTE OFICIAL / ESTILO DOS VÍDEOS" e quatro exemplos Golpe do Pix, Senha por Conta, Permissões e Backup).
Esta referência prevalece sobre propostas posteriores de robô 2D, ícones e slides narrados.

## Personagem que deve aparecer no vídeo

- **Personagem feminina estilizada em animação 3D**, carismática, de aparência jovem adulta e traços expressivos.
- Cabelo castanho-escuro comprido, olhos grandes castanhos, expressão acolhedora e confiável; variar emoção de acordo com a situação (preocupação ao alertar, sorriso ao ensinar).
- Roupa marcante: moletom preto/cinza-escuro com acabamento rosa-pink e símbolo tecnológico rosa no peito. Manter identidade consistente entre vídeos.
- Iluminação cinematográfica rosa/magenta e azul/roxo, ambientes tecnológicos com profundidade e contraste para tela pequena.
- **Não substituir a personagem por um robô genérico**, boneco geométrico, carinha simples, cenas abstratas ou slides. A antiga "NEXO" robô 2D foi uma implementação divergente, não a referência visual autorizada.
- A imagem é um painel conceitual. Não usar o painel inteiro como vídeo nem repetir uma única imagem com zoom; os acontecimentos precisam ser realmente representados por planos distintos.

## Roteiro visual obrigatório

- Abertura de até 3 segundos com conflito visual imediato. Exemplos: celular vibra com pedido de Pix, personagem surpreende-se, mensagem suspeita aparece.
- Personagem apresenta e atua, gesticulando, olhando para celular e reagindo de maneira coerente; idealmente sincronização labial, não apenas boca oscilando sem fonemas.
- Mostrar o **objeto da dica** em ação: interface do celular, mensagens, QR Code, alerta, configurações; demonstrar antes/depois e consequências.
- Planos variados, cortes, zooms intencionais e mudanças visuais relevantes a cada ~2–4 segundos, sem trocar por trocar.
- Legendas dinâmicas curtas com palavras-chave e contraste alto; não usar grandes parágrafos.
- Final útil e direto; CTA sem prolongar vídeo artificialmente.
- Cada tema deve ter ilustrações específicas, não o mesmo cenário com texto ou ícone diferente.
- Preferir voz natural e inteligível pt-BR, com ritmo de conversa, não um monólogo de 2 minutos no mesmo plano.
- Duração baseada na narrativa e nas exigências do programa aplicável; não aumentar tempo com cenas vazias. Formato vertical 9:16, vídeo e áudio estáveis.

## Validação antes de qualquer publicação

1. Entregar **um piloto** com a personagem feminina 3D fiel à referência.
2. Inspecionar o MP4 *completo*, incluindo os 3 primeiros segundos, várias cenas intermediárias, legibilidade, movimentos e sincronia voz/cena.
3. O usuário deve ver e aprovar o piloto audiovisual. Somente depois adaptar o gerador semanal e retomar agendamento.
4. A aprovação de ffprobe, duração, H.264, "animated_segments" ou metadados de manifesto **não comprova** boa qualidade ou fidelidade visual.
5. O Metricool guarda uma cópia da mídia enviada: substituir vídeos no GitHub não substitui a mídia de posts já agendados. Verificar o post de destino.
6. Rótulo nativo de IA tiktokData.isAigc=true, evitar duplicação, cotas do plano gratuito e conteúdo original.

## Estado atual — 01/11/2026

- Slides narrados, robô 2D NEXO e protótipos 2D de Wi-Fi foram rejeitados por não corresponderem à referência.
- A geração semanal antiga deve ficar **desativada**, mantendo apenas execução manual para desenvolvimento e testes.
- A rotina de acompanhamento pode continuar, mas **nenhum agendamento novo ou publicação automática** até a aprovação explícita do novo piloto.
- O rascunho "Mais espaço sem apagar memórias" de 01/11 18h está com draft=true, autoPublish=false no Metricool.
- Não declarar que o novo formato 3D já está implementado. O código atual de Pillow/FFmpeg desenha formas 2D; ele é insuficiente para reproduzir essa referência sem novos recursos e animações.
- Não contratar serviços nem assumir que a geração de vídeo 3D/cenas cinematográficas completas esteja disponível gratuitamente sem validar ferramentas e limites.

## Proteção contra desvio de escopo

Este documento é a referência autoritativa em qualquer mudança de produção ou proposta criativa. Se o resultado for inviável com a pilha gratuita atual, informar a limitação e produzir uma prévia fiel para aprovação, nunca trocar a personagem ou estilo silenciosamente.
