from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.database.orm.sqlalchemy_orm.base import table_registry


@table_registry.mapped_as_dataclass
class AllocationModel:
    __tablename__ = 'allocations'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    batch_id: Mapped[int] = mapped_column(Integer, ForeignKey('batches.id'))

    orderline_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('order_lines.id')
    )
