def recommend_actions(risk_level, z_score, forecast_risk):
    """
    Maps detected risk patterns to concrete business actions
    """

    actions = []

    # -----------------------------
    # Revenue Drop Scenarios
    # -----------------------------
    if z_score < -2:
        actions.append({
            "team": "Marketing",
            "action": "Analyze conversion funnel and recent campaign performance",
            "priority": "HIGH",
            "expected_impact": "Recover lost conversions and stabilize revenue"
        })

        actions.append({
            "team": "Product",
            "action": "Check website/app errors, checkout failures, and UX regressions",
            "priority": "HIGH",
            "expected_impact": "Prevent technical revenue leakage"
        })

    # -----------------------------
    # Revenue Spike Scenarios
    # -----------------------------
    if z_score > 2:
        actions.append({
            "team": "Operations",
            "action": "Ensure inventory and fulfillment capacity can handle demand",
            "priority": "MEDIUM",
            "expected_impact": "Avoid stockouts and delivery delays"
        })

    # -----------------------------
    # Forecast Risk
    # -----------------------------
    if forecast_risk:
        actions.append({
            "team": "Finance",
            "action": "Re-evaluate short-term revenue projections and cash planning",
            "priority": "HIGH",
            "expected_impact": "Reduce financial planning risk"
        })

    # -----------------------------
    # Default Safety Net
    # -----------------------------
    if not actions:
        actions.append({
            "team": "Analytics",
            "action": "Continue monitoring KPIs for stability",
            "priority": "LOW",
            "expected_impact": "Ensure sustained performance"
        })

    return actions
