from datetime import datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))


def ist_today_start_epoch() -> float:
    """Epoch timestamp (UTC) for today's midnight in IST."""
    now_ist = datetime.now(IST)
    start_ist = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
    return start_ist.timestamp()


def ist_week_start_epoch() -> float:
    """Epoch timestamp (UTC) for this week's Monday midnight in IST."""
    now_ist = datetime.now(IST)
    start_of_day = now_ist.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = start_of_day - timedelta(days=start_of_day.weekday())  # Monday == 0
    return monday.timestamp()


def since_epoch_for_period(period: str):
    """Returns the epoch cutoff for a leaderboard period, or None for 'overall'."""
    if period == "daily":
        return ist_today_start_epoch()
    if period == "weekly":
        return ist_week_start_epoch()
    return None