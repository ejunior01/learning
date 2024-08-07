from dataclasses import dataclass

from src.domain.shared.types import OrderReference, ProductReference, Quantity


@dataclass(frozen=True)
class OrderLine:
    orderid: OrderReference
    sku: ProductReference
    qty: Quantity
