from typing import List

from src.domain.entities.batch import Batch
from src.domain.errors.out_of_stock_error import OutOfStockError
from src.domain.value_object.order_line import OrderLine


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStockError(f'Out of stock for sku {line.sku}')
