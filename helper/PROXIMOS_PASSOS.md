# Helper - Próximos Passos para Catarina

## ✅ O que foi entregue

O Bob criou um sistema completo de gerenciamento de despesas com:

### Código Fonte
- ✅ Backend Flask com webhook WhatsApp
- ✅ Integração Google Sheets
- ✅ Processamento OCR de imagens
- ✅ Auditoria mensal inteligente
- ✅ Widget Windows com notificações
- ✅ Mensagens com personalidade esdrúxula

### Documentação
- ✅ README principal
- ✅ Guia de instalação completo
- ✅ Guia de uso detalhado
- ✅ Início rápido (5 minutos)
- ✅ Resumo técnico

### Scripts Auxiliares
- ✅ `instalar.bat` - Instalação automática
- ✅ `iniciar_backend.bat` - Inicia servidor
- ✅ `iniciar_widget.bat` - Inicia interface
- ✅ `.gitignore` - Proteção de dados sensíveis

## 📋 Checklist de Configuração

### 1. Google Sheets (15 minutos)

**O que fazer:**
1. Acesse https://console.cloud.google.com/
2. Crie projeto "Helper"
3. Ative Google Sheets API e Google Drive API
4. Crie Service Account
5. Baixe credenciais JSON
6. Salve como `config/google_credentials.json`

**Depois:**
1. Crie planilha "Helper - Gastos" no Google Sheets
2. Copie o ID da URL
3. Compartilhe com email da service account (está no JSON)

**Documentação**: `docs/INSTALACAO.md` seção "Configuração do Google Sheets"

### 2. Evolution API (30 minutos)

**Opção A - Local (para testes):**
```bash
git clone https://github.com/EvolutionAPI/evolution-api.git
cd evolution-api
docker-compose up -d
```

**Opção B - VPS (produção):**
- Contrate VPS (DigitalOcean, Vultr, Contabo)
- Instale Docker
- Configure Evolution API
- Aponte domínio (opcional)

**Depois:**
1. Acesse painel da Evolution API
2. Crie instância "helper"
3. Escaneie QR Code com WhatsApp
4. Configure webhook para seu servidor

**Documentação**: `docs/INSTALACAO.md` seção "Configuração do WhatsApp"

### 3. Configurar Ambiente Local (5 minutos)

```powershell
# 1. Execute o instalador
instalar.bat

# 2. Configure .env
copy config\.env.example config\.env
notepad config\.env

# 3. Preencha com suas informações:
# - SPREADSHEET_ID (da planilha)
# - EVOLUTION_API_URL (do servidor)
# - EVOLUTION_API_KEY (da Evolution API)
# - AUTHORIZED_NUMBERS (seus 3 números)
```

### 4. Instalar Tesseract OCR (5 minutos)

1. Baixe: https://github.com/UB-Mannheim/tesseract/wiki
2. Instale em `C:\Program Files\Tesseract-OCR`
3. Adicione ao PATH ou configure no código

**Necessário para**: Processar fotos de recibos

### 5. Testar Localmente (5 minutos)

```powershell
# Terminal 1 - Backend
iniciar_backend.bat

# Terminal 2 - Widget
iniciar_widget.bat

# Teste
# 1. Acesse http://localhost:5000/health
# 2. Envie "Ajuda" no WhatsApp
# 3. Registre gasto: "Teste 10"
```

### 6. Deploy no HostGator (20 minutos)

1. Compacte: `backend/`, `config/`, `requirements.txt`
2. Upload via cPanel File Manager
3. Configure Python App no cPanel
4. Instale dependências
5. Configure variáveis de ambiente
6. Teste: `https://seu-dominio.com/helper/health`

**Documentação**: `docs/INSTALACAO.md` seção "Deploy no HostGator"

## 🎯 Ordem Recomendada

### Fase 1: Setup Básico (1 hora)
1. ✅ Google Sheets configurado
2. ✅ Planilha criada e compartilhada
3. ✅ Ambiente local instalado
4. ✅ `.env` configurado

### Fase 2: Testes Locais (30 min)
1. ✅ Backend rodando
2. ✅ Widget funcionando
3. ✅ Primeiro gasto registrado
4. ✅ Planilha atualizada

### Fase 3: WhatsApp (1 hora)
1. ✅ Evolution API instalada
2. ✅ WhatsApp conectado
3. ✅ Webhook configurado
4. ✅ Mensagens funcionando

### Fase 4: Produção (30 min)
1. ✅ Deploy no HostGator
2. ✅ Testes em produção
3. ✅ Widget configurado para iniciar com Windows

## 🚨 Problemas Comuns

### "Import gspread could not be resolved"
**Solução**: Execute `pip install -r requirements.txt`

### "Spreadsheet not found"
**Solução**: Compartilhe planilha com email da service account

### "Unauthorized" no WhatsApp
**Solução**: Verifique números em `AUTHORIZED_NUMBERS` no `.env`

### Backend não inicia
**Solução**: Verifique se `config/.env` existe e está preenchido

### OCR não funciona
**Solução**: Instale Tesseract OCR e configure o PATH

## 📚 Documentação Disponível

1. **README.md** - Visão geral do projeto
2. **docs/INICIO_RAPIDO.md** - Setup em 5 minutos
3. **docs/INSTALACAO.md** - Guia completo de instalação
4. **docs/GUIA_USO.md** - Como usar no dia a dia
5. **docs/RESUMO_TECNICO.md** - Detalhes técnicos

## 💡 Dicas

### Para Começar Rápido
1. Foque primeiro no Google Sheets (mais importante)
2. Teste localmente antes de fazer deploy
3. Use Evolution API local para testes iniciais
4. Deploy no HostGator pode esperar

### Para Usar Bem
1. Registre gastos imediatamente
2. Use fotos para recibos longos
3. Revise a planilha semanalmente
4. Deixe o widget sempre aberto

### Para Manter
1. Backup mensal da planilha
2. Verifique logs se algo der errado
3. Atualize dependências ocasionalmente

## 🎉 Quando Estiver Pronto

Você saberá que está tudo funcionando quando:

1. ✅ Enviar "Ajuda" no WhatsApp e receber resposta
2. ✅ Registrar "Teste 10" e ver na planilha
3. ✅ Widget mostrar alertas
4. ✅ Auditoria executar sem erros
5. ✅ Receber notificações Windows

## 🆘 Se Precisar de Ajuda

1. **Primeiro**: Consulte a documentação em `docs/`
2. **Segundo**: Verifique os logs de erro
3. **Terceiro**: Teste cada componente isoladamente
4. **Último**: Revise o código (está todo comentado)

## 📞 Contatos Úteis

- **Google Cloud Console**: https://console.cloud.google.com/
- **Evolution API**: https://github.com/EvolutionAPI/evolution-api
- **Tesseract OCR**: https://github.com/UB-Mannheim/tesseract/wiki
- **HostGator cPanel**: Seu domínio/cpanel

## 🎊 Mensagem Final

O Helper está pronto para te ajudar a controlar seus gastos de forma divertida e eficiente!

Lembre-se:
- O sistema foi feito APENAS para despesas (sem receitas)
- A personalidade esdrúxula é proposital (para motivar)
- Todos os dados ficam no seu Google Sheets (privacidade)
- Apenas 3 números autorizados (segurança)

**Boa sorte e bom controle financeiro!** 💰📊

---

*Desenvolvido com dedicação por Bob*
*Abril 2026*