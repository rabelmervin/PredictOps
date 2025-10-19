from pydantic import BaseModel, Field
from typing import List

FEATURE_ORDER: List[str] = [
    "Revenue",
    "Gross Profit",
    "EBITDA(Earnings Before Interest, Taxes, Depreciation, and Amortization.)",
    "Share Holder Equity",
    "Cash Flow from Operating",
    "Net Profit Margin",
    "Return on Tangible Equity",
    "Number of Employees",
    "Profit_margin",
    "Revenue_per_employee",
    "Employee_productivity",
]


class PredictionRequest(BaseModel):
    # Python-safe field names, aliases map to original column names
    revenue: float = Field(..., alias="Revenue")
    gross_profit: float = Field(..., alias="Gross Profit")
    ebitda: float = Field(..., alias="EBITDA")
    share_holder_equity: float = Field(..., alias="Share Holder Equity")
    cash_flow_from_operating: float = Field(..., alias="Cash Flow from Operating")
    net_profit_margin: float = Field(..., alias="Net Profit Margin")
    return_on_tangible_equity: float = Field(..., alias="Return on Tangible Equity")
    number_of_employees: float = Field(..., alias="Number of Employees")
    profit_margin: float = Field(..., alias="Profit_margin")
    revenue_per_employee: float = Field(..., alias="Revenue_per_employee")
    employee_productivity: float = Field(..., alias="Employee_productivity")

    class Config:
        extra = "forbid"
        allow_population_by_field_name = True

    def as_feature_dict(self, by_alias: bool = True) -> dict:
        """Return a dict keyed by alias (original column names) or field names."""
        return self.dict(by_alias=by_alias)