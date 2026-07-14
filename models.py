"""
Structured output schemas for the AI-Crisis Command Center.

Each of the five agents is forced (via CrewAI's `output_pydantic`) to return
data that matches one of these models, instead of free-form prose. This is
what lets the Streamlit dashboard render tables and checklists directly,
rather than having to parse raw text.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class RiskAssessment(BaseModel):
    """Output of the Risk / Incident Analyst agent."""
    incident_type: str = Field(..., description="Short classification, e.g. 'Urban Flood', 'Gas Leak'")
    severity_level: str = Field(..., description="One of: Low, Moderate, High, Critical")
    affected_area_summary: str = Field(..., description="Plain-language summary of the affected zone")
    key_hazards: List[str] = Field(default_factory=list, description="Bullet list of immediate hazards")
    immediate_priorities: List[str] = Field(default_factory=list, description="Top 3-5 priority actions")


class ResourceItem(BaseModel):
    resource: str
    quantity: str
    assigned_location: str
    priority: str = Field(default="Medium", description="Low, Medium, High")


class ResourceAllocation(BaseModel):
    """Output of the Logistics / Resource Optimization agent."""
    resources: List[ResourceItem] = Field(default_factory=list)
    notes: Optional[str] = None


class RouteStep(BaseModel):
    origin: str
    destination: str
    mode: str = Field(..., description="e.g. Road, Boat, Air")
    status: str = Field(..., description="Open, Congested, Blocked")
    notes: Optional[str] = None


class RoutePlan(BaseModel):
    """Output of the Route Planner agent."""
    evacuation_routes: List[RouteStep] = Field(default_factory=list)
    rescue_access_routes: List[RouteStep] = Field(default_factory=list)


class TriageZone(BaseModel):
    zone_name: str
    condition: str = Field(..., description="e.g. 'Critical - crush injuries', 'Stable - minor injuries'")
    recommended_action: str


class TriagePlan(BaseModel):
    """Output of the Triage Director agent."""
    triage_zones: List[TriageZone] = Field(default_factory=list)
    medical_supply_priorities: List[str] = Field(default_factory=list)


class CommsBrief(BaseModel):
    """Output of the Communications Officer agent."""
    public_alert_message: str = Field(..., description="Ready-to-broadcast short public alert")
    recommended_channels: List[str] = Field(default_factory=list)
    key_dos_and_donts: List[str] = Field(default_factory=list)


class FullResponsePlan(BaseModel):
    """Aggregated result returned by the whole crew, used by the dashboard."""
    risk_assessment: RiskAssessment
    resource_allocation: ResourceAllocation
    route_plan: RoutePlan
    triage_plan: TriagePlan
    comms_brief: CommsBrief
