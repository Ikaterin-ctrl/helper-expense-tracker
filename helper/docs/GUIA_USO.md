# Helper - Guia de Uso

## Índice
1. [Visão Geral](#visão-geral)
2. [Usando o WhatsApp](#usando-o-whatsapp)
3. [Formatos de Mensagem](#formatos-de-mensagem)
4. [Widget Windows](#widget-windows)
5. [Auditoria Mensal](#auditoria-mensal)
6. [Dicas e Boas Práticas](#dicas-e-boas-práticas)

---

## Visão Geral

O Helper é seu assistente pessoal de gastos com personalidade esdrúxula. Ele:
- Registra gastos via WhatsApp
- Processa fotos de recibos automaticamente
- Alerta sobre contas a vencer
- Audita seus gastos mensalmente
- Identifica aumentos suspeitos e gastos duplicados

---

## Usando o WhatsApp

### Números Autorizados

Apenas 3 números podem usar o Helper:
- Catarina: 19 99348-8882
- Flávio: 19 98368-0292
- Pai: 19 98368-0308

### Comandos Básicos

#### Registrar um Gasto Simples
```
Padaria 20
```
Resposta do Helper:
> "Surpresa! Anotei seu gasto de R$ 20,00 com Padaria. Mais um tijolinho no muro das contas!"

#### Registrar Múltiplos Gastos
```
Padaria 20, Gasolina 250, Farmácia 80
```
Resposta do Helper:
> "Uau! 3 gastos de uma vez só! Total de R$ 350,00. Você é eficiente em gastar, hein?"

#### Gasto com Data Retroativa
```
Ontem: Cinema 40
```
ou
```
15/04: Restaurante 120
```

#### Pedir Ajuda
```
Ajuda
```
ou
```
Como usar
```

---

## Formatos de Mensagem

### Formato Básico
```
Descrição Valor
```

Exemplos:
- `Supermercado 150`
- `Uber 25`
- `Netflix 39.90`

### Com Cifrão (Opcional)
```
Descrição R$ Valor
```

Exemplos:
- `Aluguel R$ 1200`
- `Luz R$ 180,50`

### Múltiplos Gastos (Separados por Vírgula)
```
Descrição1 Valor1, Descrição2 Valor2, Descrição3 Valor3
```

Exemplo:
```
Café 15, Almoço 35, Jantar 40
```

### Com Data Customizada
```
Data: Descrição Valor
```

Formatos de data aceitos:
- `Ontem: Descrição Valor`
- `Anteontem: Descrição Valor`
- `15/04: Descrição Valor`
- `15/04/2026: Descrição Valor`

### Enviando Foto de Recibo

1. Tire uma foto clara do recibo
2. Envie a foto pelo WhatsApp
3. O Helper processará automaticamente e extrairá os valores
4. Você receberá confirmação dos itens registrados

**Dicas para fotos:**
- Boa iluminação
- Foco no texto
- Recibo completo visível
- Evite sombras e reflexos

---

## Widget Windows

### Funcionalidades

O widget mostra em tempo real:
- Contas próximas do vencimento
- Gastos duplicados
- Dados incompletos na planilha
- Aumentos suspeitos de categorias
- Gastos recorrentes faltantes

### Botões

#### Verificar Agora
Executa verificação manual imediata de todos os alertas.

#### Auditar Mês
Executa auditoria completa comparando mês atual com anterior.

### Cores dos Alertas

- **Vermelho**: Severidade alta (ação imediata necessária)
- **Laranja**: Severidade média (atenção recomendada)
- **Amarelo**: Severidade baixa (informativo)
- **Azul**: Informações gerais

### Notificações do Sistema

O widget envia notificações do Windows para:
- Contas vencendo hoje ou amanhã
- Alertas de alta severidade
- Resumo de auditoria

---

## Auditoria Mensal

### O que o Auditor Verifica

#### 1. Gastos Faltantes
Identifica categorias que apareceram no mês anterior mas não no atual.

Exemplo:
> "Ei! Cadê o gasto de Aluguel deste mês? No mês passado você lançou. Esqueceu ou tá sobrando dinheiro?"

#### 2. Aumentos Suspeitos (>30%)
Alerta quando uma categoria aumenta mais de 30% em relação ao mês anterior.

Exemplo:
> "EITAAAA! Alimentação subiu 45%! Era R$ 800,00, agora é R$ 1.160,00. Explica isso!"

#### 3. Gastos Duplicados
Detecta lançamentos idênticos (mesma descrição, valor e data).

Exemplo:
> "Peraí! Já vi esse gasto de Farmácia (R$ 50,00) em 15/04/2026. Lançou duas vezes ou gastou de novo?"

#### 4. Dados Incompletos
Identifica linhas sem data, descrição ou valor.

Exemplo:
> "Opa! Cadê o valor? Eu sou bom, mas não sou vidente! Me diz quanto gastou, vai?"

### Quando a Auditoria Roda

- **Automática**: A cada 24 horas (configurável)
- **Manual**: Via widget (botão "Auditar Mês")
- **Via API**: POST para `/audit`

### Relatório de Auditoria

O relatório inclui:
- Total de gastos do mês atual
- Total de gastos do mês anterior
- Variação percentual
- Número de alertas por severidade
- Detalhes de cada alerta

---

## Dicas e Boas Práticas

### Registro de Gastos

1. **Registre Imediatamente**
   - Anote o gasto assim que acontecer
   - Use o WhatsApp mesmo na rua

2. **Seja Específico**
   - Em vez de "Compras 200", use "Supermercado 200"
   - Ajuda na categorização automática

3. **Use Fotos**
   - Para recibos com múltiplos itens
   - Mais rápido que digitar tudo

4. **Revise Semanalmente**
   - Abra a planilha e confira
   - Corrija categorizações se necessário

### Categorias Automáticas

O Helper categoriza automaticamente baseado em palavras-chave:

- **Alimentação**: mercado, padaria, restaurante, café, bar
- **Transporte**: gasolina, uber, taxi, ônibus, estacionamento
- **Saúde**: farmácia, médico, consulta, exame
- **Moradia**: aluguel, luz, água, internet, condomínio
- **Lazer**: cinema, show, netflix, spotify
- **Vestuário**: roupa, sapato, loja
- **Educação**: livro, curso, escola
- **Beleza**: salão, manicure, perfume
- **Pets**: veterinário, ração
- **Serviços**: lavanderia, conserto, limpeza

Se não reconhecer, categoriza como "Outros".

### Contas Recorrentes

Para contas mensais fixas:
1. Registre sempre no mesmo dia
2. Use descrição consistente
3. O Helper aprenderá o padrão
4. Receberá alertas se esquecer

### Organização da Planilha

- **Não delete abas antigas**: Necessárias para comparação
- **Não altere o cabeçalho**: Sistema depende dele
- **Pode adicionar colunas extras**: Após a coluna "Observações"
- **Pode colorir células**: Não afeta o sistema

### Limites e Restrições

- **Valor mínimo**: R$ 0,01
- **Valor máximo**: Sem limite (mas valores muito altos geram alerta)
- **Descrição**: Até 50 caracteres
- **Múltiplos gastos**: Até 10 por mensagem
- **Fotos**: Máximo 5MB, formatos JPG/PNG

### Privacidade e Segurança

- Apenas 3 números autorizados
- Credenciais Google criptografadas
- Dados armazenados apenas no Google Sheets
- Sem compartilhamento com terceiros
- Webhook protegido por API Key

---

## Exemplos de Uso Real

### Dia a Dia
```
# Manhã
Padaria 8.50

# Almoço
Restaurante 35

# Tarde
Uber 15, Farmácia 42.90

# Noite
Supermercado 156.80
```

### Fim de Semana
```
# Sábado
Cinema 40, Pipoca 25, Jantar 120

# Domingo
Churrasco 180, Bebidas 85
```

### Contas Mensais
```
# Dia 5
Aluguel 1200

# Dia 10
Luz 180, Água 90, Internet 120

# Dia 15
Condomínio 350
```

### Gastos Retroativos
```
# Esqueceu de anotar ontem
Ontem: Posto 250, Lanche 15

# Esqueceu de anotar semana passada
10/04: Médico 200
```

---

## Mensagens do Helper

### Confirmações
- "Surpresa! Anotei seu gasto..."
- "Eba! R$ X devidamente registrado..."
- "Maravilha! Gastou R$ X com..."

### Alertas
- "Ei! Cadê o gasto de..."
- "EITAAAA! X subiu Y%..."
- "Peraí! Já vi esse gasto..."

### Erros
- "Opa! Cadê o valor?..."
- "Faltou me dizer o que foi..."
- "Eita! Deu algum problema..."

### Ajuda
- "Oi! Sou o Helper, seu assistente..."
- Instruções completas de uso

---

## Solução de Problemas

### Helper não responde
1. Verifique se seu número está autorizado
2. Confirme que a Evolution API está online
3. Teste com "Ajuda"

### Gasto não foi registrado
1. Verifique o formato da mensagem
2. Confirme que incluiu o valor
3. Tente novamente com formato simples: "Descrição Valor"

### Categoria errada
1. Edite manualmente na planilha
2. Use descrição mais específica na próxima vez

### OCR não funcionou
1. Tire foto mais clara
2. Certifique-se que o recibo está legível
3. Como alternativa, digite manualmente

### Widget não abre
1. Verifique se Python está instalado
2. Confirme que as dependências foram instaladas
3. Execute `pythonw widget\helper_ui.pyw` manualmente

---

## Contato e Suporte

Para dúvidas sobre o sistema:
1. Consulte esta documentação
2. Verifique o arquivo INSTALACAO.md
3. Revise os logs de erro

O Helper está sempre aprendendo e melhorando!