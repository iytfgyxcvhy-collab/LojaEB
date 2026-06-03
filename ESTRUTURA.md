# LojaEB - Guia de Estrutura e Arquitetura

## 📋 Visão Geral da Estrutura

O projeto LojaEB é organizado em módulos independentes para máxima escalabilidade e manutenibilidade.

## 🗂️ Estrutura de Diretórios

```
LojaEB/
├── bot/
│   ├── cogs/                  # Componentes do bot (módulos Discord)
│   │   ├── __init__.py        # Carregador de cogs
│   │   ├── subscription.py    # Sistema de assinatura e licenças
│   │   ├── shop.py            # Gerenciamento de loja e produtos
│   │   ├── tickets.py         # Sistema de suporte com tickets
│   │   └── events.py          # Listeners de eventos do bot
│   │
│   ├── database/              # Camada de dados
│   │   ├── __init__.py        # Exports do módulo
│   │   ├── connection.py      # Gerenciador de conexão MongoDB
│   │   └── models.py          # Schemas e factory methods
│   │
│   ├── models/                # Modelos de dados
│   │   └── __init__.py
│   │
│   ├── services/              # Lógica de negócio
│   │   ├── __init__.py
│   │   ├── subscription_service.py  # Serviço de assinaturas
│   │   ├── shop_service.py            # Serviço de loja
│   │   ├── ticket_service.py         # Serviço de tickets
│   │   └── payment_service.py        # Serviço de pagamentos
│   │
│   ├── utils/                  # Utilitários e helpers
│   │   ├── __init__.py
│   │   ├── logger.py           # Sistema de logs centralizado
│   │   ├── embeds.py           # Factory de embeds Discord
│   │   ├── decorators.py       # Decoradores para comandos
│   │   └── validators.py       # Validação de dados
│   │
│   ├── __init__.py
│   └── main.py                 # Ponto de entrada principal
│
├── dashboard/                 # FastAPI Dashboard (em desenvolvimento)
├── logs/                      # Diretório de logs
├── requirements.txt           # Dependências Python
├── .env.example              # Exemplo de variáveis de ambiente
├── .gitignore                # Arquivos ignorados pelo Git
├── Procfile                  # Configuração para Railway
├── railway.json              # Especificação do Railway
├── README.md                 # Documentação principal
└── ESTRUTURA.md              # Documentação de arquitetura
```

## 🏗️ Componentes Principais

### 1. **Cogs (bot/cogs/)**
Módulos independentes que adicionam funcionalidades:

- **subscription.py**: Gerencia assinaturas
- **shop.py**: Sistema de loja
- **tickets.py**: Suporte com tickets
- **events.py**: Listeners de eventos

### 2. **Database (bot/database/)**
Camada de dados com MongoDB:

- **connection.py**: Conexão assíncrona MongoDB
- **models.py**: Schemas de documentos

### 3. **Services (bot/services/)**
Lógica de negócio isolada:

- **subscription_service.py**: Assinaturas
- **shop_service.py**: Loja
- **ticket_service.py**: Tickets
- **payment_service.py**: Pagamentos

### 4. **Utils (bot/utils/)**
Utilitários reutilizáveis:

- **logger.py**: Logging centralizado
- **embeds.py**: Factory de embeds
- **decorators.py**: Decoradores
- **validators.py**: Validação

## 🔄 Fluxo de Dados

```
[Comando Discord] → [Cog] → [Service] → [Database] → [Response]
```

## 📚 Padrões de Projeto

- **Singleton**: Database, Logger
- **Factory**: EmbedFactory, Models
- **Service Layer**: Separação de lógica

## 🔐 Verificação de Licença

```
Comando → @require_license → Service.check_license() → MongoDB
→ Permitir/Bloquear
```

## 📊 Coleções MongoDB

- `guilds` - Servidores
- `licenses` - Assinaturas
- `products` - Produtos
- `categories` - Categorias
- `orders` - Pedidos
- `payments` - Pagamentos
- `tickets` - Tickets
- `coupons` - Cupons
- `users` - Usuários
- `logs` - Auditoria (TTL 30 dias)

## 🔑 Índices de Performance

Índices criados automaticamente em cada coleção para otimizar queries.

## 🚀 Como Expandir

### Novo Cog
1. Criar em `bot/cogs/novo_cog.py`
2. Herdar de `commands.Cog`
3. Implementar `async def setup(bot)`
4. Será carregado automaticamente

### Novo Service
1. Criar em `bot/services/novo_service.py`
2. Usar `self.db = db_instance.get_db()`
3. Implementar métodos async

### Nova Coleção
1. Adicionar modelo em `models.py`
2. Adicionar índice em `Database.create_indexes()`
3. Usar via `get_collection("nome")`

## 🔧 Troubleshooting

- **MONGODB_URI not set**: Configure em `.env`
- **Database not connected**: Verifique `await db_instance.connect()`
- **Cogs não carregam**: Veja `logs/bot_YYYYMMDD.log`

## 📈 Monitoramento

Logs incluem:
- Execução de comandos
- Operações de BD
- Erros e exceções
- Verificações de permissão

---

**LojaEB** - Sistema Modular e Escalável para Discord
