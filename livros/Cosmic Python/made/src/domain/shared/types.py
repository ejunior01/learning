from typing import NewType

Quantity = NewType('Quantity', int)
Sku = NewType('Sku', str)
Reference = NewType('Reference', str)

OrderReference = NewType('OrderReference', str)
ProductReference = NewType('ProductReference', str)
