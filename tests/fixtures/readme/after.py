from decimal import Decimal
from typing import Iterable


def receipt(
    items: Iterable[tuple[str, Decimal]],
    discount: Decimal = Decimal("0"),
) -> str:
    """Format a receipt from named prices.

    Apply the discount after summing all line items.
    """
    if not 0 <= discount <= 1:
        raise ValueError("discount must be between 0 and 1")

    prices = {name: price for name, price in items}
    subtotal = sum(prices.values(), start=Decimal("0"))
    total = subtotal * (1 - discount)
    total = total.quantize(Decimal("0.01"))
    count = len(prices)
    label = "item" if count == 1 else "items"

    return (
        f"{count} {label}: ${total:,.2f}\n"
        f"Discount: {discount:.0%}"
    )
