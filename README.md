# 🌍 Trip Planner Agent

An intelligent trip planning agent built with **Python + Gemini API**, demonstrating core **Agentic AI design patterns** from my internship project.

## 🧠 Agentic Patterns Used

| Pattern | Where | Description |
|---|---|---|
| **ReAct** | `agent/react_agent.py` | Thought → Action → Observation loop for each sub-task |
| **Planning** | `agent/planner.py` | Decomposes trip into ordered sub-tasks before execution |
| **Tool Use** | `tools/` | 5 specialized tools called by the agent |
| **Memory** | `agent/memory.py` | Stores trip context + tool results across calls |

## 🛠️ Tools

| Tool | Description | API |
|---|---|---|
| `search_flights` | Finds available flights for a route | Simulated |
| `search_hotels` | Finds hotels at destination | Simulated |
| `search_activities` | Recommends activities & attractions | Simulated |
| `get_weather` | Fetches real current weather | Open-Meteo (free) |
| `calculate_budget` | Estimates total trip cost | Local calculation |

## 📁 Project Structure

```
trip-planner-agent/
├── .env                    # API keys (not committed)
├── .gitignore
├── README.md
├── requirements.txt
├── main.py                 # Entry point
├── agent/
│   ├── planner.py          # Trip decomposition
│   ├── react_agent.py      # ReAct execution loop
│   └── memory.py           # Trip context + results storage
└── tools/
    ├── flights.py
    ├── hotels.py
    ├── activities.py
    ├── weather.py
    └── budget.py
```

## 🚀 Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/jubel-11/trip-planner-agent.git
cd trip-planner-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up API key
Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-gemini-api-key-here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

### 5. Run
```bash
python main.py
```

## 💡 Example Output

```
Request: Plan a 5-day trip to Paris for 2 people, mid-range budget

📋 TRIP DECOMPOSITION PLAN
  1. 🌤️  Check weather at destination
  2. ✈️  Search available flights
  3. 🏨 Find hotel options
  4. 🎯 Discover activities
  5. 💰 Calculate trip budget

[Sub-task 1/5] 🌤️ Check weather at destination
  💭 Thought: Knowing the weather helps with packing and activity planning
  🔧 Action: get_weather({"city": "Paris"})
  👁️  Observation: Weather in Paris: 22°C, Partly cloudy...

...

🗺️ COMPLETE TRIP PLAN
  Day 1: Arrival & Eiffel Tower
  Day 2: Louvre Museum & Seine Cruise
  ...
```

## 📚 References

- [ReAct Paper — Yao et al. 2022](https://openreview.net/pdf?id=vAElhFcKW6)
- [Andrew Ng — Agentic Design Patterns](https://www.youtube.com/watch?v=sal78ACtGTc)
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

## 👨‍💻 Author

**Jubelin Joji** — Agentic AI Project
