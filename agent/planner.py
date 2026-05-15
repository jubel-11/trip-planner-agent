"""
Trip Planner — decomposes a user's trip request into ordered sub-tasks.
This is the PLANNING component from the Key Skills list.

Planning pattern used: hierarchical decomposition
  User request → sub-tasks → tool calls → assembled plan
"""

import os
import re
import time
import json
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
from agent.memory import TripContext, TripMemory

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def extract_trip_context(user_input: str, model) -> TripContext:
    """
    Use the LLM to extract structured trip details from natural language.

    Example input:  "I want to go to Paris from June 10-17, 2 people, mid budget"
    Example output: TripContext(destination="Paris", start_date="June 10", ...)
    """
    current_year = datetime.now().year
    prompt = f"""Extract trip details from this request and return ONLY valid JSON.
No extra text, no markdown, just the JSON object.

Today's date is {datetime.now().strftime("%B %d, %Y")}.
If the user specifies a year, use EXACTLY what they said.
If no year is mentioned, assume {current_year}.

User request: "{user_input}"

Return this exact JSON structure:
{{
  "destination": "city name or empty string",
  "origin": "departure city or empty string",
  "start_date": "date or empty string",
  "end_date": "date or empty string",
  "travelers": 1,
  "budget_style": "budget or mid or luxury",
  "interests": "comma separated interests or general",
  "days": 0
}}

Rules:
- days: calculate from dates if possible, else 0
- budget_style: infer from words like cheap/budget/luxury/backpacker
- interests: infer from words like food/culture/adventure/beach/history"""

    try:
        response = model.generate_content(prompt)
        raw      = response.text.strip()
        # Strip markdown fences
        clean    = re.sub(r"```(?:json)?|```", "", raw).strip()
        data     = json.loads(clean)

        ctx = TripContext(
            destination  = data.get("destination", ""),
            origin       = data.get("origin", ""),
            start_date   = data.get("start_date", ""),
            end_date     = data.get("end_date", ""),
            travelers    = int(data.get("travelers", 1)),
            budget_style = data.get("budget_style", "mid"),
            interests    = data.get("interests", "general"),
            days         = int(data.get("days", 0)),
            raw_request  = user_input,
        )
        time.sleep(2)
        return ctx

    except Exception as e:
        print(f"  ⚠️  Could not parse trip details: {e}")
        return TripContext(raw_request=user_input)


def decompose_trip(context: TripContext) -> list:
    """
    Decompose a trip into an ordered list of sub-tasks.
    Each sub-task maps to a specific tool call.

    This is the planning step — before any tool is called,
    we figure out WHAT needs to be done and IN WHAT ORDER.

    Returns:
        List of dicts: [{"task": str, "tool": str, "args": dict}, ...]
    """
    days = context.days if context.days > 0 else 5

    sub_tasks = [
        {
            "task":  "Check weather at destination",
            "tool":  "get_weather",
            "args":  {"city": context.destination},
            "emoji": "🌤️",
        },
        {
            "task":  "Search available flights",
            "tool":  "search_flights",
            "args":  {
                "origin":      context.origin or "home city",
                "destination": context.destination,
                "date":        context.start_date,
                "passengers":  context.travelers,
            },
            "emoji": "✈️",
        },
        {
            "task":  "Find hotel options",
            "tool":  "search_hotels",
            "args":  {
                "destination": context.destination,
                "check_in":    context.start_date,
                "check_out":   context.end_date,
                "guests":      context.travelers,
            },
            "emoji": "🏨",
        },
        {
            "task":  "Discover activities",
            "tool":  "search_activities",
            "args":  {
                "destination": context.destination,
                "interests":   context.interests,
                "days":        days,
            },
            "emoji": "🎯",
        },
        {
            "task":  "Calculate trip budget",
            "tool":  "calculate_budget",
            "args":  {
                "destination":  context.destination,
                "days":         days,
                "travelers":    context.travelers,
                "travel_style": context.budget_style,
            },
            "emoji": "💰",
        },
    ]

    return sub_tasks


def print_plan(sub_tasks: list, context: TripContext):
    """Print the decomposed plan before execution."""
    print(f"\n{'─'*60}")
    print(f"  📋 TRIP DECOMPOSITION PLAN")
    print(f"  {context.summary()}")
    print(f"{'─'*60}")
    print(f"  Sub-tasks to execute:")
    for i, task in enumerate(sub_tasks, 1):
        print(f"  {i}. {task['emoji']} {task['task']}")
    print(f"{'─'*60}\n")
