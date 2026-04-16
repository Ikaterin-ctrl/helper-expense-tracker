Helper - Agente de Curadoria de Despesas Pessoais
O Helper é um sistema de gerenciamento de gastos pessoais desenvolvido para automatizar a extração, organização e auditoria de despesas. O projeto integra o WhatsApp como interface de entrada, o Google Sheets como base de dados e um widget nativo do Windows para notificações e auditoria em tempo real.

Visão Geral
O sistema foi projetado para atuar como um assistente de curadoria financeira com uma personalidade inspirada nos assistentes de escritório dos anos 2000. Sua identidade visual utiliza a estética de colagem mix-media (estilo Adventure Time), representada por uma lupa vintage com pernas mecânicas.

Funcionalidades Principais
Registro via WhatsApp: Processamento de mensagens de texto simples ou em lote para inserção de despesas.

Processamento de Imagens (OCR): Extração automática de dados (valor, data e item) a partir de fotos de recibos e notas fiscais.

Auditoria Inteligente: Comparação entre o mês atual e o anterior para identificar inconsistências.

Detecção de Anomalias: Alerta automático caso um gasto em determinada categoria suba mais de 30% em relação ao período anterior.

Monitoramento de Gastos Fixos: Verificação de despesas recorrentes (Aluguel, Luz, Internet) para identificar esquecimentos de lançamento.

Widget Windows: Interface local para exibição de alertas de vencimento, erros de preenchimento e relatórios de auditoria.

Arquitetura do Sistema
A solução é composta por três camadas principais integradas:

Backend (HostGator): Aplicação Flask que gerencia os Webhooks da Evolution API (WhatsApp), processa a lógica de negócio e comunica-se com a API do Google Sheets.

Base de Dados (Google Sheets): Armazenamento organizado em abas mensais (ex: Abril_2026), garantindo histórico e fácil acesso aos dados.

Frontend Local (Widget): Aplicativo Python (.pyw) executado em segundo plano no Windows para notificações push e interação rápida.

Stack Técnica
Linguagem: Python 3.9+

Framework Web: Flask

Interface Gráfica: CustomTkinter

Integrações: Google Sheets API, Evolution API (WhatsApp)

Processamento de Imagem: Tesseract OCR / Google Vision

Notificações: Plyer

Estrutura do Projeto
Plaintext
helper/
├── backend/                # Lógica do servidor e webhooks
│   ├── app.py              # Ponto de entrada da aplicação
│   ├── sheets_manager.py   # Manipulação da API do Google Sheets
│   ├── ocr_engine.py       # Motor de processamento de imagens
│   ├── auditor.py          # Lógica de auditoria e comparação
│   └── messages.py         # Biblioteca de mensagens e persona
├── widget/                 # Interface desktop Windows
│   ├── assets/             # Ícones e expressões dinâmicas do Helper
│   └── helper_ui.pyw       # Widget de notificações local
├── config/                 # Arquivos de configuração e chaves
│   ├── .env                # Variáveis de ambiente
│   └── google_json.json    # Credenciais da Service Account Google
└── requirements.txt        # Dependências do sistema
Regras de Negócio e Segurança
Fluxo de Dados
O Helper opera exclusivamente sob a premissa de rastreio de gastos. O sistema não possui funcionalidades para registro de entradas, receitas ou gerenciamento de saldo positivo. O foco é estritamente o controle de saídas financeiras.

Whitelisting e Privacidade
O sistema possui um filtro de segurança por número de origem. Apenas mensagens provenientes dos números autorizados são processadas:


Auditoria e Alertas
Variação de Custo: Alerta de alta severidade para aumentos superiores a 30%.

Vencimentos: Notificações persistentes no Windows para contas que vencem no dia ou dia anterior.

Dados Incompletos: Identificação de linhas na planilha que não possuem valor ou descrição.

Instalação e Deploy
O projeto foi otimizado para deploy em ambientes de hospedagem compartilhada (HostGator) via cPanel Python App.

Google Cloud: Ativar a API do Google Sheets e Drive, criar uma Service Account e baixar as credenciais JSON.

Planilha: Criar uma planilha no Google Sheets e compartilhá-la com o e-mail da Service Account.

Backend: Configurar o Python App no cPanel, instalar as dependências via pip e configurar as variáveis de ambiente no arquivo .env.

WhatsApp: Configurar o Webhook na Evolution API para apontar para a URL do backend.

Widget: Instalar o Python localmente, configurar o caminho do Tesseract OCR e adicionar o script helper_ui.pyw à inicialização do Windows.

Persona do Agente
O Helper utiliza um tom de voz caricato, simulando um assistente de escritório altamente energético e ácido. A comunicação é inclusiva e didática, evitando jargões técnicos e priorizando a clareza sobre o estado das finanças pessoais de forma direta e, por vezes, sarcástica.

Desenvolvido por Catarina.
