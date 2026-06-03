"""
Pagamento com Mercado Pago - Integração completa
"""

import os
import uuid
from typing import Optional, Dict, Any
import mercadopago
from datetime import datetime, timedelta
from bot.database import db_instance, PaymentModel
from bot.utils.logger import get_logger

logger = get_logger("mercadopago_service")


class MercadoPagoService:
    """Serviço de pagamento com Mercado Pago"""

    def __init__(self):
        self.db = None
        self.mp_client = None
        self.initialize_client()

    def initialize_client(self):
        """Inicializar cliente do Mercado Pago"""
        access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
        if not access_token:
            logger.warning("MERCADOPAGO_ACCESS_TOKEN não configurado")
            return
        
        self.mp_client = mercadopago.SDK(access_token)
        logger.info("✅ Mercado Pago client inicializado")

    async def initialize(self):
        """Inicializar banco de dados"""
        self.db = db_instance.get_db()

    async def create_payment(self, order_id: str, guild_id: int, user_id: int, amount: float) -> Dict[str, Any]:
        """Criar pagamento no Mercado Pago"""
        if not self.mp_client:
            raise ValueError("Mercado Pago não configurado")
        
        try:
            if not self.db:
                await self.initialize()

            # Buscar pedido
            order = await self.db.orders.find_one({"order_id": order_id})
            if not order:
                raise ValueError(f"Pedido {order_id} não encontrado")

            # Criar preferência de pagamento
            preference_data = {
                "items": [
                    {
                        "title": f"Pedido #{order_id[:8]}",
                        "description": f"Compra de {len(order.get('items', []))} produto(s)",
                        "quantity": 1,
                        "currency_id": "BRL",
                        "unit_price": amount
                    }
                ],
                "payer": {
                    "email": f"user{user_id}@discord.local"
                },
                "external_reference": order_id,
                "notification_url": os.getenv("WEBHOOK_URL") + "/webhook/mercadopago",
                "back_urls": {
                    "success": os.getenv("DASHBOARD_URL") + f"/payment/success/{order_id}",
                    "pending": os.getenv("DASHBOARD_URL") + f"/payment/pending/{order_id}",
                    "failure": os.getenv("DASHBOARD_URL") + f"/payment/failure/{order_id}"
                },
                "auto_return": "approved"
            }

            # Criar preferência
            response = self.mp_client.preference().create(preference_data)
            
            if response["status"] != 201:
                raise Exception(f"Erro ao criar preferência: {response}")

            preference = response["response"]
            
            # Salvar preferência no BD
            payment_data = {
                "guild_id": guild_id,
                "order_id": order_id,
                "user_id": user_id,
                "amount": amount,
                "payment_method": "mercadopago",
                "status": "pending",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "mercadopago_preference_id": preference["id"],
                "mercadopago_init_point": preference["init_point"],
                "transaction_id": None
            }

            await self.db.payments.insert_one(payment_data)
            logger.info(f"✅ Pagamento criado: {order_id}")

            return {
                "order_id": order_id,
                "payment_url": preference["init_point"],
                "preference_id": preference["id"],
                "amount": amount,
                "status": "pending"
            }

        except Exception as e:
            logger.error(f"❌ Erro ao criar pagamento: {str(e)}", exc_info=True)
            raise

    async def process_webhook(self, data: Dict[str, Any]) -> bool:
        """Processar webhook do Mercado Pago"""
        try:
            if not self.db:
                await self.initialize()

            payment_id = data.get("data", {}).get("id")
            if not payment_id:
                return False

            # Buscar pagamento no Mercado Pago
            response = self.mp_client.payment().get(payment_id)
            if response["status"] != 200:
                logger.error(f"Erro ao buscar pagamento {payment_id}")
                return False

            payment = response["response"]
            external_reference = payment.get("external_reference")
            status = payment.get("status")
            transaction_id = payment.get("id")

            # Mapear status
            status_map = {
                "approved": "completed",
                "pending": "pending",
                "rejected": "failed",
                "cancelled": "cancelled"
            }

            mapped_status = status_map.get(status, "unknown")

            # Atualizar pagamento no BD
            result = await self.db.payments.update_one(
                {"order_id": external_reference},
                {
                    "$set": {
                        "status": mapped_status,
                        "transaction_id": transaction_id,
                        "updated_at": datetime.utcnow(),
                        "mercadopago_status": status
                    }
                }
            )

            if result.modified_count > 0:
                # Se aprovado, atualizar pedido
                if mapped_status == "completed":
                    await self.db.orders.update_one(
                        {"order_id": external_reference},
                        {
                            "$set": {
                                "status": "completed",
                                "payment_id": transaction_id,
                                "updated_at": datetime.utcnow()
                            }
                        }
                    )
                    logger.info(f"✅ Pagamento aprovado: {external_reference}")
                    return True
            
            return False

        except Exception as e:
            logger.error(f"❌ Erro ao processar webhook: {str(e)}", exc_info=True)
            return False

    async def get_payment_status(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Obter status do pagamento"""
        try:
            if not self.db:
                await self.initialize()

            payment = await self.db.payments.find_one({"order_id": order_id})
            return payment

        except Exception as e:
            logger.error(f"❌ Erro ao obter status: {str(e)}", exc_info=True)
            return None

    async def cancel_payment(self, order_id: str) -> bool:
        """Cancelar pagamento"""
        try:
            if not self.db:
                await self.initialize()

            payment = await self.db.payments.find_one({"order_id": order_id})
            if not payment:
                return False

            preference_id = payment.get("mercadopago_preference_id")
            if not preference_id:
                return False

            # Cancelar preferência
            response = self.mp_client.preference().update({
                "id": preference_id,
                "auto_return": "all"
            })

            # Atualizar status
            await self.db.payments.update_one(
                {"order_id": order_id},
                {
                    "$set": {
                        "status": "cancelled",
                        "updated_at": datetime.utcnow()
                    }
                }
            )

            logger.info(f"✅ Pagamento cancelado: {order_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Erro ao cancelar pagamento: {str(e)}", exc_info=True)
            return False
