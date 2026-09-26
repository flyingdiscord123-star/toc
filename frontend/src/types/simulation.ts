export interface SimulationConfig {
  agents: {
    numAgents: number;
    greedyPercentage: number;
    cooperativePercentage: number;
    riskAversePercentage: number;
  };
  environment: {
    initialResources: number;
    regenerationRate: number;
    rounds: number;
  };
  governance: {
    quotaEnabled: boolean;
    quotaLimit: number;
    taxEnabled: boolean;
    taxRate: number;
  };
}

export interface ChartData {
  round: number;
  resourceLevel: number;
  averageWealth: number;
}

export interface SimulationResult {
  status: "Resource Sustained" | "Resource Collapsed";
  remainingResource: number;
  averageWealth: number;
  averageTrust: number;
  chartData: ChartData[];
  completedAt: string;
}

export interface MetricCardData {
  label: string;
  value: string;
  detail?: string;
  tone?: "teal" | "coral" | "ink" | "neutral";
}
