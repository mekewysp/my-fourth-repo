"""Commit 1: procedural version (explicit loops)."""
import csv


def load_cities(path="Cities.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["latitude"] = float(r["latitude"])
        r["longitude"] = float(r["longitude"])
        r["temperature"] = float(r["temperature"])
    return rows


cities = load_cities()

# Print the average temperature of all the cities
total = 0
for c in cities:
    total += c["temperature"]
print("Average temperature:", total / len(cities))

# Print all cities in Germany
for c in cities:
    if c["country"] == "Germany":
        print(c["city"])

# Print all cities in Spain with a temperature above 12°C
for c in cities:
    if c["country"] == "Spain" and c["temperature"] > 12:
        print(c["city"], c["temperature"])

# Count the number of unique countries
countries = set()
for c in cities:
    countries.add(c["country"])
print("Unique countries:", len(countries))

# Print the average temperature for all the cities in Germany
temps = [c["temperature"] for c in cities if c["country"] == "Germany"]
print("Germany average:", sum(temps) / len(temps))

# Print the max temperature for all the cities in Italy
temps = [c["temperature"] for c in cities if c["country"] == "Italy"]
print("Italy max:", max(temps))
