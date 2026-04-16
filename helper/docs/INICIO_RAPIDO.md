# Helper - Início Rápido (5 Minutos)

## Checklist de Configuração

### ✅ Passo 1: Instalar Dependências (2 min)

```powershell
# Execute o instalador automático
instalar.bat
```

Ou manualmente:
```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### ✅ Passo 2: Google Sheets (1 min)

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie projeto "Helper"
3. Ative Google Sheets API
4. Crie Service Account
5. Baixe JSON de credenciais
6. Salve como `config/google_credentials.json`

### ✅ Passo 3: Criar Planilha (30 seg)

1. Crie planilha no Google Sheets: "Helper - Gastos"
2. Copie o ID da URL
3. Compartilhe com email da service account (do JSON)

### ✅ Passo 4: Configurar .env (1 min)

```powershell
# Copie o template
copy config\.env.example config\.env

# Edite com suas informações
notepad config\.env
```

Preencha:
```env
SPREADSHEET_ID=seu_id_aqui
EVOLUTION_API_URL=http://seu-servidor:8080
EVOLUTION_API_KEY=sua_chave_aqui
AUTHORIZED_NUMBERS=5519993488882,5519983680292,5519983680308
```

### ✅ Passo 5: Testar (30 seg)

```powershell
# Inicie o backend
iniciar_backend.bat

# Em outro terminal, inicie o widget
iniciar_widget.bat
```

Acesse: http://localhost:5000/health

Deve retornar:
```json
{"status": "healthy"}
```

## Primeiro Uso

### 1. Envie Mensagem de Teste

WhatsApp:
```
Ajuda
```

Deve receber instruções do Helper.

### 2. Registre Primeiro Gasto

WhatsApp:
```
Teste 10
```

Deve receber confirmação e ver na planilha.

### 3. Verifique Widget

O widget deve mostrar "Tudo Certo!" se não houver alertas.

## Próximos Passos

1. Configure Evolution API (veja [INSTALACAO.md](INSTALACAO.md))
2. Instale Tesseract OCR para processar imagens
3. Configure widget para iniciar com Windows
4. Leia o [Guia de Uso](GUIA_USO.md) completo

## Problemas Comuns

### "Import gspread could not be resolved"
```powershell
pip install -r requirements.txt
```

### "Spreadsheet not found"
Verifique se compartilhou a planilha com a service account.

### "Unauthorized"
Verifique se seu número está em AUTHORIZED_NUMBERS.

### Backend não inicia
Verifique se config/.env existe e está configurado.

## Comandos Úteis

```powershell
# Instalar tudo
instalar.bat

# Iniciar backend
iniciar_backend.bat

# Iniciar widget
iniciar_widget.bat

# Testar conexão
curl http://localhost:5000/health

# Ver logs (se houver erro)
type logs\error.log
```

## Estrutura Mínima

```
helper/
├── backend/
│   └── app.py
├── config/
│   ├── .env                      ← Configure aqui
│   └── google_credentials.json   ← Coloque aqui
├── widget/
│   └── helper_ui.pyw
├── requirements.txt
└── instalar.bat                  ← Execute primeiro
```

## Teste Completo

1. ✅ Backend rodando (http://localhost:5000/health)
2. ✅ Widget aberto e sem erros
3. ✅ Mensagem "Ajuda" respondida
4. ✅ Gasto registrado na planilha
5. ✅ Auditoria executada sem erros

Se todos os itens estão OK, você está pronto! 🎉

## Suporte

- Documentação completa: [INSTALACAO.md](INSTALACAO.md)
- Guia de uso: [GUIA_USO.md](GUIA_USO.md)
- README principal: [README.md](../README.md)