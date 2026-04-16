# Helper Assets - Imagens de Expressões

## Pasta de Assets

Esta pasta contém as imagens das expressões do Helper que mudam dinamicamente conforme o contexto.

## Imagens Necessárias

Coloque as seguintes imagens nesta pasta:

### 1. helper_standard.png
**Expressão**: Feliz/Padrão
**Quando aparece**:
- Gastos registrados com sucesso
- Sistema funcionando normalmente
- Auditoria sem problemas

### 2. helper_alert.png
**Expressão**: Alerta/Preocupado
**Quando aparece**:
- Contas vencendo (hoje ou amanhã)
- Gastos recorrentes não lançados
- Lembretes importantes

### 3. helper_angry.png
**Expressão**: Irritado/Sério
**Quando aparece**:
- Gastos aumentaram mais de 30%
- Gastos duplicados detectados
- Auditoria com muitos problemas

### 4. helper_confused.png
**Expressão**: Confuso/Perdido
**Quando aparece**:
- Valor não informado
- Dados incompletos
- Erros de processamento
- OCR falhou

## Especificações Técnicas

- **Formato**: PNG com transparência
- **Tamanho**: 128x128 pixels (recomendado)
- **Fundo**: Transparente
- **Estilo**: Consistente entre todas as expressões

## Como Criar as Imagens

1. Use ferramentas de design (Figma, Illustrator, Canva)
2. Ou gere com IA (DALL-E, Midjourney, Leonardo.ai)
3. Mantenha o mesmo personagem em todas as expressões
4. Exagere as expressões (personalidade esdrúxula!)

## Prompt Sugerido para IA

```
Create a cartoon character mascot for a personal finance app called "Helper".
The character should be an enthusiastic office assistant from the 2000s era.
Style: flat design, vibrant colors, transparent background, 128x128px.

Create 4 variations:
1. Standard/Happy - big smile, bright eyes, energetic pose
2. Alert/Panic - wide eyes, mouth open in surprise, worried expression
3. Angry/Serious - furrowed brows, stern expression, arms crossed
4. Confused/Lost - tilted head, questioning look, hand on head

PNG format with alpha channel, same character in all variations.
```

## Fallback

Se uma imagem específica não for encontrada, o sistema usa `helper_standard.png` como padrão.

Se nenhuma imagem existir, o widget funciona normalmente sem ícone.

## Testando

Após adicionar as imagens:
1. Reinicie o widget
2. Teste cada tipo de alerta
3. Verifique se a expressão muda corretamente

## Documentação Completa

Veja `docs/ASSETS_GUIDE.md` para informações detalhadas sobre o sistema de moods.