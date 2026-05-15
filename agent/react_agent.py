"""
ReAct Agent — executes the trip plan using Thought → Action → Observation loop.
This is the REACT component from the Key Skills list.

For each sub-task in the plan:
  Thought   → why this task matters for the trip
  Action    → call the appropriate tool
  Observation → what the tool returned
  → move to next sub-task

After all tasks: synthesize into a complete trip plan.
"""

import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

from agent.memory   import TripMemory
from agent.planner  import decompose_trip, extract_trip_context, print_plan
from tools          import (
    search_flights,
    search_hotels,
    search_activities,
    get_weather,
    calculate_budget,
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Tool registry
TOOL_REGISTRY = {
    "search_flights":    search_flights,
    "search_hotels":     search_hotels,
    "search_activities": search_activities,
    "get_weather":       get_weather,
    "calculate_budget":  calculate_budget,
}


class TripPlannerAgent:
    """
    Trip Planner Agent combining:
      ✅ Planning     : decomposes trip into sub-tasks
      ✅ ReAct        : thinks before each tool call
      ✅ Tool use     : 5 specialized tools
      ✅ Memory       : stores context and results
    """

    def __init__(self, model_name: str = "gemini-2.5-flash-lite", verbose: bool = True):
        self.model   = genai.GenerativeModel(model_name)
        self.memory  = TripMemory()
        self.verbose = verbose

    def _call_llm(self, prompt: str, label: str = "") -> str:
        """Call Gemini with rate limit handling."""
        for attempt in range(3):
            try:
                if self.verbose and label:
                    print(f"    📡 [{label}]...")
                response = self.model.generate_content(prompt)
                time.sleep(3)
                return response.text.strip()
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    wait = 60 * (attempt + 1)
                    print(f"    ⚠️  Rate limit — waiting {wait}s...")
                    time.sleep(wait)
                else:
                    return f"LLM error: {str(e)}"
        return "Error: max retries exceeded"

    def _think(self, task: dict, context_str: str) -> str:
        """
        THOUGHT step — LLM reasons about why this task matters.
        Makes the agent's reasoning transparent (ReAct pattern).
        """
        prompt = (
            f"You are a trip planning agent.\n"
            f"Current trip context:\n{context_str}\n\n"
            f"Next task: {task['task']}\n"
            f"Tool to use: {task['tool']}\n\n"
            f"In one sentence, explain why this task is important "
            f"for planning this specific trip:"
        )
        return self._call_llm(prompt, "Thinking")

    def _execute_tool(self, task: dict) -> str:
        """
        ACTION + OBSERVATION steps — run the tool and return the result.
        """
        tool_fn = TOOL_REGISTRY.get(task["tool"])
        if not tool_fn:
            return f"Error: Tool '{task['tool']}' not found."

        try:
            result = tool_fn(**task["args"])
            return result
        except Exception as e:
            return f"Tool error: {str(e)}"

    def _synthesize_plan(self) -> str:
        """
        Final synthesis step — LLM assembles all tool results into
        a complete, readable trip plan.
        """
        ctx      = self.memory.trip_context
        results  = self.memory.plan_results

        results_text = "\n\n".join(
            f"=== {tool.replace('_', ' ').title()} ===\n{result}"
            for tool, result in results.items()
        )

        prompt = f"""You are an expert travel agent. 
Create a complete, well-structured trip plan using the information gathered below.

Trip: {ctx.summary()}

Gathered Information:
{results_text}

Write a comprehensive trip plan that includes:
1. 🌍 Trip Overview (destination, dates, travelers)
2. ✈️  Flight Recommendation (pick the best option and explain why)
3. 🏨 Hotel Recommendation (pick the best option and explain why)
4. 📅 Day-by-Day Itinerary (based on activities found)
5. 🌤️  Weather & Packing Tips
6. 💰 Budget Summary
7. 💡 Top 3 Travel Tips for this destination

Make it practical, friendly, and exciting. Use emojis for readability."""

        return self._call_llm(prompt, "Synthesizing plan")

    def plan_trip(self, user_input: str) -> str:
        """
        Main entry point — takes a natural language trip request
        and returns a complete trip plan.

        Full flow:
          1. Extract trip context from user input
          2. Decompose into sub-tasks (planning)
          3. For each sub-task: Think → Act → Observe (ReAct)
          4. Store results in memory
          5. Synthesize into final plan
        """
        print(f"\n{'='*60}")
        print(f"  🌍 TRIP PLANNER AGENT")
        print(f"{'='*60}")
        print(f"  Request: {user_input}")

        # ── Step 1: Extract trip context ──
        print(f"\n🔍 Extracting trip details...")
        context = extract_trip_context(user_input, self.model)
        self.memory.trip_context = context

        if not context.destination:
            return (
                "I couldn't identify a destination from your request. "
                "Please include a city name, e.g. 'Plan a trip to Paris from June 10-17'"
            )

        print(f"  ✅ Destination: {context.destination}")
        print(f"  ✅ Dates: {context.start_date} → {context.end_date}")
        print(f"  ✅ Travelers: {context.travelers} | Style: {context.budget_style}")

        # ── Step 2: Decompose into sub-tasks ──
        sub_tasks = decompose_trip(context)
        print_plan(sub_tasks, context)

        # ── Step 3: ReAct loop — execute each sub-task ──
        for i, task in enumerate(sub_tasks, 1):
            print(f"\n[Sub-task {i}/{len(sub_tasks)}] {task['emoji']} {task['task']}")

            # THOUGHT
            thought = self._think(task, self.memory.get_context_string())
            print(f"  💭 Thought: {thought}")

            # ACTION + OBSERVATION
            print(f"  🔧 Action: {task['tool']}({task['args']})")
            result = self._execute_tool(task)
            print(f"  👁️  Observation:\n")
            for line in result.split("\n"):
                print(f"    {line}")

            # Store in memory
            self.memory.store_result(task["tool"], result)
            self.memory.add_message("agent", f"Completed: {task['task']}")

        # ── Step 4: Synthesize final plan ──
        print(f"\n{'─'*60}")
        print(f"  📝 Synthesizing complete trip plan...")
        print(f"{'─'*60}")

        final_plan = self._synthesize_plan()
        self.memory.full_plan = final_plan

        return final_plan
