from sqlalchemy.orm import Mapped, mapped_column

from src.domain.value_object.order_line import OrderLine
from src.infra.database.orm.sqlalchemy_orm.base import table_registry


@table_registry.mapped_as_dataclass
class OrderLineModel:
    __tablename__ = 'order_lines'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    orderid: Mapped[str]
    sku: Mapped[str]
    qty: Mapped[int]

    def to_domain(self) -> OrderLine:
        return OrderLine(self.orderid, self.sku, self.qty)

    @staticmethod
    def from_domain(order_line: OrderLine):
        return OrderLineModel(
            order_line.orderid, order_line.sku, order_line.qty
        )
