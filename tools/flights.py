"""
Flight Search Tool
Simulated flight data (replace with Amadeus/Skyscanner API in production).
Returns realistic flight options for a given route and date.
"""

import random
from datetime import datetime, timedelta


# Simulated airline data
AIRLINES = [
    "Air India", "IndiGo", "Emirates", "Qatar Airways",
    "Singapore Airlines", "Lufthansa", "British Airways"
]

HUB_AIRPORTS = {
    "paris": "CDG", "london": "LHR", "tokyo": "NRT",
    "dubai": "DXB", "new york": "JFK", "singapore": "SIN",
    "bangkok": "BKK", "bali": "DPS", "rome": "FCO",
    "barcelona": "BCN", "amsterdam": "AMS", "sydney": "SYD",
    "india": "DEL", "mumbai": "BOM", "kerala": "COK",
    "trivandrum": "TRV", "cochin": "COK", "delhi": "DEL",
}


def get_airport_code(city: str) -> str:
    """Get airport code for a city."""
    city_lower = city.lower().strip()
    for key, code in HUB_AIRPORTS.items():
        if key in city_lower or city_lower in key:
            return code
    # Generate a plausible code from city name
    return city[:3].upper()


def search_flights(
    origin: str,
    destination: str,
    date: str,
    passengers: int = 1
) -> str:
    """
    Search for available flights between two cities.

    Args:
        origin:      Departure city
        destination: Arrival city
        date:        Travel date (YYYY-MM-DD or natural language)
        passengers:  Number of passengers

    Returns:
        Formatted string of flight options
    """
    try:
        origin_code = get_airport_code(origin)
        dest_code   = get_airport_code(destination)

        # Seed random for consistent results per route
        seed = hash(f"{origin}{destination}{date}") % 10000
        random.seed(seed)

        flights = []
        for i in range(3):
            airline     = random.choice(AIRLINES)
            base_price  = random.randint(250, 1200)
            price       = base_price * passengers
            duration_h  = random.randint(3, 16)
            duration_m  = random.choice([0, 15, 30, 45])
            depart_h    = random.randint(5, 22)
            depart_m    = random.choice([0, 15, 30, 45])
            stops       = random.choice([0, 0, 1])  # 2/3 chance nonstop

            stop_str    = "Nonstop" if stops == 0 else "1 stop"
            depart_str  = f"{depart_h:02d}:{depart_m:02d}"
            arrive_h    = (depart_h + duration_h) % 24
            arrive_str  = f"{arrive_h:02d}:{depart_m:02d}"

            flights.append(
                f"  ✈️  {airline} | {origin_code}→{dest_code} | "
                f"Departs {depart_str} Arrives {arrive_str} | "
                f"{duration_h}h {duration_m}m | {stop_str} | "
                f"${price:,} for {passengers} passenger(s)"
            )

        result = (
            f"Flights from {origin} to {destination} on {date} "
            f"({passengers} passenger(s)):\n" + "\n".join(flights) +
            f"\n  💡 Tip: Book the earliest flight for best hotel check-in."
        )
        return result

    except Exception as e:
        return f"Error searching flights: {str(e)}"
