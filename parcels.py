"""Parcel data model and CSV helpers.

Each parcel has:
    parcel_id   - unique label, e.g. "P01"
    weight      - integer kg  (knapsack COST)
    priority    - 1..10       (knapsack VALUE, before urgency bonus)
    deadline    - hours left  (SORTING KEY: smaller = more urgent)
    destination - graph node the parcel must be delivered to
"""
import csv
from dataclasses import dataclass

URGENT_HOURS = 8      # parcels due within this many hours are "urgent"
URGENT_BONUS = 3      # extra value given to urgent parcels in the knapsack


@dataclass
class Parcel:
    parcel_id: str
    weight: int
    priority: int
    deadline: int
    destination: str


def parcel_value(p):
    """Knapsack value of a parcel: its priority plus a bonus if it is urgent.

    This is how the sorting/urgency idea influences the packing step.
    """
    return p.priority + (URGENT_BONUS if p.deadline <= URGENT_HOURS else 0)


def load_parcels(path):
    parcels = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            parcels.append(Parcel(row["parcel_id"], int(row["weight"]),
                                  int(row["priority"]), int(row["deadline"]),
                                  row["destination"]))
    return parcels


def save_parcels(parcels, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["parcel_id", "weight", "priority", "deadline", "destination"])
        for p in parcels:
            w.writerow([p.parcel_id, p.weight, p.priority, p.deadline, p.destination])
