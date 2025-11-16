from pydantic import BaseModel, Field, ConfigDict
from typing import List

FEATURE_ORDER: List[str] = [
    "Revenue",
    "Gross Profit",
    "EBITDA",
    "Share Holder Equity",
    "Operating Expenses",
    "Net Income",
    "Total Assets",
    "Total Liabilities",
]


class PredictionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    # Financial metrics - the model now expects 8 features
    revenue: float = Field(..., alias="Revenue", description="Total revenue")
    gross_profit: float = Field(..., alias="Gross Profit", description="Gross profit")
    ebitda: float = Field(..., alias="EBITDA", description="EBITDA")
    share_holder_equity: float = Field(..., alias="Share Holder Equity", description="Shareholder equity")
    operating_expenses: float = Field(..., alias="Operating Expenses", description="Operating expenses")
    net_income: float = Field(..., alias="Net Income", description="Net income")
    total_assets: float = Field(..., alias="Total Assets", description="Total assets")
    total_liabilities: float = Field(..., alias="Total Liabilities", description="Total liabilities")
    
    def as_feature_dict(self, by_alias: bool = True) -> dict:
        """Return a dict keyed by alias (original column names) or field names."""
        if by_alias:
            return {
                "Revenue": self.revenue,
                "Gross Profit": self.gross_profit,
                "EBITDA": self.ebitda,
                "Share Holder Equity": self.share_holder_equity,
                "Operating Expenses": self.operating_expenses,
                "Net Income": self.net_income,
                "Total Assets": self.total_assets,
                "Total Liabilities": self.total_liabilities,
            }
        else:
            return self.model_dump()
