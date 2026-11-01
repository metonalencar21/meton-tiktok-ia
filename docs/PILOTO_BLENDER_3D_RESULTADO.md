# Piloto Blender 3D — Resultado técnico de 01/11/2026

## Arquivos entregues
- MP4: [piloto 3D animado](../public/pilotos/piloto-3d-blender-animado.mp4).
- Miniatura com quatro quadros reais: [inspeção](../public/pilotos/piloto-3d-preview.jpg).
- Informações técnicas: [manifesto do piloto](../public/pilotos/piloto-3d-blender-animado.json).
- Código de animação: [scripts/blender_piloto.py](../scripts/blender_piloto.py).
- Workflow gratuito: [.github/workflows/testar-piloto-3d.yml](../.github/workflows/testar-piloto-3d.yml).

## Estado verificado

- O GitHub Actions completou o teste no plano gratuito.
- Blender Workbench montou geometria 3D, cabelo volumétrico, corpo, rosto, braços, celular e cenário, com keyframes de cabeça, boca, braços, câmera e aparelho.
- Render passou validação H.264/AAC 720x1280 30fps, voz neural pt-BR, duração 15,3 segundos, frames iniciais e finais distintos.
- A primeira tentativa falhou por biblioteca gráfica ausente; correção de libEGL e Xvfb validada na segunda execução.

## Avaliação visual (REPROVADO PARA PUBLICAÇÃO)

Os quatro quadros retirados do MP4 revelam aparência muito simplificada: rosto grande redondo, olhos e boca pouco naturais, mãos rudimentares, cenário de baixa complexidade. Embora seja uma cena 3D real, **não atende o acabamento cinematográfico e a personagem feminina 3D estilizada que o usuário escolheu**.

Este resultado não deve ser publicado nem tomado como piloto final do projeto. A automação semanal permanece suspensa.

## Próxima etapa de produção

Usar uma malha de personagem feminina 3D de alta qualidade e **rigada**, com licença adequada, adaptar cabelo castanho comprido, olhos, rosto e moletom preto/rosa, conectar gestos e interações à biblioteca de cenas. Não basta adicionar mais objetos geométricos ao modelo atual.

Só depois produzir novo piloto, inspecionar vídeo inteiro e obter aprovação visual explícita do usuário. Não comprar serviços nem ativar Metricool até essa aprovação.
