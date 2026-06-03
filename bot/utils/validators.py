"""
Validators for input data and business logic.
"""

import re
from typing import Tuple


class Validators:
    """Validation utilities."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def validate_price(price: float) -> Tuple[bool, str]:
        """Validate product price."""
        if price < 0:
            return False, "Preço não pode ser negativo"
        if price > 999999.99:
            return False, "Preço excede o limite máximo"
        return True, ""

    @staticmethod
    def validate_product_name(name: str) -> Tuple[bool, str]:
        """Validate product name."""
        if not name or len(name) < 3:
            return False, "Nome deve ter pelo menos 3 caracteres"
        if len(name) > 100:
            return False, "Nome não pode exceder 100 caracteres"
        return True, ""

    @staticmethod
    def validate_description(description: str, max_length: int = 1024) -> Tuple[bool, str]:
        """Validate description."""
        if not description or len(description) < 5:
            return False, "Descrição deve ter pelo menos 5 caracteres"
        if len(description) > max_length:
            return False, f"Descrição não pode exceder {max_length} caracteres"
        return True, ""

    @staticmethod
    def validate_stock(quantity: int) -> Tuple[bool, str]:
        """Validate stock quantity."""
        if quantity < 0:
            return False, "Quantidade não pode ser negativa"
        if quantity > 1000000:
            return False, "Quantidade excede o limite máximo"
        return True, ""

    @staticmethod
    def validate_coupon_code(code: str) -> Tuple[bool, str]:
        """Validate coupon code format."""
        if not code or len(code) < 3:
            return False, "Código deve ter pelo menos 3 caracteres"
        if len(code) > 20:
            return False, "Código não pode exceder 20 caracteres"
        if not re.match(r'^[A-Z0-9_-]+$', code):
            return False, "Código deve conter apenas letras maiúsculas, números, - e _"
        return True, ""

    @staticmethod
    def validate_discount_percentage(discount: float) -> Tuple[bool, str]:
        """Validate discount percentage."""
        if discount < 0 or discount > 100:
            return False, "Desconto deve estar entre 0 e 100%"
        return True, ""

    @staticmethod
    def validate_category_name(name: str) -> Tuple[bool, str]:
        """Validate category name."""
        if not name or len(name) < 2:
            return False, "Nome da categoria deve ter pelo menos 2 caracteres"
        if len(name) > 50:
            return False, "Nome da categoria não pode exceder 50 caracteres"
        return True, ""
