# alerts/rules.py

def zscore_alert(zscore_value: float, threshold: float):
    """
    Simple z-score based alert rule.

    Returns:
        (bool, str) -> (alert_triggered, message)
    """
    if zscore_value is None:
        return False, ""

    if zscore_value > threshold:
        return True, f"Z-Score {zscore_value:.2f} above +{threshold}"
    elif zscore_value < -threshold:
        return True, f"Z-Score {zscore_value:.2f} below -{threshold}"

    return False, ""
