"""
Trip Planner Agent — Main Entry Point
PROJECT: Agentic AI Internship

Demonstrates:
  ✅ ReAct pattern    : Thought → Action → Observation loop
  ✅ Planning         : trip decomposed into ordered sub-tasks
  ✅ Tool use         : 5 specialized tools (flights, hotels, activities, weather, budget)
  ✅ Memory           : trip context + results stored across tool calls
"""

import os
from dotenv import load_dotenv
from agent.react_agent import TripPlannerAgent

load_dotenv()


def save_plan(plan: str, destination: str):
    """Save the trip plan to a text file."""
    filename = f"trip_plan_{destination.lower().replace(' ', '_')}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(plan)
    print(f"\n💾 Trip plan saved to '{filename}'")
    return filename


def run_demo():
    """Run a demo trip planning request."""
    demo_request = (
        "Plan a 5-day trip to Paris for 2 people, "
        "flying from London in June, mid-range budget, "
        "interested in culture and food."
    )

    print("🚀 Trip Planner Agent — Demo Mode")
    print(f"Demo request: {demo_request}\n")

    agent = TripPlannerAgent(verbose=True)
    plan  = agent.plan_trip(demo_request)

    print(f"\n{'='*60}")
    print("  🗺️  COMPLETE TRIP PLAN")
    print(f"{'='*60}\n")
    print(plan)

    save_plan(plan, "Paris")


def interactive_mode():
    """Let the user enter their own trip request."""
    print("\n🌍 Trip Planner Agent — Interactive Mode")
    print("Examples:")
    print("  • Plan a 7-day trip to Tokyo for 2, budget style")
    print("  • I want to visit Bali for 5 days in August, luxury")
    print("  • Weekend trip to London from Paris, 1 person\n")

    agent = TripPlannerAgent(verbose=True)

    while True:
        request = input("Your trip request (or 'quit'): ").strip()
        if request.lower() in ["quit", "exit", "q"]:
            break
        if not request:
            continue

        plan = agent.plan_trip(request)

        print(f"\n{'='*60}")
        print("  🗺️  YOUR COMPLETE TRIP PLAN")
        print(f"{'='*60}\n")
        print(plan)

        # Extract destination for filename
        dest = agent.memory.trip_context.destination or "trip"
        save_plan(plan, dest)

        print("\nPlan another trip? (or 'quit' to exit)")


if __name__ == "__main__":
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY not found in .env file.")
        print("   Add it: GEMINI_API_KEY=your-key-here")
        exit(1)

    print("🌍 Trip Planner Agent")
    print("=" * 60)
    print("1 → Demo  (Paris, 5 days, 2 people)")
    print("2 → Interactive (plan your own trip)")

    choice = input("\nYour choice (1 or 2): ").strip()

    if choice == "2":
        interactive_mode()
    else:
        run_demo()
