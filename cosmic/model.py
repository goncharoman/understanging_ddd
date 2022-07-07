from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


@dataclass(frozen=True)
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:

    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self._ref = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    @property
    def ref(self) -> str:
        return self._ref

    def allocate(self, order: OrderLine):
        if self.can_allocate(order):
            self._allocations.add(order)

    def can_allocate(self, order: OrderLine) -> bool:
        return self.sku == order.sku and self.available_quantity >= order.qty

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self) -> int:
        return sum(order.qty for order in self._allocations)

    def deallocate(self, order: OrderLine):
        if order in self._allocations:
            self._allocations.remove(order)

    def __hash__(self) -> int:
        return hash(self._ref)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._ref == other._ref
        return False

    def __gt__(self, other: Batch) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(order: OrderLine, batches: List[Batch]) -> str:
    batch = next(batch for batch in sorted(batches) if batch.can_allocate(order))
    batch.allocate(order)
    return batch.ref
