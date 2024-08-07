from operator import and_

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.batch import Batch
from src.domain.value_object.order_line import OrderLine
from src.infra.database.orm.sqlalchemy_orm.models.allocations_model import (
    AllocationModel,
)
from src.infra.database.orm.sqlalchemy_orm.models.batch_model import BatchModel
from src.infra.database.orm.sqlalchemy_orm.models.orderLine_model import (
    OrderLineModel,
)
from src.infra.repository.batch_sqlalchemy_repository import (
    BatchSqlAlchemyRepository,
)
from src.infra.repository.order_line_sqlalchemy_repository import (
    OrderLineSqlAlchemyRepository,
)
from src.shared.utils import today


def test_repository_can_save_a_batch(session):
    batch = Batch('batch1', 'RUSTY-SOAPDISH', 100, eta=today())

    repo_batch = BatchSqlAlchemyRepository(session)
    repo_batch.add(batch)
    session.commit()

    batch_model = session.scalar(
        select(BatchModel).where(BatchModel.reference == batch.reference)
    )

    assert batch_model.reference == 'batch1'


def insert_order_line(session) -> str:
    orderline = OrderLine('order1', 'GENERIC-SOFA', 12)

    repo_order_line = OrderLineSqlAlchemyRepository(session)
    repo_order_line.add(orderline)
    session.commit()

    orderline_model = session.scalar(
        select(OrderLineModel).where(
            and_(
                OrderLineModel.orderid == orderline.orderid,
                OrderLineModel.sku == orderline.sku,
            )
        )
    )

    return orderline_model.id if orderline_model else None


def insert_batch(session: Session, batch_ref) -> str:
    batch = Batch(batch_ref, 'GENERIC-SOFA', 100, eta=None)

    repo_batch = BatchSqlAlchemyRepository(session)
    repo_batch.add(batch)
    session.commit()

    batch_model = session.scalar(
        select(BatchModel).where(BatchModel.reference == batch.reference)
    )

    return batch_model.id if batch_model else None


def insert_allocation(session, orderline_id, batch1_id) -> None:
    andllocation = AllocationModel(batch1_id, orderline_id)
    session.add(andllocation)
    session.commit()


def test_repository_can_retrieve_a_batch_with_allocations(session):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, 'batch1')
    insert_batch(session, 'batch2')

    insert_allocation(session, orderline_id, batch1_id)

    repo_batch = BatchSqlAlchemyRepository(session)

    retrieved = repo_batch.get('batch1')

    allocation_model = session.scalar(
        select(AllocationModel).where(AllocationModel.batch_id == batch1_id)
    )

    expected = Batch('batch1', 'GENERIC-SOFA', 100, eta=None)

    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved.purchased_quantity == expected.purchased_quantity

    assert allocation_model.orderline_id == orderline_id
