# LojaEB - Discord Commercial Bot 🤖

Sistema completo de e-commerce para Discord com suporte a assinaturas, loja, tickets, dashboard e pagamentos via PIX.

## 🎯 Características

### Sistema de Assinatura
- ✅ Planos: Diário, Mensal, Trimestral
- ✅ Verificação automática de licença
- ✅ Bloqueio de funcionalidades sem assinatura
- ✅ Renovação automática

### Sistema de Loja
- ✅ Produtos ilimitados
- ✅ Categorias customizáveis
- ✅ Controle de estoque
- ✅ Produtos digitais
- ✅ Produtos por cargo Discord
- ✅ Cupons e descontos

### Sistema de Tickets
- ✅ 5 Categorias de tickets
- ✅ Fechamento automático
- ✅ Logs completos
- ✅ Transcrição de tickets

### Sistema de Pagamentos
- ✅ Integração Mercado Pago
- ✅ Integração PushinPay
- ✅ QR Code PIX
- ✅ PIX Copia e Cola
- ✅ Aprovação automática

### Dashboard Web
- ✅ Painel administrativo completo
- ✅ Estatísticas em tempo real
- ✅ Monitoramento de recursos
- ✅ Logs em tempo real

## 🛠️ Tecnologias

- **Python 3.12+** - Linguagem principal
- **discord.py** - Framework Discord
- **MongoDB Atlas** - Banco de dados
- **Motor** - Driver assíncrono para MongoDB
- **FastAPI** - API do dashboard
- **Railway** - Hospedagem

## 📦 Instalação

### Pré-requisitos
- Python 3.12+
- MongoDB Atlas conta
- Bot Discord criado em Discord Developer Portal

### Setup Local

```bash
# Clone o repositório
git clone https://github.com/iytfgyxcvhy-collab/LojaEB.git
cd LojaEB

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais
```

## 🚀 Deploy na Railway

```bash
# Instale a CLI do Railway
npm install -g @railway/cli

# Faça login
railway login

# Deploy
railway up
```

## 📁 Estrutura do Projeto

```
LojaEB/
├── bot/
│   ├── cogs/
│   │   ├── subscription.py
│   │   ├── shop.py
│   │   ├── tickets.py
│   │   ├── payments.py
│   │   ├── admin.py
│   │   └── __init__.py
│   ├── database/
│   │   ├── connection.py
│   │   ├── models.py
│   │   └── __init__.py
│   ├── models/
│   │   ├── guild.py
│   │   ├── license.py
│   │   ├── product.py
│   │   ├── order.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── subscription_service.py
│   │   ├── shop_service.py
│   │   ├── payment_service.py
│   │   ├── ticket_service.py
│   │   └── __init__.py
│   ├── utils/
│   │   ├── logger.py
│   │   ├── embeds.py
│   │   ├── validators.py
│   │   ├── decorators.py
│   │   └── __init__.py
│   └── main.py
├── dashboard/
│   ├── app/
│   ├── routes/
│   ├── main.py
│   └── requirements.txt
├── requirements.txt
├── railway.json
├── Procfile
├── .env.example
└── README.md
```

## 🔐 Segurança

- Variáveis de ambiente para credenciais
- Proteção contra comandos sem licença
- Tratamento global de erros
- Logs de auditoria completos
- Sistema de permissões robusto

## 📊 Banco de Dados

MongoDB Atlas com as seguintes coleções:
- `guilds` - Dados dos servidores
- `licenses` - Assinaturas ativas
- `products` - Catálogo de produtos
- `categories` - Categorias de produtos
- `stock` - Controle de estoque
- `orders` - Pedidos realizados
- `users` - Dados dos usuários
- `payments` - Histórico de pagamentos
- `coupons` - Cupons e promoções
- `tickets` - Sistema de tickets
- `logs` - Auditoria completa

## 📝 Comandos Disponíveis

### Assinatura
- `/assinar` - Ver planos de assinatura
- `/status` - Status da licença do servidor

### Loja
- `/catalogo` - Ver catálogo de produtos
- `/produtos` - Gerenciar produtos
- `/categorias` - Gerenciar categorias
- `/estoque` - Visualizar estoque
- `/gerenciarestoque` - Controlar estoque
- `/pedidos` - Ver pedidos

### Tickets
- `/ticket` - Criar novo ticket
- `/fecharticket` - Fechar ticket

### Administração
- `/backup` - Realizar backup
- `/logs` - Visualizar logs
- `/configurar` - Configurações do servidor

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📧 Suporte

Para suporte, entre em contato através:
- Discord: Crie um ticket no servidor
- Email: support@lojaeb.com

## 🙏 Agradecimentos

- discord.py community
- MongoDB
- Railway
- Mercado Pago

---

**LojaEB** © 2024 - Desenvolvido com ❤️ para Discord
