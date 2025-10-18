from pydantic import Basemodel, Field
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