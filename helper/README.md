# Helper - Agente de Curadoria de Despesas

> Seu assistente esdrúxulo de gastos pessoais com integração WhatsApp, Google Sheets e notificações Windows

## Visão Geral

O Helper é um sistema completo de gerenciamento de despesas pessoais que combina:
- **WhatsApp**: Interface principal para registro de gastos
- **Google Sheets**: Armazenamento e organização dos dados
- **OCR**: Processamento automático de fotos de recibos
- **Auditoria Inteligente**: Comparação mensal e detecção de anomalias
- **Widget Windows**: Notificações em tempo real

### Características Principais

- Registro rápido via mensagem de texto
- Suporte a múltiplos gastos em uma mensagem
- Processamento automático de imagens (OCR)
- Categorização automática inteligente
- Detecção de gastos duplicados
- Alertas de contas a vencer
- Auditoria mensal com comparação de 30%
- Personalidade esdrúxula e divertida
- **Expressões visuais dinâmicas** (muda conforme contexto)

## Arquitetura

```
helper/
├── backend/              # Backend Flask
│   ├── app.py           # Aplicação principal e webhook
│   ├── sheets_manager.py # Integração Google Sheets
│   ├── ocr_engine.py    # Processamento de imagens
│   ├── auditor.py       # Auditoria mensal
│   ├── message_processor.py # Parser de mensagens
│   └── messages.py      # Mensagens do Helper
├── widget/              # Interface Windows
│   └── helper_ui.pyw    # Widget de notificações
├── config/              # Configurações
│   ├── .env.example     # Template de variáveis
│   └── google_credentials.json # Credenciais Google
├── docs/                # Documentação
│   ├── INSTALACAO.md    # Guia de instalação
│   └── GUIA_USO.md      # Guia de uso
└── requirements.txt     # Dependências Python
```

## Tecnologias

### Backend
- **Flask**: Framework web Python
- **gspread**: Integração Google Sheets API
- **pytesseract**: OCR para processamento de imagens
- **requests**: Comunicação com Evolution API

### Frontend (Widget)
- **CustomTkinter**: Interface gráfica moderna
- **plyer**: Notificações do sistema Windows

### Integrações
- **Evolution API**: WhatsApp Business API
- **Google Sheets API**: Armazenamento de dados
- **Tesseract OCR**: Reconhecimento de texto em imagens

## Início Rápido

### 1. Pré-requisitos

- Python 3.9+
- Tesseract OCR
- Conta Google (para Sheets)
- Evolution API configurada

### 2. Instalação

```powershell
# Clone ou baixe o projeto
cd helper

# Crie ambiente virtual
python -m venv venv
.\venv\Scripts\activate

# Instale dependências
pip install -r requirements.txt
```

### 3. Configuração

```powershell
# Copie o template de configuração
copy config\.env.example config\.env

# Edite config/.env com suas credenciais
notepad config\.env
```

### 4. Execute

```powershell
# Backend
cd backend
python app.py

# Widget (em outro terminal)
pythonw widget\helper_ui.pyw
```

## Documentação Completa

- **[Guia de Instalação](docs/INSTALACAO.md)**: Configuração detalhada de todos os componentes
- **[Guia de Uso](docs/GUIA_USO.md)**: Como usar o sistema no dia a dia

## Exemplos de Uso

### Registro Simples
```
Padaria 20
```
> "Surpresa! Anotei seu gasto de R$ 20,00 com Padaria!"

### Múltiplos Gastos
```
Padaria 20, Gasolina 250, Farmácia 80
```
> "Uau! 3 gastos de uma vez só! Total de R$ 350,00!"

### Gasto Retroativo
```
Ontem: Cinema 40
```

### Foto de Recibo
Envie a foto pelo WhatsApp e o Helper processará automaticamente.

## Regras de Negócio

### Apenas Despesas
O sistema foi projetado exclusivamente para registro de gastos. Não há funcionalidade de entrada de valores ou fluxo de caixa positivo.

### Higiene de Dados
Cada gasto deve ter no mínimo:
- Data
- Descrição
- Valor

O Helper alerta imediatamente se algum dado faltar.

### Auditoria Mensal
O sistema compara automaticamente:
- Gastos recorrentes faltantes
- Aumentos superiores a 30%
- Duplicatas
- Dados incompletos

## Estrutura da Planilha

Cada mês tem uma aba própria (ex: `Abril_2026`) com o seguinte formato:

| Data | Descrição | Categoria | Valor | Forma_Pagamento | Observações |
|------|-----------|-----------|-------|-----------------|-------------|
| 15/04/2026 | Padaria | Alimentação | 20.00 | | |
| 15/04/2026 | Gasolina | Transporte | 250.00 | | |

## Segurança

- **Whitelisting**: Apenas 3 números autorizados
- **API Key**: Webhook protegido
- **Service Account**: Credenciais Google isoladas
- **Sem armazenamento local**: Dados apenas no Google Sheets

## Números Autorizados

- Catarina: 19 99348-8882
- Flávio: 19 98368-0292
- Pai: 19 98368-0308

## Personalidade do Helper

O Helper é uma caricatura de assistente de escritório dos anos 2000:
- Excessivamente feliz e energético
- Sarcasmo ácido mas construtivo
- Linguagem inclusiva e didática
- Evita termos técnicos

### Exemplos de Mensagens

**Confirmação:**
> "Maravilha! Gastou R$ 50,00 com café. Adoro ver o dinheiro indo embora... ops, digo, adoro organizar!"

**Alerta:**
> "Ei! Cadê o gasto do aluguel deste mês? O dono do imóvel não aceita sorrisos como pagamento, sabia?"

**Erro:**
> "Opa! Cadê o valor? Eu sou bom, mas não sou vidente! Me diz quanto gastou, vai?"

## Deploy

### HostGator (Produção)
Veja instruções detalhadas em [docs/INSTALACAO.md](docs/INSTALACAO.md#deploy-no-hostgator)

### Requisitos do Servidor
- Python 3.9+
- 512MB RAM mínimo
- Suporte a Python App (cPanel)
- SSL/HTTPS recomendado

## Limitações Conhecidas

- **HostGator Compartilhado**: CPU limitada, otimizado para execução rápida
- **OCR Gratuito**: Tesseract menos preciso que soluções pagas
- **WhatsApp**: Depende de Evolution API externa
- **Apenas Despesas**: Sem controle de receitas ou saldo

## Roadmap Futuro

- [ ] Gráficos de gastos por categoria
- [ ] Exportação de relatórios PDF
- [ ] Previsão de gastos com ML
- [ ] Integração com bancos (Open Banking)
- [ ] App mobile nativo
- [ ] Suporte a múltiplas moedas

## Contribuindo

Este é um projeto pessoal, mas sugestões são bem-vindas!

## Licença

Uso pessoal - Todos os direitos reservados

## Suporte

Para dúvidas:
1. Consulte a [documentação](docs/)
2. Verifique os logs de erro
3. Teste componentes isoladamente

---

**Desenvolvido com ☕ e 💻 por Bob para Catarina**

*"Porque controlar gastos não precisa ser chato!"*