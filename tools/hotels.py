"""
Hotel Search Tool
Simulated hotel data (replace with Booking.com/Hotels.com API in production).
Returns realistic hotel options for a destination and dates.
"""

import random

HOTEL_NAMES = {
    "paris":     ["Hotel Le Marais", "Montmartre Boutique", "Seine River Lodge", "Paris Grand Palace"],
    "london":    ["The Covent Garden Hotel", "Shoreditch Inn", "Thames View Hotel", "Kensington Suites"],
    "tokyo":     ["Shinjuku Grand", "Asakusa Ryokan", "Shibuya Crossing Hotel", "Tokyo Bay Resort"],
    "dubai":     ["Burj View Hotel", "Dubai Marina Resort", "Desert Palm Hotel", "JBR Beach Suites"],
    "bali":      ["Ubud Jungle Villa", "Seminyak Beach Resort", "Kuta Surf Hotel", "Uluwatu Cliffs"],
    "barcelona": ["Gothic Quarter Inn", "Barceloneta Beach Hotel", "Eixample Suites", "Gracia Boutique"],
    "default":   ["Grand Hotel", "City Center Inn", "Boutique Suites", "Traveller's Lodge"],
}

AMENITIES = [
    "Free WiFi, Breakfast included",
    "Pool, Gym, Free WiFi",
    "Breakfast, Airport Shuttle",
    "Rooftop Bar, Free WiFi, Spa",
    "Free WiFi, 24hr Reception",
]


def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    guests: int = 1
) -> str:
    """
    Search for hotels at a destination.

    Args:
        destination: City to search hotels in
        check_in:    Check-in date
        check_out:   Check-out date
        guests:      Number of guests

    Returns:
        Formatted string of hotel options
    """
    try:
        dest_lower = destination.lower().strip()

        # Find hotel names for destination
        hotel_list = HOTEL_NAMES.get("default")
        for key in HOTEL_NAMES:
            if key in dest_lower or dest_lower in key:
                hotel_list = HOTEL_NAMES[key]
                break

        # Seed for consistency
        seed = hash(f"{destination}{check_in}") % 10000
        random.seed(seed)

        hotels = []
        for name in hotel_list[:3]:
            stars      = random.randint(3, 5)
            price      = random.randint(60, 450)
            rating     = round(random.uniform(7.5, 9.8), 1)
            amenity    = random.choice(AMENITIES)
            star_str   = "⭐" * stars

            hotels.append(
                f"  🏨 {name} {star_str}\n"
                f"     Rating: {rating}/10 | ${price}/night/room | "
                f"{amenity}"
            )

        result = (
            f"Hotels in {destination} | Check-in: {check_in} | "
            f"Check-out: {check_out} | Guests: {guests}\n\n" +
            "\n\n".join(hotels) +
            f"\n\n  💡 Tip: Book refundable rates when dates may change."
        )
        return result

    except Exception as e:
        return f"Error searching hotels: {str(e)}"
