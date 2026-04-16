# Helper - Guia de Assets Visuais

## Identidade Visual Dinâmica

O Helper possui expressões visuais que mudam de acordo com o contexto das mensagens e alertas.

## Estrutura de Assets

Todas as imagens devem ser colocadas na pasta:
```
widget/assets/
```

## Nomenclatura Obrigatória

As imagens devem seguir exatamente estes nomes para serem reconhecidas pelo sistema:

### 1. helper_standard.png
**Quando usar**: Expressão padrão/feliz
**Contextos**:
- Gastos registrados com sucesso
- Sistema funcionando normalmente
- Mensagens de confirmação
- Estado padrão do widget

**Personalidade**: Feliz, energético, animado

### 2. helper_alert.png
**Quando usar**: Alertas de atenção/pânico
**Contextos**:
- Contas vencendo hoje ou amanhã
- Lembretes urgentes
- Gastos recorrentes não lançados
- Notificações importantes

**Personalidade**: Preocupado, alerta, chamando atenção

### 3. helper_angry.png
**Quando usar**: Situações críticas/irritado
**Contextos**:
- Gastos aumentaram mais de 30%
- Auditoria com muitos problemas
- Gastos duplicados detectados
- Dados muito inconsistentes

**Personalidade**: Sério, irritado, crítico

### 4. helper_confused.png
**Quando usar**: Erros ou dados faltando
**Contextos**:
- Valor não informado na mensagem
- Descrição faltando
- Data inválida
- Mensagem não compreendida
- Erros de processamento

**Personalidade**: Confuso, perdido, questionador

## Especificações Técnicas

### Formato
- **Tipo**: PNG (com transparência)
- **Tamanho recomendado**: 128x128 pixels
- **Resolução**: 72 DPI mínimo
- **Fundo**: Transparente (alpha channel)

### Estilo Visual
- Cartoon/ilustração
- Cores vibrantes
- Expressões exageradas (esdrúxulo)
- Consistência entre todas as expressões
- Reconhecível como o mesmo personagem

## Mapeamento de Contextos

### Backend → Mood

```python
# Confirmações (standard)
"gasto_registrado" → mood="standard"
"multiplos_gastos" → mood="standard"
"ocr_sucesso" → mood="standard"

# Alertas (alert)
"conta_vencendo" → mood="alert"
"gasto_faltando" → mood="alert"

# Crítico (angry)
"aumento_suspeito" → mood="angry"
"auditoria_problemas" → mood="angry"
"gasto_duplicado" → mood="angry"

# Erros (confused)
"dados_incompletos" → mood="confused"
"ocr_falha" → mood="confused"
"erro_generico" → mood="confused"
```

## Fallback System

O sistema possui proteção contra imagens faltantes:

1. **Primeira tentativa**: Carrega a imagem específica do mood
2. **Fallback**: Se não encontrar, usa `helper_standard.png`
3. **Último recurso**: Se nenhuma imagem existir, widget funciona sem ícone

## Como Adicionar Novas Expressões

### 1. Criar a Imagem
Siga as especificações técnicas acima.

### 2. Nomear Corretamente
Use o padrão: `helper_[nome].png`

### 3. Adicionar ao Código
Edite `widget/helper_ui.pyw`:

```python
# Adicione o novo mood no dicionário
MOOD_IMAGES = {
    'standard': 'helper_standard.png',
    'alert': 'helper_alert.png',
    'angry': 'helper_angry.png',
    'confused': 'helper_confused.png',
    'novo_mood': 'helper_novo_mood.png'  # Nova expressão
}
```

### 4. Mapear Contextos
Edite `backend/messages.py` para retornar o novo mood quando apropriado.

## Exemplos de Uso

### No Widget
```python
# Alerta com expressão de pânico
self.add_alert(
    title="Conta Vencendo!",
    message="Aluguel vence hoje!",
    severity="alta",
    mood="alert"  # Usa helper_alert.png
)
```

### No Backend
```python
# Ao processar mensagem
if valor_faltando:
    mood = "confused"
    message = helper_messages.dados_incompletos('valor')
    send_notification(message, mood)
```

## Checklist de Implementação

- [ ] Criar 4 imagens base (standard, alert, angry, confused)
- [ ] Salvar na pasta `widget/assets/`
- [ ] Verificar nomenclatura exata
- [ ] Testar cada expressão no widget
- [ ] Confirmar fallback funciona

## Dicas de Design

### Helper Standard (Feliz)
- Sorriso largo
- Olhos brilhantes
- Postura animada
- Cores quentes (amarelo, laranja)

### Helper Alert (Alerta)
- Olhos arregalados
- Boca em "O"
- Mãos levantadas
- Cores de atenção (amarelo, laranja)

### Helper Angry (Irritado)
- Sobrancelhas franzidas
- Boca séria/carrancuda
- Postura rígida
- Cores intensas (vermelho, roxo)

### Helper Confused (Confuso)
- Olhos semicerrados
- Boca torta
- Mão na cabeça/coçando
- Cores neutras (azul, cinza)

## Ferramentas Recomendadas

### Para Criar
- Adobe Illustrator
- Figma
- Procreate
- Canva (templates)

### Para Editar
- Photoshop
- GIMP (gratuito)
- Paint.NET (gratuito)

### Para Gerar (IA)
- DALL-E
- Midjourney
- Stable Diffusion
- Leonardo.ai

## Prompt Sugerido para IA

```
Create a cartoon character mascot for a personal finance app called "Helper". 
The character should be an enthusiastic office assistant from the 2000s era, 
with an exaggerated happy expression. Style: flat design, vibrant colors, 
transparent background, 128x128px. The character should look friendly but 
slightly sarcastic. PNG format with alpha channel.

Variations needed:
1. Standard/Happy - big smile, bright eyes
2. Alert/Panic - wide eyes, mouth open in surprise
3. Angry/Serious - furrowed brows, stern expression
4. Confused/Lost - tilted head, questioning look
```

## Manutenção

### Atualizar Imagens
1. Substitua o arquivo PNG na pasta `assets/`
2. Mantenha o mesmo nome
3. Reinicie o widget para ver mudanças

### Adicionar Variações
1. Crie nova imagem seguindo padrão
2. Adicione ao código (ver seção "Como Adicionar")
3. Documente o novo mood neste guia

## Troubleshooting

### Imagem não aparece
- Verifique o nome do arquivo (case-sensitive)
- Confirme que está na pasta `widget/assets/`
- Verifique formato PNG
- Reinicie o widget

### Imagem distorcida
- Redimensione para 128x128px
- Mantenha proporção 1:1
- Use fundo transparente

### Cores estranhas
- Salve em modo RGB (não CMYK)
- Use perfil de cor sRGB
- Verifique transparência (alpha)

## Recursos Adicionais

- **Paleta de cores**: Use cores consistentes entre expressões
- **Estilo**: Mantenha mesmo estilo de traço
- **Tamanho**: Todas as imagens devem ter dimensões idênticas
- **Formato**: Sempre PNG com transparência

---

**Importante**: As imagens são essenciais para a identidade visual do Helper. Invista tempo criando expressões que realmente transmitam a personalidade esdrúxula do assistente!