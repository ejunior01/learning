from operator import and_

from sqlalchemy.orm import Session

from src.domain.repository.order_line_repository import OrderLineRepository
from src.domain.shared.types import OrderReference
from src.domain.value_object.order_line import OrderLine
from src.infra.database.orm.sqlalchemy_orm.models.orderLine_model import (
    OrderLineModel,
)


class OrderLineSqlAlchemyRepository(OrderLineRepository):
    def __init__(self, session: Session):
        self._session: Session = session

    def add(self, order_line: OrderLine) -> None:
        order_line_Model = OrderLineModel.from_domain(order_line)
        self._session.add(order_line_Model)
        self._session.commit()

    def update(self, order_line: OrderLine) -> None:
        order_line_Model = (
            self._session.query(OrderLineModel)
            .filter(
                and_(
                    orderid=order_line.orderid,
                    sku=order_line.sku,
                    qty=order_line.qty,
                )
            )
            .first()
        )

        if order_line_Model:
            order_line_Model.orderid = order_line.orderid
            order_line_Model.qty = order_line.qty
            order_line_Model.sku = order_line.sku

            self._session.commit()

    def get(self, orderid: OrderReference) -> OrderLine:
        order_line_Model = (
            self._session.query(OrderLineModel)
            .filter(OrderLineModel.orderid == orderid)
            .first()
        )

        return order_line_Model.to_domain() if order_line_Model else None

    def remove(self, orderid: OrderReference) -> None:
        order_line_Model = (
            self._session.query(OrderLineModel)
            .filter(OrderLineModel.orderid == orderid)
            .first()
        )

        if order_line_Model:
            self._session.delete(order_line_Model)
            self._session.commit()
