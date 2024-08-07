from sqlalchemy import text

from src.domain.value_object.order_line import OrderLine
from src.infra.database.orm.sqlalchemy_orm.models.orderLine_model import (
    OrderLineModel,
)


def test_orderline_mapper_can_load_lines(session):
    session.add_all([
        OrderLineModel('order1', 'RED-CHAIR', 12),
        OrderLineModel('order1', 'RED-TABLE', 13),
        OrderLineModel('order2', 'BLUE-LIPSTICK', 14),
    ])

    session.commit()

    expected = 3

    assert len(session.query(OrderLineModel).all()) == expected


def test_orderline_mapper_can_save_lines(session):
    order_line_entity = OrderLine('order1', 'DECORATIVE-WIDGET', 12)
    new_line = OrderLineModel.from_domain(order_line_entity)
    session.add(new_line)
    session.commit()

    rows = list(
        session.execute(text('SELECT orderid, sku, qty FROM "order_lines"'))
    )
    assert rows == [('order1', 'DECORATIVE-WIDGET', 12)]
