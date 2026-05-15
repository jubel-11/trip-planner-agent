"""
Budget Calculator Tool
Estimates total trip cost based on destination, duration, and travel style.
"""

# Cost of living index per city (daily estimates in USD per person)
CITY_COSTS = {
    "paris":     {"budget": 80,  "mid": 180, "luxury": 450},
    "london":    {"budget": 90,  "mid": 200, "luxury": 500},
    "tokyo":     {"budget": 65,  "mid": 150, "luxury": 400},
    "dubai":     {"budget": 100, "mid": 220, "luxury": 600},
    "bali":      {"budget": 35,  "mid": 85,  "luxury": 250},
    "bangkok":   {"budget": 30,  "mid": 75,  "luxury": 200},
    "barcelona": {"budget": 70,  "mid": 160, "luxury": 420},
    "amsterdam": {"budget": 85,  "mid": 190, "luxury": 480},
    "rome":      {"budget": 75,  "mid": 170, "luxury": 440},
    "singapore": {"budget": 80,  "mid": 180, "luxury": 500},
    "default":   {"budget": 60,  "mid": 140, "luxury": 350},
}

FLIGHT_ESTIMATES = {
    "budget": 300, "mid": 650, "luxury": 1500
}


def calculate_budget(
    destination: str,
    days: int,
    travelers: int = 1,
    travel_style: str = "mid"
) -> str:
    """
    Calculate estimated trip budget.

    Args:
        destination:  City of travel
        days:         Number of days
        travelers:    Number of travelers
        travel_style: 'budget', 'mid', or 'luxury'

    Returns:
        Detailed budget breakdown as a string
    """
    try:
        days      = int(days)
        travelers = int(travelers)
        style     = travel_style.lower().strip()

        if style not in ["budget", "mid", "luxury"]:
            style = "mid"

        dest_lower = destination.lower().strip()

        # Find cost data
        costs = CITY_COSTS.get("default")
        for key in CITY_COSTS:
            if key in dest_lower or dest_lower in key:
                costs = CITY_COSTS[key]
                break

        daily_per_person = costs[style]

        # Breakdown
        hotel_pct      = 0.40
        food_pct       = 0.30
        activities_pct = 0.20
        transport_pct  = 0.10

        daily_total     = daily_per_person * travelers
        stay_total      = daily_total * days
        flight_total    = FLIGHT_ESTIMATES[style] * travelers

        hotel_cost      = stay_total * hotel_pct
        food_cost       = stay_total * food_pct
        activity_cost   = stay_total * activities_pct
        transport_cost  = stay_total * transport_pct
        grand_total     = stay_total + flight_total

        result = (
            f"Budget Estimate — {destination} | {days} days | "
            f"{travelers} traveler(s) | {style.title()} style\n\n"
            f"  ✈️  Flights:        ${flight_total:,.0f}\n"
            f"  🏨 Hotel:          ${hotel_cost:,.0f}  (${hotel_cost/days:,.0f}/night)\n"
            f"  🍽️  Food:           ${food_cost:,.0f}  (${food_cost/days:,.0f}/day)\n"
            f"  🎯 Activities:     ${activity_cost:,.0f}\n"
            f"  🚌 Local Transport: ${transport_cost:,.0f}\n"
            f"  {'─'*40}\n"
            f"  💰 TOTAL ESTIMATE:  ${grand_total:,.0f} "
            f"(${grand_total/travelers:,.0f}/person)\n\n"
            f"  💡 Add 15% buffer for unexpected expenses: "
            f"${grand_total * 1.15:,.0f}"
        )
        return result

    except Exception as e:
        return f"Error calculating budget: {str(e)}"
