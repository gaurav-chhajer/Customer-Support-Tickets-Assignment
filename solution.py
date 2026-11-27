"""Clean up support tickets and work out counts and average resolution time."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_INPUT = Path(__file__).with_name("tickets.json")


def load_tickets(path=DEFAULT_INPUT):
    """Load the ticket list from a JSON file, including files saved with a BOM."""
    with open(path, encoding="utf-8-sig") as source:
        tickets = json.load(source)
    if not isinstance(tickets, list):
        raise ValueError("Input JSON must be an array of tickets.")
    return tickets


def _text(value, default="Unknown"):
    if isinstance(value, str):
        return value.strip() or default
    return default


def _cleaned(tickets):
    """Clean tickets one at a time, keeping the first copy of each ticket ID.

    Skip records without a usable string ID. Fill missing text with Unknown
    and tidy up statuses so they can be counted consistently later.
    """
    if tickets is None or isinstance(tickets, (str, bytes, dict)):
        raise TypeError("Tickets must be an iterable of ticket dictionaries.")
    seen = set()
    for ticket in tickets:
        if not isinstance(ticket, dict):
            continue
        ticket_id = _text(ticket.get("ticket_id"), "")
        if not ticket_id or ticket_id in seen:
            continue
        seen.add(ticket_id)
        record = ticket.copy()
        record["ticket_id"] = ticket_id
        for field in ("issue", "customer", "product"):
            record[field] = _text(ticket.get(field))
        record["status"] = _text(ticket.get("status"), "").lower()
        yield record


def _resolution_seconds(ticket):
    """Work out how long a resolved ticket took, or return None if unsure.

    Both dates need to use ISO 8601 format. If neither includes a timezone,
    assume they use the same clock. If only one has a timezone, skip the
    calculation rather than guess the other timezone.
    """
    if ticket.get("status") != "resolved":
        return None
    values = (ticket.get("created_at"), ticket.get("resolved_at"))
    if any(not isinstance(value, str) or not value.strip() for value in values):
        return None
    try:
        start, end = (datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
                      for value in values)
        if (start.tzinfo is None) != (end.tzinfo is None):
            return None
        if start.tzinfo is not None:
            start = start.astimezone(timezone.utc)
            end = end.astimezone(timezone.utc)
        seconds = (end - start).total_seconds()
    except (ValueError, OverflowError):
        return None
    return seconds if seconds >= 0 else None


def _statistics(tickets):
    counts = {}
    total_seconds = 0.0
    resolved_count = 0
    for ticket in tickets:
        product = ticket["product"]
        if product not in counts:
            counts[product] = {"open": 0, "resolved": 0}
        status = ticket["status"]
        if status in ("open", "resolved"):
            counts[product][status] += 1
        seconds = _resolution_seconds(ticket)
        if seconds is not None:
            total_seconds += seconds
            resolved_count += 1
    average = total_seconds / resolved_count / 3600 if resolved_count else None
    return counts, average


if __name__ == "__main__":
    try:
        counts, average = _statistics(_cleaned(load_tickets()))
    except (OSError, ValueError) as error:
        print(f"Error loading tickets: {error}", file=sys.stderr)
        sys.exit(1)
    print("Open vs resolved per product:")
    for product, count in counts.items():
        print(f"  {product}: open={count['open']}, resolved={count['resolved']}")
    result = f"{average:.2f} hours" if average is not None else "N/A (no valid resolved tickets)"
    print(f"Average resolution time: {result}")
