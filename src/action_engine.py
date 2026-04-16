def recommend_actions(risk_level, z_score, forecast_risk, insights=None):
    actions = []

    if z_score < -2:
        actions.append({
            "team": "Marketing",
            "action": "Analyze conversion funnel and campaign performance",
            "priority": "HIGH",
            "expected_impact": "Recover lost revenue"
        })

    if z_score > 2:
        actions.append({
            "team": "Operations",
            "action": "Ensure inventory and fulfillment readiness",
            "priority": "MEDIUM",
            "expected_impact": "Avoid stockouts"
        })

    if forecast_risk:
        actions.append({
            "team": "Finance",
            "action": "Adjust revenue forecasts and budgets",
            "priority": "HIGH",
            "expected_impact": "Reduce financial risk"
        })

    # 🔥 NEW: Insight-driven actions
    if insights:
        for ins in insights:
            if "declining" in ins:
                actions.append({
                    "team": "Marketing",
                    "action": "Run targeted campaigns",
                    "priority": "HIGH",
                    "expected_impact": "Boost revenue"
                })

            if "volatile" in ins:
                actions.append({
                    "team": "Analytics",
                    "action": "Investigate revenue fluctuations",
                    "priority": "MEDIUM",
                    "expected_impact": "Stabilize performance"
                })

    if not actions:
        actions.append({
            "team": "Analytics",
            "action": "Monitor KPIs",
            "priority": "LOW",
            "expected_impact": "Maintain stability"
        })

    return actions