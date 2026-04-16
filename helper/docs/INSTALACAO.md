# Helper - Guia de Instalação e Configuração

## Índice
1. [Pré-requisitos](#pré-requisitos)
2. [Configuração do Google Sheets](#configuração-do-google-sheets)
3. [Configuração do WhatsApp (Evolution API)](#configuração-do-whatsapp-evolution-api)
4. [Instalação Local](#instalação-local)
5. [Deploy no HostGator](#deploy-no-hostgator)
6. [Configuração do Widget Windows](#configuração-do-widget-windows)
7. [Testes](#testes)

---

## Pré-requisitos

### Software Necessário
- Python 3.9 ou superior
- Tesseract OCR (para processamento de imagens)
- Git (opcional, para versionamento)

### Contas e Serviços
- Conta Google (para Google Sheets)
- Servidor para Evolution API (pode ser local ou VPS)
- Hospedagem HostGator (Plano Compartilhado)

---

## Configuração do Google Sheets

### 1. Criar Projeto no Google Cloud Console

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto chamado "Helper"
3. Ative as seguintes APIs:
   - Google Sheets API
   - Google Drive API

### 2. Criar Service Account

1. No menu lateral, vá em "IAM & Admin" > "Service Accounts"
2. Clique em "Create Service Account"
3. Nome: `helper-service-account`
4. Clique em "Create and Continue"
5. Role: "Editor"
6. Clique em "Done"

### 3. Gerar Credenciais JSON

1. Clique na service account criada
2. Vá na aba "Keys"
3. Clique em "Add Key" > "Create new key"
4. Escolha formato JSON
5. Salve o arquivo como `google_credentials.json` na pasta `config/`

### 4. Criar Planilha

1. Acesse [Google Sheets](https://sheets.google.com/)
2. Crie uma nova planilha chamada "Helper - Gastos"
3. Copie o ID da planilha (está na URL):
   ```
   https://docs.google.com/spreadsheets/d/SEU_ID_AQUI/edit
   ```
4. Compartilhe a planilha com o email da service account (está no JSON)
   - Permissão: Editor

### 5. Estrutura da Planilha

A primeira aba será criada automaticamente pelo sistema com o seguinte cabeçalho:
```
Data | Descrição | Categoria | Valor | Forma_Pagamento | Observações
```

---

## Configuração do WhatsApp (Evolution API)

### Opção 1: Instalação Local (Desenvolvimento)

1. Clone o repositório da Evolution API:
```bash
git clone https://github.com/EvolutionAPI/evolution-api.git
cd evolution-api
```

2. Configure o arquivo `.env`:
```env
SERVER_URL=http://localhost:8080
AUTHENTICATION_API_KEY=sua_chave_secreta_aqui
```

3. Inicie com Docker:
```bash
docker-compose up -d
```

4. Acesse `http://localhost:8080/manager` para configurar

### Opção 2: Servidor VPS (Produção)

1. Contrate uma VPS (recomendado: DigitalOcean, Vultr, Contabo)
2. Instale Docker e Docker Compose
3. Siga os passos da Opção 1, mas use o IP público da VPS
4. Configure um domínio (opcional mas recomendado)

### Criar Instância do WhatsApp

1. Acesse o painel da Evolution API
2. Crie uma nova instância chamada "helper"
3. Escaneie o QR Code com o WhatsApp
4. Anote a API Key gerada

### Configurar Webhook

1. No painel da Evolution API, vá em "Webhook"
2. Configure:
   - URL: `https://seu-dominio.com/webhook` (ou IP do HostGator)
   - Events: Marque "messages"
   - Enabled: Sim

---

## Instalação Local

### 1. Clonar/Baixar o Projeto

```bash
cd Desktop
cd helper
```

### 2. Criar Ambiente Virtual

```powershell
python -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

1. Baixe o instalador: [Tesseract Windows](https://github.com/UB-Mannheim/tesseract/wiki)
2. Instale em `C:\Program Files\Tesseract-OCR`
3. Adicione ao PATH do Windows ou configure no código

### 5. Configurar Variáveis de Ambiente

1. Copie o arquivo de exemplo:
```powershell
copy config\.env.example config\.env
```

2. Edite `config/.env` com suas configurações:
```env
# Google Sheets
GOOGLE_SHEETS_CREDENTIALS_FILE=config/google_credentials.json
SPREADSHEET_ID=seu_id_da_planilha_aqui

# WhatsApp (Evolution API)
EVOLUTION_API_URL=http://seu-servidor:8080
EVOLUTION_API_KEY=sua_chave_api_aqui
EVOLUTION_INSTANCE_NAME=helper

# Números Autorizados
AUTHORIZED_NUMBERS=5519993488882,5519983680292,5519983680308

# Flask
FLASK_SECRET_KEY=gere_uma_chave_secreta_forte_aqui
FLASK_ENV=production
FLASK_DEBUG=False

# Configurações do Auditor
ALERT_THRESHOLD_PERCENT=30
CHECK_INTERVAL_HOURS=24

# Widget Windows
WIDGET_CHECK_INTERVAL_MINUTES=30
WIDGET_POSITION_X=100
WIDGET_POSITION_Y=100
```

### 6. Testar Localmente

```powershell
cd backend
python app.py
```

O servidor estará rodando em `http://localhost:5000`

---

## Deploy no HostGator

### 1. Preparar Arquivos

1. Compacte os seguintes arquivos/pastas:
   - `backend/`
   - `config/` (com `.env` e `google_credentials.json`)
   - `requirements.txt`

### 2. Upload via cPanel

1. Acesse o cPanel do HostGator
2. Vá em "File Manager"
3. Navegue até `public_html` ou crie uma pasta `helper`
4. Faça upload do arquivo ZIP
5. Extraia os arquivos

### 3. Configurar Python App

1. No cPanel, procure por "Setup Python App"
2. Clique em "Create Application"
3. Configure:
   - Python version: 3.9 ou superior
   - Application root: `/home/seu_usuario/helper`
   - Application URL: `/helper` ou domínio customizado
   - Application startup file: `backend/app.py`
   - Application Entry point: `app`

4. Clique em "Create"

### 4. Instalar Dependências

1. No painel da Python App, clique em "Enter to the virtual environment"
2. Execute:
```bash
pip install -r requirements.txt
```

### 5. Configurar Variáveis de Ambiente

No cPanel, adicione as variáveis de ambiente na seção "Environment Variables" da Python App.

### 6. Configurar .htaccess (se necessário)

Crie um arquivo `.htaccess` em `public_html/helper`:
```apache
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ /helper/backend/app.py/$1 [QSA,L]
```

### 7. Reiniciar Aplicação

No painel Python App, clique em "Restart"

### 8. Testar

Acesse: `https://seu-dominio.com/helper/health`

Deve retornar:
```json
{
  "status": "healthy",
  "service": "Helper Backend",
  "version": "1.0.0"
}
```

---

## Configuração do Widget Windows

### 1. Criar Atalho

1. Crie um arquivo `iniciar_helper.bat`:
```batch
@echo off
cd /d "%~dp0"
call venv\Scripts\activate
pythonw widget\helper_ui.pyw
```

2. Crie um atalho deste arquivo na pasta Inicializar do Windows:
   - Pressione `Win + R`
   - Digite `shell:startup`
   - Copie o atalho para esta pasta

### 2. Configurar Tesseract no Widget

Se o Tesseract não estiver no PATH, edite `backend/ocr_engine.py`:
```python
def __init__(self, tesseract_path: Optional[str] = None):
    if tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_path
    else:
        # Caminho padrão Windows
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### 3. Testar Widget

```powershell
pythonw widget\helper_ui.pyw
```

---

## Testes

### 1. Testar Integração Google Sheets

```python
from backend.sheets_manager import SheetsManager

sheets = SheetsManager('config/google_credentials.json', 'SEU_ID_PLANILHA')
sheets.ensure_current_month_exists()
print("Conexão OK!")
```

### 2. Testar Webhook WhatsApp

Envie uma mensagem de teste:
```
Teste 10
```

Deve receber resposta do Helper confirmando o registro.

### 3. Testar OCR

Envie uma foto de recibo pelo WhatsApp.

### 4. Testar Auditoria

```powershell
curl -X POST http://localhost:5000/audit
```

---

## Solução de Problemas

### Erro: "Import gspread could not be resolved"

Instale as dependências:
```powershell
pip install -r requirements.txt
```

### Erro: "Tesseract not found"

Instale o Tesseract OCR e adicione ao PATH ou configure o caminho manualmente.

### Erro: "Unauthorized" no WhatsApp

Verifique se o número está na lista `AUTHORIZED_NUMBERS` no `.env`.

### Erro: "Connection refused" Evolution API

Verifique se a Evolution API está rodando e acessível.

### HostGator: "Application failed to start"

1. Verifique os logs em `logs/` no cPanel
2. Confirme que todas as dependências foram instaladas
3. Verifique permissões dos arquivos (755 para pastas, 644 para arquivos)

---

## Manutenção

### Backup da Planilha

Configure backup automático no Google Drive ou exporte mensalmente.

### Atualização do Sistema

1. Faça backup dos arquivos de configuração
2. Substitua os arquivos do código
3. Reinstale dependências se necessário
4. Reinicie a aplicação

### Monitoramento

- Verifique logs regularmente
- Configure alertas de erro (opcional)
- Teste o webhook periodicamente

---

## Suporte

Para dúvidas ou problemas:
1. Verifique a documentação
2. Revise os logs de erro
3. Teste cada componente isoladamente