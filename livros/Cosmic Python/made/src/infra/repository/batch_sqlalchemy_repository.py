from sqlalchemy.orm import Session

from src.domain.entities.batch import Batch
from src.domain.repository.batch_repository import BatchRepository
from src.domain.shared.types import Reference
from src.infra.database.orm.sqlalchemy_orm.models.batch_model import BatchModel


class BatchSqlAlchemyRepository(BatchRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def add(self, batch: Batch) -> None:
        batch_model = BatchModel.from_domain(batch)
        self._session.add(batch_model)
        self._session.commit()

    def update(self, batch: Batch) -> None:
        batch_model = (
            self._session.query(BatchModel)
            .filter(reference=batch.reference)
            .first()
        )

        if batch_model:
            batch_model.eta = batch.eta
            batch_model.sku = batch.sku
            batch_model.qty = batch.available_quantity()

            self._session.commit()

    def get(self, reference: Reference) -> Batch:
        batch_model = (
            self._session.query(BatchModel)
            .filter(BatchModel.reference == reference)
            .first()
        )

        return batch_model.to_domain() if batch_model else None

    def remove(self, reference: Reference) -> None:
        batch_model = (
            self._session.query(BatchModel)
            .filter(BatchModel.reference == reference)
            .first()
        )

        if batch_model:
            self._session.delete(batch_model)
            self._session.commit()
