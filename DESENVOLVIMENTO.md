# 🛠️ Guia de Desenvolvimento - LojaEB

## 📚 Documentação de Desenvolvimento

Este guia ajuda desenvolvedores a entender e expandir o LojaEB.

## 🎯 Fluxo de Desenvolvimento

### 1. Entender a Arquitetura

- Leia `ESTRUTURA.md` para entender a organização
- Familiarize-se com padrões: Singleton, Factory, Service Layer
- Veja exemplos em `bot/services/subscription_service.py`

### 2. Setup de Desenvolvimento

```bash
# Clone e setup
git clone https://github.com/iytfgyxcvhy-collab/LojaEB.git
cd LojaEB
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure .env
cp .env.example .env
# Edite com suas credenciais

# Execute
python bot/main.py
```

### 3. Fazer Mudanças

Crie uma branch para sua feature:

```bash
git checkout -b feature/minha-feature
```

## 🏗️ Adicionando Nova Funcionalidade

### Exemplo: Adicionar Comando de Estatísticas

#### 1. Criar Service

`bot/services/stats_service.py`:
```python
class StatsService:
    def __init__(self):
        self.db = None
    
    async def initialize(self):
        self.db = db_instance.get_db()
    
    async def get_guild_stats(self, guild_id: int):
        # Implementar lógica
        pass
```

#### 2. Criar Cog

`bot/cogs/stats.py`:
```python
class StatsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.stats_service = StatsService()
    
    async def cog_load(self):
        await self.stats_service.initialize()
    
    @app_commands.command(name="stats")
    @require_license
    async def stats(self, interaction: discord.Interaction):
        # Usar service
        stats = await self.stats_service.get_guild_stats(interaction.guild_id)
        # Retornar resultado

async def setup(bot):
    await bot.add_cog(StatsCog(bot))
```

#### 3. Registrar Dependências

Adicione em `bot/services/__init__.py`:
```python
from bot.services.stats_service import StatsService

__all__ = [
    # ...
    "StatsService"
]
```

## 📝 Convenções de Código

### Nomes
- Classes: `PascalCase` (ex: `StatsService`)
- Funções: `snake_case` (ex: `get_guild_stats`)
- Constantes: `UPPER_CASE` (ex: `MAX_PRODUCTS`)
- Variáveis: `snake_case` (ex: `product_id`)

### Docstrings

```python
def minha_funcao(param1: str, param2: int) -> bool:
    """Descrição breve da função.
    
    Descrição mais longa se necessário.
    
    Args:
        param1: Descrição do param1
        param2: Descrição do param2
    
    Returns:
        Descrição do retorno
    
    Raises:
        ValueError: Quando algo está errado
    """
    pass
```

### Type Hints

Sempre use type hints:

```python
# ✅ Bom
async def get_products(guild_id: int) -> List[Dict[str, Any]]:
    pass

# ❌ Ruim
async def get_products(guild_id):
    pass
```

## 🧪 Testes

Estrutura de testes (quando implementado):

```
tests/
├── __init__.py
├── test_services/
│   ├── test_subscription_service.py
│   ├── test_shop_service.py
│   └── test_payment_service.py
└── test_utils/
    ├── test_validators.py
    └── test_embeds.py
```

Executar testes:
```bash
pytest tests/ -v
```

## 🔍 Checklist para Pull Request

Antes de fazer um PR:

- [ ] Código segue convenções de nomes
- [ ] Tem docstrings em funções públicas
- [ ] Type hints em todas as funções
- [ ] Tratamento de erros adequado
- [ ] Logs adicionados quando apropriado
- [ ] Testado localmente
- [ ] Sem prints (usar logger)
- [ ] Sem credenciais no código
- [ ] Branch atualizada com main

## 📊 Estrutura de Branches

```
main (estável)
├── develop (desenvolvimento)
│   ├── feature/nova-funcionalidade
│   ├── bugfix/corrigir-bug
│   └── hotfix/corrigir-urgente
```

Nomenclatura:
- `feature/descricao-curta` - Nova funcionalidade
- `bugfix/descricao-curta` - Correção de bug
- `hotfix/descricao-curta` - Correção urgente

## 🔐 Segurança

### Verificação de Licença

Sempre proteja comandos que precisam de licença:

```python
@app_commands.command(name="comando")
@require_license
async def comando(self, interaction: discord.Interaction):
    pass
```

### Validação de Input

Use `Validators` para validar dados:

```python
from bot.utils import Validators

is_valid, error = Validators.validate_price(price)
if not is_valid:
    # Retornar erro
    pass
```

### Erros e Exceções

Sempre trate erros:

```python
try:
    # Seu código
    pass
except ValueError as e:
    logger.error(f"Erro: {str(e)}", exc_info=True)
    raise
```

## 🚀 Performance

### Queries MongoDB

- Use índices criados em `Database.create_indexes()`
- Limite resultados quando possível
- Use projeção para retornar apenas campos necessários

```python
# ❌ Ruim - retorna documento completo
product = await db.products.find_one({"product_id": id})

# ✅ Bom - retorna apenas campos necessários
product = await db.products.find_one(
    {"product_id": id},
    {"name": 1, "price": 1, "stock": 1}
)
```

### Async/Await

Sempre use async para I/O:

```python
# ✅ Bom - não bloqueia
await asyncio.sleep(1)
await db.collection.find_one({})

# ❌ Ruim - bloqueia todo o bot
time.sleep(1)
```

## 📖 Documentação

### Adicionar Documentação

1. Atualize `README.md` para mudanças em features
2. Atualize `ESTRUTURA.md` para mudanças arquiteturais
3. Adicione docstrings em novo código
4. Atualize este documento se necessário

## 🐛 Debug

### Ver Logs em Tempo Real

```bash
tail -f logs/bot_*.log
```

### Modo Debug

Alternei `LOG_LEVEL` em `.env`:

```bash
LOG_LEVEL=DEBUG
```

### Conectar ao MongoDB

Use MongoDB Compass:
1. Acesse https://www.mongodb.com/products/compass
2. Conecte com sua `MONGODB_URI`
3. Explore dados em tempo real

## 📞 Suporte para Desenvolvedores

- Perguntas? Abra uma issue no GitHub
- Melhorias? Faça um PR
- Bugs? Reporte com passos para reproduzir

---

**LojaEB** - Desenvolvido com ❤️ e Python
