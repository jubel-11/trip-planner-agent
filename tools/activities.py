"""
Activities Search Tool
Simulated activities data (replace with Viator/GetYourGuide API in production).
Returns top activities and attractions for a destination.
"""

import random

ACTIVITIES_DB = {
    "paris": [
        ("Eiffel Tower Visit", 35, "3h", "Landmark"),
        ("Louvre Museum Tour", 22, "4h", "Culture"),
        ("Seine River Cruise", 18, "1.5h", "Sightseeing"),
        ("Versailles Day Trip", 55, "6h", "History"),
        ("Montmartre Walking Tour", 0, "2h", "Free"),
        ("French Cooking Class", 95, "3h", "Experience"),
    ],
    "tokyo": [
        ("Senso-ji Temple Visit", 0, "2h", "Culture"),
        ("TeamLab Planets", 32, "2h", "Art"),
        ("Mount Fuji Day Trip", 85, "10h", "Nature"),
        ("Shibuya Crossing Tour", 0, "1h", "Free"),
        ("Sushi Making Class", 75, "2.5h", "Experience"),
        ("Akihabara Electronics Tour", 0, "3h", "Free"),
    ],
    "bali": [
        ("Ubud Monkey Forest", 4, "2h", "Nature"),
        ("Tanah Lot Sunset", 3, "2h", "Landmark"),
        ("Rice Terrace Trekking", 25, "4h", "Adventure"),
        ("Balinese Cooking Class", 45, "3h", "Experience"),
        ("Uluwatu Temple & Kecak", 8, "3h", "Culture"),
        ("Surfing Lesson Kuta", 35, "2h", "Adventure"),
    ],
    "london": [
        ("British Museum", 0, "3h", "Culture"),
        ("Tower of London", 35, "2.5h", "History"),
        ("Thames River Cruise", 20, "1h", "Sightseeing"),
        ("Harry Potter Studio Tour", 55, "4h", "Experience"),
        ("Changing of the Guard", 0, "1h", "Free"),
        ("West End Show", 75, "3h", "Entertainment"),
    ],
    "default": [
        ("City Walking Tour", 15, "2h", "Sightseeing"),
        ("Local Food Tour", 45, "3h", "Experience"),
        ("Museum Visit", 12, "2h", "Culture"),
        ("Day Trip to Countryside", 55, "8h", "Nature"),
        ("Cooking Class", 65, "3h", "Experience"),
        ("Sunset Viewpoint Tour", 0, "1h", "Free"),
    ],
}


def search_activities(
    destination: str,
    interests: str = "general",
    days: int = 3
) -> str:
    """
    Search for activities and attractions at a destination.

    Args:
        destination: City to search activities in
        interests:   Type of activities (culture, adventure, food, etc.)
        days:        Number of days to plan for

    Returns:
        Formatted string of activity recommendations
    """
    try:
        dest_lower = destination.lower().strip()

        # Find activities for destination
        activity_list = ACTIVITIES_DB.get("default")
        for key in ACTIVITIES_DB:
            if key in dest_lower or dest_lower in key:
                activity_list = ACTIVITIES_DB[key]
                break

        # Select activities based on days (2 per day)
        count    = min(days * 2, len(activity_list))
        selected = activity_list[:count]

        activities = []
        total_cost = 0
        for name, price, duration, category in selected:
            price_str   = "Free" if price == 0 else f"${price}/person"
            total_cost += price
            activities.append(
                f"  🎯 {name}\n"
                f"     Category: {category} | Duration: {duration} | {price_str}"
            )

        result = (
            f"Top activities in {destination} for {days} day(s) "
            f"(interests: {interests}):\n\n" +
            "\n\n".join(activities) +
            f"\n\n  💰 Estimated activities cost: ${total_cost}/person"
            f"\n  💡 Tip: Book popular attractions in advance to skip queues."
        )
        return result

    except Exception as e:
        return f"Error searching activities: {str(e)}"
