# 📦 Guia de Instalação - LojaEB

## 🔧 Pré-requisitos

- Python 3.12+
- pip (gerenciador de pacotes)
- MongoDB Atlas (conta gratuita)
- Bot Discord criado em Discord Developer Portal
- Git

## 🚀 Instalação Local

### 1. Clone o Repositório

```bash
git clone https://github.com/iytfgyxcvhy-collab/LojaEB.git
cd LojaEB
```

### 2. Crie um Ambiente Virtual

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o Arquivo .env

```bash
cp .env.example .env
```

Edite o `.env` com seus valores:

```bash
# Discord
DISCORD_TOKEN=seu_token_aqui
APPLICATION_ID=seu_app_id

# MongoDB
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=LojaEB

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Timezone
TIMEZONE=America/Sao_Paulo
```

### 5. Configure MongoDB Atlas

1. Acesse https://www.mongodb.com/cloud/atlas
2. Crie uma conta ou faça login
3. Crie um novo cluster (gratuito)
4. Adicione um usuário de banco de dados
5. Copie a string de conexão
6. Substitua em `MONGODB_URI` no `.env`

### 6. Configure Discord Bot

1. Acesse https://discord.com/developers/applications
2. Crie uma nova aplicação
3. Vá em "Bot" e clique "Add Bot"
4. Copie o token e adicione em `DISCORD_TOKEN`
5. Ative as intents necessárias:
   - Message Content Intent
   - Server Members Intent
   - Presence Intent

6. Convide o bot para seu servidor:
   - Vá em OAuth2 → URL Generator
   - Selecione scopes: `bot`
   - Selecione permissions: `administrator`
   - Copie o link gerado e acesse no navegador

### 7. Execute o Bot

```bash
python bot/main.py
```

Você deve ver:
```
✅ Connected to MongoDB: LojaEB
✅ LojaEB | Gerenciador de Loja Discord
✅ Bot is ready! Logged in as LojaEB#0000
```

## 🌐 Deploy na Railway

### 1. Prepare o Repositório

Certifique-se de que tem `requirements.txt`, `Procfile` e `railway.json`:

**requirements.txt:**
```
discord.py==2.3.2
motor==3.3.2
pymongo==4.6.0
python-dotenv==1.0.0
aiohttp==3.9.1
fastapi==0.109.0
uvicorn==0.27.0
pydantic==2.5.3
pytz==2024.1
Pillow==10.1.0
qrcode==7.4.2
```

**Procfile:**
```
web: python bot/main.py
```

### 2. Push para GitHub

```bash
git add .
git commit -m "Deploy to Railway"
git push origin main
```

### 3. Configure na Railway

1. Acesse https://railway.app
2. Faça login com GitHub
3. Clique "New Project"
4. Selecione "Deploy from GitHub repo"
5. Selecione o repositório LojaEB

### 4. Configure Variáveis de Ambiente

Na Railway:
1. Vá em "Variables"
2. Adicione as mesmas variáveis do `.env`
3. Salve

### 5. Deploy

```bash
npm install -g @railway/cli
railway login
railway link  # Link to your Railway project
railway up
```

Ou clique "Deploy" na interface da Railway.

## ✅ Verificação

Ano seu servidor Discord, execute:

```
/assinar
```

Você deve ver um embed com os planos de assinatura.

## 🐛 Troubleshooting

### Erro: Token inválido
- Verifique se copiou o token completo
- Regenere o token se necessário
- Certifique-se que não tem espaços

### Erro: MONGODB_URI not set
- Configure em `.env` corretamente
- Use a string completa do MongoDB Atlas
- Verifique caracteres especiais (use URL encoding)

### Bot não responde a comandos
- Certifique-se que o bot tem permissão de "administrator"
- Verifique se o bot está online
- Veja os logs: `cat logs/bot_*.log`

### Erro de conexão MongoDB
- Verifique IP whitelist no MongoDB Atlas
- Certifique-se que o database existe
- Teste a conexão com MongoDB Compass

## 📝 Variáveis de Ambiente Completas

```bash
# Bot Discord
DISCORD_TOKEN=your_bot_token
APPLICATION_ID=your_app_id
COMMAND_PREFIX=!

# MongoDB
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority
DATABASE_NAME=LojaEB

# Pagamentos (preparado para futuro)
MERCADO_PAGO_ACCESS_TOKEN=your_token
MERCADO_PAGO_PUBLIC_KEY=your_key
PUSHINPAY_API_KEY=your_key

# Dashboard
DASHBOARD_SECRET_KEY=your_secret_key
DASHBOARD_ADMIN_TOKEN=your_admin_token

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log

# Timezone
TIMEZONE=America/Sao_Paulo

# Ambiente
RAILWAY_ENVIRONMENT=production
```

## 🔄 Atualizações

Para atualizar o bot:

```bash
git pull origin main
pip install -r requirements.txt --upgrade
python bot/main.py
```

## 📞 Suporte

Se encontrar problemas:

1. Verifique os logs: `logs/bot_YYYYMMDD.log`
2. Leia a documentação: `README.md` e `ESTRUTURA.md`
3. Crie uma issue no GitHub
4. Entre em contato via Discord

---

**LojaEB** © 2024 - Pronto para usar!
