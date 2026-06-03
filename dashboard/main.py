"""
Dashboard FastAPI - Admin e Cliente
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import asyncio
from datetime import datetime
import jwt
from functools import wraps

from bot.database import db_instance
from bot.services.mercadopago_service import MercadoPagoService
from bot.services.shop_service import ShopService
from bot.services.subscription_service import SubscriptionService
from bot.utils.logger import get_logger

logger = get_logger("dashboard")

# Inicializar FastAPI
app = FastAPI(title="LojaEB Dashboard", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serviços
mp_service = MercadoPagoService()
shop_service = ShopService()
sub_service = SubscriptionService()


# ============ MODELOS ============

class OrderCreate(BaseModel):
    guild_id: int
    user_id: int
    items: List[Dict[str, Any]]
    total: float


class PaymentWebhook(BaseModel):
    action: str
    data: Dict[str, Any]


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: Optional[str] = None


# ============ AUTENTICAÇÃO ============

async def verify_token(token: Optional[str] = None):
    """Verificar token JWT"""
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    
    try:
        secret = os.getenv("JWT_SECRET_KEY", "seu-secret-key-aqui")
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# ============ ROTAS PÚBLICAS ============

@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Landing page principal"""
    return open("dashboard/templates/landing.html").read()


@app.post("/api/auth/login")
async def login(guild_id: int, user_id: int, token: str):
    """Login com Discord"""
    try:
        # Validar token Discord
        # (simplificado - em produção validar com Discord API)
        
        secret = os.getenv("JWT_SECRET_KEY", "seu-secret-key-aqui")
        jwt_token = jwt.encode(
            {"guild_id": guild_id, "user_id": user_id, "exp": datetime.utcnow().timestamp() + 86400},
            secret,
            algorithm="HS256"
        )
        
        return {
            "access_token": jwt_token,
            "token_type": "bearer",
            "guild_id": guild_id,
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Erro login: {str(e)}")
        raise HTTPException(status_code=400, detail="Erro no login")


@app.get("/api/products")
async def list_products(guild_id: int):
    """Listar produtos da loja"""
    try:
        await shop_service.initialize()
        products = await shop_service.get_products_by_guild(guild_id)
        return {
            "status": "success",
            "data": products
        }
    except Exception as e:
        logger.error(f"Erro ao listar produtos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar produtos")


@app.get("/api/products/{product_id}")
async def get_product(product_id: str):
    """Obter detalhes do produto"""
    try:
        await shop_service.initialize()
        product = await shop_service.get_product(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return {
            "status": "success",
            "data": product
        }
    except Exception as e:
        logger.error(f"Erro ao obter produto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao obter produto")


# ============ ROTAS DE PAGAMENTO ============

@app.post("/api/orders/create")
async def create_order(order: OrderCreate):
    """Criar novo pedido e iniciar pagamento"""
    try:
        await shop_service.initialize()
        await mp_service.initialize()

        # Criar pedido
        order_data = await shop_service.create_order(
            guild_id=order.guild_id,
            user_id=order.user_id,
            items=order.items,
            total=order.total
        )
        
        order_id = order_data["order_id"]

        # Criar pagamento
        payment = await mp_service.create_payment(
            order_id=order_id,
            guild_id=order.guild_id,
            user_id=order.user_id,
            amount=order.total
        )

        return {
            "status": "success",
            "order_id": order_id,
            "payment_url": payment["payment_url"],
            "message": "Pedido criado, redirecionando para pagamento..."
        }

    except Exception as e:
        logger.error(f"Erro ao criar pedido: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar pedido")


@app.get("/api/orders/{order_id}/status")
async def get_order_status(order_id: str):
    """Obter status do pedido"""
    try:
        await mp_service.initialize()
        payment = await mp_service.get_payment_status(order_id)
        
        if not payment:
            raise HTTPException(status_code=404, detail="Pedido não encontrado")
        
        return {
            "status": "success",
            "order_id": order_id,
            "payment_status": payment.get("status"),
            "amount": payment.get("amount"),
            "created_at": payment.get("created_at")
        }
    except Exception as e:
        logger.error(f"Erro ao obter status: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao obter status")


@app.post("/webhook/mercadopago")
async def mercadopago_webhook(request: Request):
    """Webhook do Mercado Pago"""
    try:
        data = await request.json()
        logger.info(f"Webhook Mercado Pago recebido: {data}")
        
        await mp_service.initialize()
        success = await mp_service.process_webhook(data)
        
        if success:
            return {"status": "ok"}
        return {"status": "processed"}
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {str(e)}")
        return {"status": "error", "message": str(e)}


# ============ ROTAS ADMIN ============

@app.get("/api/admin/dashboard/{guild_id}")
async def admin_dashboard(guild_id: int, token: str):
    """Dashboard administrativo"""
    try:
        payload = await verify_token(token)
        
        await db_instance.connect()
        db = db_instance.get_db()
        
        # Estatísticas
        total_orders = await db.orders.count_documents({"guild_id": guild_id})
        completed_orders = await db.orders.count_documents({"guild_id": guild_id, "status": "completed"})
        total_revenue = 0
        
        orders = await db.orders.find({"guild_id": guild_id, "status": "completed"}).to_list(None)
        for order in orders:
            total_revenue += order.get("total", 0)
        
        return {
            "status": "success",
            "data": {
                "total_orders": total_orders,
                "completed_orders": completed_orders,
                "total_revenue": total_revenue,
                "pending_orders": total_orders - completed_orders
            }
        }
    except Exception as e:
        logger.error(f"Erro no dashboard: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao carregar dashboard")


@app.get("/api/admin/orders/{guild_id}")
async def admin_orders(guild_id: int, token: str):
    """Listar pedidos do servidor"""
    try:
        payload = await verify_token(token)
        
        await shop_service.initialize()
        db = db_instance.get_db()
        
        cursor = db.orders.find({"guild_id": guild_id}).sort("created_at", -1)
        orders = await cursor.to_list(length=100)
        
        return {
            "status": "success",
            "data": orders
        }
    except Exception as e:
        logger.error(f"Erro ao listar pedidos: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao listar pedidos")


@app.post("/api/admin/products")
async def admin_create_product(product: ProductCreate, guild_id: int, token: str):
    """Criar novo produto (admin)"""
    try:
        payload = await verify_token(token)
        
        await shop_service.initialize()
        new_product = await shop_service.create_product(
            guild_id=guild_id,
            name=product.name,
            description=product.description,
            price=product.price,
            category_id=product.category_id or "general",
            stock=product.stock
        )
        
        return {
            "status": "success",
            "data": new_product
        }
    except Exception as e:
        logger.error(f"Erro ao criar produto: {str(e)}")
        raise HTTPException(status_code=500, detail="Erro ao criar produto")


# ============ PÁGINAS DE STATUS ============

@app.get("/payment/success/{order_id}", response_class=HTMLResponse)
async def payment_success(order_id: str):
    """Página de sucesso de pagamento"""
    return f"""
    <html>
    <head>
        <title>Pagamento Confirmado</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}
            .success {{ color: #28a745; font-size: 30px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="success">✅ Pagamento Confirmado!</div>
            <p>Obrigado pela sua compra.</p>
            <p>Seu pedido: <strong>{order_id[:8]}</strong></p>
            <p>Em breve seus itens estarão disponíveis.</p>
        </div>
    </body>
    </html>
    """


@app.get("/payment/pending/{order_id}", response_class=HTMLResponse)
async def payment_pending(order_id: str):
    """Página de pagamento pendente"""
    return f"""
    <html>
    <head>
        <title>Pagamento Pendente</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}
            .pending {{ color: #ffc107; font-size: 30px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="pending">⏳ Pagamento Pendente</div>
            <p>Seu pagamento está sendo processado.</p>
            <p>Pedido: <strong>{order_id[:8]}</strong></p>
            <p>Pode levar alguns minutos para confirmar.</p>
        </div>
    </body>
    </html>
    """


@app.get("/payment/failure/{order_id}", response_class=HTMLResponse)
async def payment_failure(order_id: str):
    """Página de falha de pagamento"""
    return f"""
    <html>
    <head>
        <title>Pagamento Recusado</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
            }}
            .container {{
                background: white;
                padding: 40px;
                border-radius: 10px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            }}
            .error {{ color: #dc3545; font-size: 30px; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="error">❌ Pagamento Recusado</div>
            <p>Seu pagamento não foi processado.</p>
            <p>Pedido: <strong>{order_id[:8]}</strong></p>
            <p>Tente novamente com outro método.</p>
        </div>
    </body>
    </html>
    """


# ============ INICIALIZAÇÃO ============

async def startup():
    """Inicializar dashboard"""
    try:
        await db_instance.connect()
        await mp_service.initialize()
        logger.info("✅ Dashboard iniciado com sucesso")
    except Exception as e:
        logger.error(f"❌ Erro ao iniciar dashboard: {str(e)}", exc_info=True)
        raise


app.add_event_handler("startup", startup)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("DASHBOARD_HOST", "0.0.0.0"),
        port=int(os.getenv("DASHBOARD_PORT", 8000))
    )
