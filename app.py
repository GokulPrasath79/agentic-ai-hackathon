import json
import math
import re


def normalize_text(value):
    return str(value or "").strip()


def to_number(value):
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    return num if math.isfinite(num) else None


def format_number(num):
    if float(num).is_integer():
        return str(int(num))
    return str(float(f"{num:.10f}")).rstrip("0").rstrip(".") if "." in str(float(f"{num:.10f}")) else str(float(f"{num:.10f}"))


def sum_from_query(query):
    text = normalize_text(query)
    lower = text.lower()

    plus_match = re.search(r"(-?\d+(?:\.\d+)?)\s*\+\s*(-?\d+(?:\.\d+)?)", lower)
    if plus_match:
        a = to_number(plus_match.group(1))
        b = to_number(plus_match.group(2))
        if a is not None and b is not None:
            return a + b

    add_match = re.search(
        r"(?:add|sum(?:\s+of)?|what\s+is\s+the\s+sum\s+of|what\s+is)\s+(-?\d+(?:\.\d+)?)\s*(?:and|with)?\s*(-?\d+(?:\.\d+)?)",
        lower,
        re.IGNORECASE,
    )
    if add_match:
        a = to_number(add_match.group(1))
        b = to_number(add_match.group(2))
        if a is not None and b is not None:
            return a + b

    numbers = re.findall(r"-?\d+(?:\.\d+)?", lower)
    asks_for_sum = bool(re.search(r"\b(sum|add|plus|total)\b", lower)) or bool(
        re.search(r"\bwhat\s+is\b", lower)
    )

    if asks_for_sum and len(numbers) >= 2:
        a = to_number(numbers[0])
        b = to_number(numbers[1])
        if a is not None and b is not None:
            return a + b

    return None


def build_output(query):
    result = sum_from_query(query)
    if result is None:
        return "I could not determine the answer."
    return f"The sum is {format_number(result)}."
