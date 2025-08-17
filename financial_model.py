import pandas as pd
import numpy as np

# Load assumptions
assump = pd.read_excel("data/assumptions.xlsx")

years = list(range(2025, 2030))
revenue_growth = assump["revenue_growth"].values[0]
cogs_percent = assump["cogs_percent"].values[0]
opex_percent = assump["opex_percent"].values[0]
dep_percent = assump["dep_percent"].values[0]
interest_rate = assump["interest_rate"].values[0]
tax_rate = assump["tax_rate"].values[0]
initial_revenue = assump["initial_revenue"].values[0]
initial_debt = assump["initial_debt"].values[0]

# Projections
revenue = [initial_revenue]
cogs, opex, depreciation, ebit, interest, taxes, net_income = [], [], [], [], [], [], []
debt, cash_flow = [initial_debt], []

for year in years:
    rev = revenue[-1] * (1 + revenue_growth)
    cogs_val = rev * cogs_percent
    opex_val = rev * opex_percent
    dep_val = rev * dep_percent
    ebit_val = rev - cogs_val - opex_val - dep_val
    int_val = debt[-1] * interest_rate
    tax_val = max(0, (ebit_val - int_val) * tax_rate)
    ni = ebit_val - int_val - tax_val
    cf = ni + dep_val
    
    # Simple debt repayment assumption: use half of cash flow
    debt_repay = min(debt[-1], cf * 0.5)
    debt_new = debt[-1] - debt_repay
    
    # Append
    revenue.append(rev)
    cogs.append(cogs_val)
    opex.append(opex_val)
    depreciation.append(dep_val)
    ebit.append(ebit_val)
    interest.append(int_val)
    taxes.append(tax_val)
    net_income.append(ni)
    cash_flow.append(cf)
    debt.append(debt_new)

# Build financial statement DataFrame
df = pd.DataFrame({
    "Year": years,
    "Revenue": revenue[1:],
    "COGS": cogs,
    "OPEX": opex,
    "Depreciation": depreciation,
    "EBIT": ebit,
    "Interest": interest,
    "Taxes": taxes,
    "Net Income": net_income,
    "Operating Cash Flow": cash_flow,
    "Debt": debt[1:]
})

df.to_csv("results/projections.csv", index=False)
print("✅ Financial model saved to results/projections.csv")
