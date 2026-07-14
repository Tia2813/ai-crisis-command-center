"""
Defines the five specialized agents, their sequential tasks, and assembles
them into a CrewAI Crew. This is the orchestration core of the AI-Crisis
Command Center.

Agents (run in sequence, each passing structured context to the next):
    1. Risk Analyst           -> RiskAssessment
    2. Logistics Lead         -> ResourceAllocation
    3. Route Planner          -> RoutePlan
    4. Triage Director        -> TriagePlan
    5. Communications Officer -> CommsBrief
"""

import os
from crewai import Agent, Task, Crew, Process, LLM

from models import (
    RiskAssessment,
    ResourceAllocation,
    RoutePlan,
    TriagePlan,
    CommsBrief,
)


def build_llm() -> LLM:
    """
    Builds the Gemini LLM connector used by every agent.

    CrewAI routes model calls through LiteLLM, which expects Gemini models
    to be referenced as 'gemini/<model-name>' and reads the API key from the
    GEMINI_API_KEY environment variable (loaded from .env by app.py).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Add it to your .env file "
            "(copy .env.example to .env and fill in your key)."
        )
    return LLM(
        model="gemini/gemini-3.5-flash",
        api_key=api_key,
        temperature=0.3,
    )


def build_crew(incident_report: str) -> Crew:
    llm = build_llm()

    # ---- Agents -----------------------------------------------------
    risk_analyst = Agent(
        role="Risk Analyst",
        goal="Rapidly classify the incident and identify immediate hazards and priorities.",
        backstory=(
            "A veteran disaster-response analyst who has triaged hundreds of incident "
            "reports and can spot the true severity of a situation within seconds, "
            "cutting through panic and noise in raw field reports."
        ),
        llm=llm,
        verbose=False,
    )

    logistics_lead = Agent(
        role="Logistics Lead",
        goal="Determine what resources (personnel, equipment, supplies) are needed and where.",
        backstory=(
            "A former military logistics officer specialized in rapidly allocating "
            "scarce rescue equipment and personnel during the first golden hour of a disaster."
        ),
        llm=llm,
        verbose=False,
    )

    route_planner = Agent(
        role="Route Planner",
        goal="Plan safe evacuation routes for civilians and access routes for rescue teams.",
        backstory=(
            "A GIS and transportation specialist who has planned evacuation corridors "
            "for floods, earthquakes, and industrial accidents, always accounting for "
            "road status, congestion, and hazard zones."
        ),
        llm=llm,
        verbose=False,
    )

    triage_director = Agent(
        role="Triage Director",
        goal="Organize medical triage zones and prioritize medical response.",
        backstory=(
            "An emergency-medicine physician experienced in mass-casualty triage, "
            "skilled at rapidly zoning casualties by severity and directing supplies "
            "to where they save the most lives."
        ),
        llm=llm,
        verbose=False,
    )

    comms_officer = Agent(
        role="Communications Officer",
        goal="Draft a clear, calm, actionable public alert message and channel plan.",
        backstory=(
            "A public-information officer skilled at turning technical response plans "
            "into short, calm, unambiguous public communications that prevent panic."
        ),
        llm=llm,
        verbose=False,
    )

    # ---- Tasks (sequential, each context-chained to the previous) ---
    risk_task = Task(
        description=(
            "Analyze the following raw, unstructured incident report and produce a "
            "structured risk assessment.\n\nINCIDENT REPORT:\n" + incident_report
        ),
        expected_output="A structured risk assessment.",
        agent=risk_analyst,
        output_pydantic=RiskAssessment,
    )

    logistics_task = Task(
        description=(
            "Using the risk assessment from the previous step, determine the resources "
            "(personnel, vehicles, equipment, medical/relief supplies) needed and where "
            "each should be assigned. Be specific about quantities where possible."
        ),
        expected_output="A structured resource allocation table.",
        agent=logistics_lead,
        context=[risk_task],
        output_pydantic=ResourceAllocation,
    )

    route_task = Task(
        description=(
            "Using the risk assessment and resource allocation from the previous steps, "
            "plan safe civilian evacuation routes and separate rescue-team access routes. "
            "Flag any routes likely to be congested or blocked given the incident type."
        ),
        expected_output="A structured route plan.",
        agent=route_planner,
        context=[risk_task, logistics_task],
        output_pydantic=RoutePlan,
    )

    triage_task = Task(
        description=(
            "Using the risk assessment and resource allocation, define medical triage "
            "zones and the medical supply priorities for this incident."
        ),
        expected_output="A structured triage plan.",
        agent=triage_director,
        context=[risk_task, logistics_task],
        output_pydantic=TriagePlan,
    )

    comms_task = Task(
        description=(
            "Using all prior outputs (risk assessment, resource allocation, route plan, "
            "triage plan), draft a short, calm, ready-to-broadcast public alert message, "
            "recommended communication channels, and a few key dos/don'ts for the public."
        ),
        expected_output="A structured public communications brief.",
        agent=comms_officer,
        context=[risk_task, logistics_task, route_task, triage_task],
        output_pydantic=CommsBrief,
    )

    return Crew(
        agents=[risk_analyst, logistics_lead, route_planner, triage_director, comms_officer],
        tasks=[risk_task, logistics_task, route_task, triage_task, comms_task],
        process=Process.sequential,
        verbose=False,
    )


def run_pipeline(incident_report: str):
    """
    Runs the full 5-agent crew against a raw incident report and returns the
    five structured pydantic outputs as a tuple:
    (risk_assessment, resource_allocation, route_plan, triage_plan, comms_brief)
    """
    crew = build_crew(incident_report)
    crew.kickoff()

    tasks = crew.tasks
    risk = tasks[0].output.pydantic
    resources = tasks[1].output.pydantic
    routes = tasks[2].output.pydantic
    triage = tasks[3].output.pydantic
    comms = tasks[4].output.pydantic

    return risk, resources, routes, triage, comms
