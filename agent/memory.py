"""
Trip Memory — stores the user's trip context and conversation history.
Combines buffer memory (recent exchanges) with structured trip data.
This is the memory component from the Key Skills list.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class TripContext:
    """Structured data extracted from the user's trip request."""
    destination:   str = ""
    origin:        str = ""
    start_date:    str = ""
    end_date:      str = ""
    travelers:     int = 1
    budget_style:  str = "mid"      # budget / mid / luxury
    interests:     str = "general"  # culture, food, adventure, etc.
    days:          int = 0
    raw_request:   str = ""

    def is_complete(self) -> bool:
        """Check if we have enough info to start planning."""
        return bool(self.destination and self.start_date)

    def summary(self) -> str:
        """Return a human-readable summary of the trip."""
        return (
            f"Trip to {self.destination} | "
            f"{self.start_date} → {self.end_date} | "
            f"{self.travelers} traveler(s) | "
            f"{self.days} day(s) | "
            f"{self.budget_style} budget | "
            f"Interests: {self.interests}"
        )


class TripMemory:
    """
    Memory system for the trip planner.

    Stores:
      - trip_context  : structured trip details (destination, dates, etc.)
      - conversation  : last N message exchanges (buffer memory)
      - plan_results  : what each tool returned (so we don't repeat calls)
      - full_plan     : the final assembled trip plan
    """

    def __init__(self, buffer_size: int = 10):
        self.trip_context: TripContext         = TripContext()
        self.conversation: List[Dict]          = []
        self.plan_results: Dict[str, str]      = {}
        self.full_plan:    str                 = ""
        self.buffer_size:  int                 = buffer_size

    def add_message(self, role: str, content: str):
        """Add a message to conversation buffer."""
        self.conversation.append({"role": role, "content": content})
        # Keep only last N messages
        if len(self.conversation) > self.buffer_size:
            self.conversation = self.conversation[-self.buffer_size:]

    def store_result(self, tool_name: str, result: str):
        """Store a tool result so it can be referenced later."""
        self.plan_results[tool_name] = result

    def get_result(self, tool_name: str) -> Optional[str]:
        """Retrieve a previously stored tool result."""
        return self.plan_results.get(tool_name)

    def has_result(self, tool_name: str) -> bool:
        """Check if we already have a result for this tool."""
        return tool_name in self.plan_results

    def get_context_string(self) -> str:
        """Return full context for injecting into prompts."""
        parts = []

        if self.trip_context.is_complete():
            parts.append(f"Trip Context: {self.trip_context.summary()}")

        if self.plan_results:
            parts.append("Already gathered information:")
            for tool, result in self.plan_results.items():
                parts.append(f"  [{tool}]: {result[:200]}...")

        return "\n".join(parts) if parts else "No context yet."

    def clear(self):
        """Reset all memory."""
        self.trip_context  = TripContext()
        self.conversation  = []
        self.plan_results  = {}
        self.full_plan     = ""

    def __repr__(self):
        return (
            f"TripMemory("
            f"destination={self.trip_context.destination!r}, "
            f"results={list(self.plan_results.keys())}, "
            f"messages={len(self.conversation)})"
        )
