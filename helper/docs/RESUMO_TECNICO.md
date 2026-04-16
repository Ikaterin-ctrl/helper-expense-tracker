# Helper - Resumo Técnico do Projeto

## Visão Geral

Sistema completo de gerenciamento de despesas pessoais com integração WhatsApp, Google Sheets e interface Windows.

## Arquitetura

### Componentes Principais

```
┌─────────────────┐
│   WhatsApp      │
│  (Evolution API)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐      ┌──────────────┐
│  Backend Flask  │◄────►│ Google Sheets│
│   (HostGator)   │      │     API      │
└────────┬────────┘      └──────────────┘
         │
         ▼
┌─────────────────┐
│ Widget Windows  │
│  (CustomTkinter)│
└─────────────────┘
```

### Fluxo de Dados

1. **Entrada**: Usuário envia mensagem/foto via WhatsApp
2. **Webhook**: Evolution API encaminha para Flask
3. **Processamento**: 
   - Texto: Parser extrai gastos
   - Imagem: OCR extrai valores
4. **Validação**: Verifica duplicatas e dados obrigatórios
5. **Armazenamento**: Grava no Google Sheets
6. **Resposta**: Helper confirma via WhatsApp
7. **Auditoria**: Widget monitora e alerta

## Módulos Backend

### 1. app.py (349 linhas)
**Responsabilidade**: Aplicação Flask principal e webhook

**Endpoints**:
- `POST /webhook`: Recebe mensagens do WhatsApp
- `POST /audit`: Executa auditoria manual
- `GET /health`: Health check

**Funções principais**:
- `is_authorized()`: Valida número autorizado
- `send_whatsapp_message()`: Envia resposta via Evolution API
- `process_text_message()`: Processa mensagens de texto
- `process_image_message()`: Processa imagens com OCR

### 2. sheets_manager.py (302 linhas)
**Responsabilidade**: Integração com Google Sheets API

**Métodos principais**:
- `ensure_current_month_exists()`: Cria aba do mês se não existir
- `add_expense()`: Adiciona gasto na planilha
- `get_all_expenses()`: Retorna todos os gastos
- `get_expenses_by_category()`: Agrupa por categoria
- `check_duplicate()`: Verifica duplicatas

**Estrutura da planilha**:
```
Data | Descrição | Categoria | Valor | Forma_Pagamento | Observações
```

### 3. ocr_engine.py (213 linhas)
**Responsabilidade**: Processamento de imagens com Tesseract OCR

**Métodos principais**:
- `process_image()`: Extrai texto da imagem
- `extract_expenses()`: Identifica gastos no texto
- `_guess_category()`: Categoriza automaticamente
- `validate_receipt()`: Valida se é recibo válido

**Padrões reconhecidos**:
- `R$ 10,50`
- `10.50`
- `R$10,50`

### 4. auditor.py (281 linhas)
**Responsabilidade**: Auditoria mensal e detecção de anomalias

**Verificações**:
- Gastos recorrentes faltantes
- Aumentos > 30%
- Duplicatas
- Dados incompletos
- Contas a vencer

**Métodos principais**:
- `run_audit()`: Executa auditoria completa
- `check_upcoming_bills()`: Verifica vencimentos
- `get_summary()`: Gera resumo estatístico

### 5. message_processor.py (258 linhas)
**Responsabilidade**: Parser de mensagens do WhatsApp

**Formatos suportados**:
- `Descrição Valor`
- `Descrição1 Valor1, Descrição2 Valor2`
- `Ontem: Descrição Valor`
- `DD/MM: Descrição Valor`

**Métodos principais**:
- `parse_message()`: Extrai gastos da mensagem
- `_extract_custom_date()`: Identifica datas retroativas
- `_guess_category()`: Categorização automática

### 6. messages.py (177 linhas)
**Responsabilidade**: Mensagens com personalidade esdrúxula

**Tipos de mensagem**:
- Confirmações de registro
- Alertas de auditoria
- Erros e validações
- Ajuda e instruções

**Características**:
- Tom sarcástico mas construtivo
- Linguagem inclusiva
- Evita termos técnicos
- Mensagens aleatórias (variação)

## Widget Windows

### helper_ui.pyw (349 linhas)
**Responsabilidade**: Interface gráfica e notificações

**Componentes**:
- Frame scrollável de alertas
- Botões de ação (Verificar/Auditar)
- Status bar
- Notificações do sistema

**Funcionalidades**:
- Verificação automática periódica (30 min)
- Alertas coloridos por severidade
- Threading para não bloquear UI
- Notificações Windows nativas

## Tecnologias e Dependências

### Backend
```python
Flask==3.0.0                    # Framework web
gspread==5.12.0                 # Google Sheets API
pytesseract==0.3.10             # OCR
requests==2.31.0                # HTTP client
python-dotenv==1.0.0            # Variáveis de ambiente
pytz==2023.3                    # Timezone
```

### Widget
```python
customtkinter==5.2.1            # UI moderna
plyer==2.1.0                    # Notificações sistema
```

## Segurança

### Autenticação
- **Whitelisting**: Apenas 3 números autorizados
- **API Key**: Webhook protegido
- **Service Account**: Credenciais Google isoladas

### Dados Sensíveis
- `.env`: Variáveis de ambiente (gitignored)
- `google_credentials.json`: Credenciais Google (gitignored)
- Sem armazenamento local de dados financeiros

### Validações
- Número de origem verificado em cada mensagem
- Valores numéricos validados
- Datas validadas
- Duplicatas detectadas

## Performance

### Otimizações HostGator
- Stateless: Sem sessões ou cache local
- Processamento rápido: < 2s por mensagem
- Batch operations: Múltiplos gastos em uma request
- Lazy loading: Conecta Google Sheets sob demanda

### Limites
- CPU compartilhada: Evita operações pesadas
- Timeout: 30s máximo por request
- Imagens: Máximo 5MB
- Mensagens: Até 10 gastos por vez

## Categorização Automática

### Palavras-chave por Categoria

**Alimentação**: mercado, padaria, restaurante, café, bar, pizza, ifood
**Transporte**: gasolina, uber, taxi, ônibus, estacionamento, pedagio
**Saúde**: farmácia, médico, consulta, exame, hospital, dentista
**Moradia**: aluguel, luz, água, internet, condomínio, iptu
**Lazer**: cinema, netflix, spotify, show, viagem, hotel
**Vestuário**: roupa, sapato, loja, shopping
**Educação**: livro, curso, escola, faculdade
**Beleza**: salão, manicure, barbeiro, perfume
**Pets**: veterinário, ração, pet
**Serviços**: lavanderia, conserto, limpeza

**Padrão**: "Outros" se não reconhecer

## Auditoria - Regras de Negócio

### 1. Gastos Faltantes
- Compara categorias do mês atual vs anterior
- Alerta se categoria recorrente não apareceu
- Severidade: Média

### 2. Aumentos Suspeitos
- Calcula variação percentual por categoria
- Alerta se > 30% (configurável)
- Severidade: Alta (>50%) ou Média (30-50%)

### 3. Duplicatas
- Compara: descrição + valor + data
- Tolerância: 1 centavo
- Severidade: Alta

### 4. Dados Incompletos
- Verifica: data, descrição, valor, categoria
- Valor <= 0 considerado inválido
- Severidade: Alta (sem valor) ou Média (outros)

### 5. Contas a Vencer
- Compara dia do mês com gastos recorrentes
- Alerta 7 dias antes
- Severidade: Alta (hoje/amanhã) ou Média (2-7 dias)

## Estrutura de Alertas

```python
{
    'tipo': 'gasto_faltante' | 'aumento_suspeito' | 'gasto_duplicado' | 'dados_incompletos',
    'severidade': 'alta' | 'media' | 'baixa',
    'categoria': str,
    'valor_anterior': float,  # se aplicável
    'valor_atual': float,     # se aplicável
    'percentual': float,      # se aplicável
    'campos_faltantes': list  # se aplicável
}
```

## Deploy HostGator

### Requisitos
- Python 3.9+
- cPanel com Python App
- 512MB RAM mínimo
- SSL/HTTPS recomendado

### Estrutura no Servidor
```
/home/usuario/helper/
├── backend/
├── config/
│   ├── .env
│   └── google_credentials.json
├── requirements.txt
└── tmp/                    # Logs e temporários
```

### Configuração Python App
- Application root: `/home/usuario/helper`
- Startup file: `backend/app.py`
- Entry point: `app`
- Python version: 3.9+

## Monitoramento

### Logs
- Flask: stdout/stderr
- Erros: Capturados e retornados via WhatsApp
- Health check: `/health` endpoint

### Métricas
- Tempo de resposta: < 2s
- Taxa de sucesso: > 95%
- Uptime: Monitorado via health check

## Limitações Conhecidas

1. **OCR Gratuito**: Tesseract menos preciso que soluções pagas
2. **CPU Compartilhada**: Pode ter latência em horários de pico
3. **Apenas Despesas**: Sem controle de receitas
4. **3 Usuários**: Limite de números autorizados
5. **WhatsApp Dependente**: Requer Evolution API externa

## Melhorias Futuras

### Curto Prazo
- [ ] Logs estruturados (JSON)
- [ ] Retry automático em falhas
- [ ] Cache de categorias frequentes
- [ ] Backup automático da planilha

### Médio Prazo
- [ ] Dashboard web de visualização
- [ ] Gráficos de gastos
- [ ] Exportação PDF de relatórios
- [ ] Múltiplas planilhas (por usuário)

### Longo Prazo
- [ ] Machine Learning para previsão
- [ ] Integração Open Banking
- [ ] App mobile nativo
- [ ] Suporte a múltiplas moedas

## Manutenção

### Diária
- Verificar health check
- Monitorar alertas do widget

### Semanal
- Revisar logs de erro
- Validar dados na planilha

### Mensal
- Backup da planilha
- Atualizar dependências (se necessário)
- Revisar auditoria

### Anual
- Renovar credenciais Google (se necessário)
- Atualizar Evolution API
- Revisar e otimizar código

## Contato Técnico

**Desenvolvedor**: Bob
**Versão**: 1.0.0
**Data**: Abril 2026
**Licença**: Uso Pessoal

---

**Documentação Relacionada**:
- [README.md](../README.md) - Visão geral
- [INSTALACAO.md](INSTALACAO.md) - Guia de instalação
- [GUIA_USO.md](GUIA_USO.md) - Manual do usuário
- [INICIO_RAPIDO.md](INICIO_RAPIDO.md) - Setup rápido