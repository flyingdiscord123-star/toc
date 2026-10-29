from pydantic import BaseModel, Field


class AgentSettings(BaseModel):
	num_agents: int = Field(alias="numAgents", gt=0)
	greedy_percentage: float = Field(alias="greedyPercentage", ge=0, le=100)
	cooperative_percentage: float = Field(
		alias="cooperativePercentage", ge=0, le=100
	)
	risk_averse_percentage: float = Field(
		alias="riskAversePercentage", ge=0, le=100
	)


class EnvironmentSettings(BaseModel):
	initial_resources: float = Field(alias="initialResources", ge=0)
	regeneration_rate: float = Field(alias="regenerationRate", ge=0)
	rounds: int = Field(gt=0)


class GovernanceSettings(BaseModel):
	quota_enabled: bool = Field(alias="quotaEnabled")
	quota_limit: float = Field(alias="quotaLimit", ge=0)
	tax_enabled: bool = Field(alias="taxEnabled")
	tax_rate: float = Field(alias="taxRate", ge=0, le=1)


class SimulationRequest(BaseModel):
	agents: AgentSettings
	environment: EnvironmentSettings
	governance: GovernanceSettings
