#by iremebrar
# ============================
# New Dynamic Pricing System
# ============================

from dataclasses import dataclass


@dataclass(frozen=True)
class PricingConfig:
    """
    Configuration for dynamic seat pricing.
    """

    base_prices = {
        "economy": 100,
        "business": 300,
        "first": 600,
    }

    # Price multiplier depending on seat position
    seat_type_multiplier = {
        "window": 1.20,   # Window seats are more expensive
        "aisle": 1.10,    # Aisle seats have slightly higher price
        "middle": 1.00,   # Middle seats have base price
    }

    # When more than 80% of seats are occupied,
    # surge pricing starts
    surge_threshold = 0.80

    # Maximum price increase: 30%
    surge_max = 0.30


def get_price(
    seat_type: str,
    seat_class: str,
    occupancy_ratio: float,
    config: PricingConfig = PricingConfig()
) -> float:
    """
    Calculate dynamic seat price based on:
    - Seat class
    - Seat position
    - Current occupancy rate
    """

    base = config.base_prices.get(seat_class.lower(), 100)
    multiplier = config.seat_type_multiplier.get(seat_type.lower(), 1.0)

    surge = 0.0

    # Apply surge pricing if plane is almost full
    if occupancy_ratio > config.surge_threshold:
        progress = (
            (occupancy_ratio - config.surge_threshold)
            / (1.0 - config.surge_threshold)
        )
        surge = min(progress * config.surge_max, config.surge_max)

    price = base * multiplier * (1.0 + surge)

    return round(price, 2)


def get_price_from_seat(seat, seat_class: str, occupancy_ratio: float) -> float:
    """
    Helper function:
    Calculates price directly from Seat object.
    """

    seat_type = getattr(seat, "name", "middle")

    return get_price(
        seat_type=seat_type,
        seat_class=seat_class,
        occupancy_ratio=occupancy_ratio
    )
