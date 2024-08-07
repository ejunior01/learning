import pytest

from src.domain.entities.batch import Batch
from src.domain.errors.out_of_stock_error import OutOfStockError
from src.domain.services.allocate import allocate
from src.domain.value_object.order_line import OrderLine
from src.shared.utils import after_tomorrow, today, tomorrow


def make_batch_and_line(sku, batch_qty, line_qty):
    return (
        Batch(ref='batch-001', sku=sku, qty=batch_qty, eta=today()),
        OrderLine('order-ref', sku=sku, qty=line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    EXPECTED_QUANTITY = 18
    batch = Batch(ref='batch-001', sku='SMALL-TABLE', qty=20, eta=today())
    line = OrderLine('order-ref', 'SMALL-TABLE', 2)

    batch.allocate(line)

    assert batch.available_quantity == EXPECTED_QUANTITY


def test_can_allocate_if_available_greater_than_required():
    large_batch, small_line = make_batch_and_line('ELEGANT-LAMP', 20, 2)
    assert large_batch.can_allocate(small_line)


def test_cannot_allocate_if_available_smaller_than_required():
    small_batch, large_line = make_batch_and_line('ELEGANT-LAMP', 2, 20)
    assert small_batch.can_allocate(large_line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_line('ELEGANT-LAMP', 2, 2)
    assert batch.can_allocate(line)


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch('batch-001', 'UNCOMFORTABLE-CHAIR', 100, eta=None)
    different_sku_line = OrderLine('order-123', 'EXPENSIVE-TOASTER', 10)
    assert batch.can_allocate(different_sku_line) is False


def test_can_only_deallocate_allocated_lines():
    EXPECTED_QUANTITY = 20

    batch, unallocated_line = make_batch_and_line('DECORATIVE-TRINKET', 20, 2)
    batch.deallocate(unallocated_line)

    assert batch.available_quantity == EXPECTED_QUANTITY


def test_allocation_is_idempotent():
    EXPECTED_QUANTITY = 18

    batch, line = make_batch_and_line('ANGULAR-DESK', 20, 2)
    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == EXPECTED_QUANTITY


def test_prefers_current_stock_batches_to_shipments():
    EXPECTED_IN_STOCK_QUANTITY = 90
    EXPECTED_SHIPMENT_QUANTITY = 100

    in_stock_batch = Batch('in-stock-batch', 'RETRO-CLOCK', 100, eta=None)
    shipment_batch = Batch('shipment-batch', 'RETRO-CLOCK', 100, eta=today())
    line = OrderLine('oref', 'RETRO-CLOCK', 10)

    allocate(line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == EXPECTED_IN_STOCK_QUANTITY
    assert shipment_batch.available_quantity == EXPECTED_SHIPMENT_QUANTITY


def test_prefers_earlier_batches():
    EXPECTED_EARLIEST_QUANTITY = 90
    EXPECTED_MEDIUM_QUANTITY = 100
    EXPECTED_LATEST_QUANTITY = 100

    earliest = Batch('speedy-batch', 'MINIMALIST-SPOON', 100, eta=today())
    medium = Batch('normal-batch', 'MINIMALIST-SPOON', 100, eta=tomorrow())
    latest = Batch('slow-batch', 'MINIMALIST-SPOON', 100, eta=after_tomorrow())
    line = OrderLine('order1', 'MINIMALIST-SPOON', 10)

    allocate(line, [medium, earliest, latest])

    assert earliest.available_quantity == EXPECTED_EARLIEST_QUANTITY
    assert medium.available_quantity == EXPECTED_MEDIUM_QUANTITY
    assert latest.available_quantity == EXPECTED_LATEST_QUANTITY


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch(
        'in-stock-batch-ref', 'HIGHBROW-POSTER', 100, eta=None
    )
    shipment_batch = Batch(
        'shipment-batch-ref', 'HIGHBROW-POSTER', 100, eta=tomorrow()
    )
    line = OrderLine('oref', 'HIGHBROW-POSTER', 10)

    allocation = allocate(line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.reference


def test_raises_out_of_stock_exception_if_cannot_allocate():
    batch = Batch('batch1', 'SMALL-FORK', 10, eta=today())
    allocate(OrderLine('order1', 'SMALL-FORK', 10), [batch])

    with pytest.raises(OutOfStockError, match='SMALL-FORK'):
        allocate(OrderLine('order2', 'SMALL-FORK', 1), [batch])
