# AI-Crisis Command Center

A multi-agent pipeline (CrewAI + Gemini) that converts a single unstructured
incident report into a structured emergency response plan: risk assessment,
resource allocation, evacuation/rescue routes, medical triage plan, and a
ready-to-broadcast public alert — all shown on a live Streamlit dashboard.

## Setup

1. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key**

   Copy the example env file and paste your key into it — **do not** paste
   API keys into chat, commits, or screenshots. Get a key from
   [Google AI Studio](https://aistudio.google.com/app/apikey).

   ```bash
   cp .env.example .env
   # then edit .env and set GEMINI_API_KEY=...
   ```

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

   Streamlit will open the dashboard in your browser (default:
   `http://localhost:8501`).

## Project structure

```
ai-crisis-command-center/
├── app.py              # Streamlit dashboard (entry point)
├── crew.py             # CrewAI agents, tasks, and pipeline orchestration
├── models.py            # Pydantic schemas for structured agent output
├── requirements.txt
├── .env.example
└── README.md
```

## How it works

Five agents run **sequentially** via CrewAI's `Process.sequential`, each
receiving the prior agents' outputs as context:

1. **Risk Analyst** — classifies the incident and identifies hazards/priorities
2. **Logistics Lead** — allocates personnel, vehicles, and supplies
3. **Route Planner** — plans evacuation and rescue-access routes
4. **Triage Director** — defines medical triage zones and supply priorities
5. **Communications Officer** — drafts a public alert and channel plan

Each agent's output is constrained to a Pydantic schema (see `models.py`) via
CrewAI's `output_pydantic`, so the dashboard can render tables and checklists
directly instead of parsing free-form text.

## Notes on the synopsis's success metrics

- **Latency target (<20s):** actual latency depends on the Gemini API and
  network conditions; `app.py` reports elapsed time after each run so you can
  measure this against real usage.
- **Re-render safety:** results are cached in `st.session_state`, so
  Streamlit UI interactions (tab switches, checkbox clicks) don't re-trigger
  the pipeline or new API calls — only clicking "Generate Response Plan" does.
