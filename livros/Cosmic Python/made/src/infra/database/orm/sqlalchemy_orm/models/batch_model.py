from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.batch import Batch
from src.infra.database.orm.sqlalchemy_orm.base import (
    table_registry,
)


@table_registry.mapped_as_dataclass
class BatchModel:
    __tablename__ = 'batches'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    reference: Mapped[str] = mapped_column(String)
    sku: Mapped[str] = mapped_column(String)
    purchased_quantity: Mapped[int] = mapped_column(Integer)
    eta: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    def to_domain(self) -> Batch:
        return Batch(
            self.reference, self.sku, self.purchased_quantity, self.eta
        )

    @staticmethod
    def from_domain(batch: Batch):
        return BatchModel(
            batch.reference, batch.sku, batch.purchased_quantity, batch.eta
        )
