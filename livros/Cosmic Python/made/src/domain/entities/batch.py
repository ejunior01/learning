from datetime import date
from typing import Optional

from src.domain.shared.types import Quantity, Reference, Sku
from src.domain.value_object.order_line import OrderLine


class Batch:
    def __init__(
        self, ref: Reference, sku: Sku, qty: Quantity, eta: Optional[date]
    ) -> None:
        self._reference = ref
        self._sku = sku
        self._eta = eta
        self._purchased_quantity = qty
        self._allocations = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def eta(self):
        return self._eta

    @property
    def sku(self):
        return self._sku

    @property
    def purchased_quantity(self):
        return self._purchased_quantity

    @property
    def reference(self) -> Reference:
        return self._reference

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> None:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.available_quantity >= line.qty and self._sku == line.sku

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return False
        return self.eta > other.eta
