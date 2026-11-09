import csv


class Table:
    """
    A list of dictionaries (rows) with filter and aggregate operations.

    >>> t = Table([{"name": "Alice", "score": 90},
    ...            {"name": "Bob", "score": 70},
    ...            {"name": "Charlie", "score": 85}])
    >>> len(t.filter(lambda s: s["score"] >= 85))
    2
    >>> t.aggregate("score", sum)
    245
    >>> t.filter(lambda s: s["score"] > 80).aggregate("score", min)
    85
    >>> len(t.filter(lambda s: s["score"] > 100))
    0
    """

    def __init__(self, rows):
        self.rows = list(rows)

    def filter(self, condition):
        return Table(r for r in self.rows if condition(r))

    def aggregate(self, key, fn):
        return fn([r[key] for r in self.rows])

    def __len__(self):
        return len(self.rows)

    def __iter__(self):
        return iter(self.rows)

    def __repr__(self):
        return f"Table({len(self.rows)} rows)"


class DataLoader:
    NUMERIC = ("latitude", "longitude", "temperature")

    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for r in rows:
            for k in self.NUMERIC:
                r[k] = float(r[k])
        return Table(rows)


if __name__ == "__main__":
    cities = DataLoader("Cities.csv").load()
    mean = lambda values: sum(values) / len(values)
    germany = cities.filter(lambda c: c["country"] == "Germany")

    # Print the average temperature of all the cities
    print("Average temperature:", cities.aggregate("temperature", mean))

    # Print all cities in Germany
    for c in germany:
        print(c["city"])

    # Print all cities in Spain with a temperature above 12°C
    for c in cities.filter(lambda c: c["country"] == "Spain" and c["temperature"] > 12):
        print(c["city"], c["temperature"])

    # Count the number of unique countries
    print("Unique countries:", cities.aggregate("country", lambda xs: len(set(xs))))

    # Print the average temperature for all the cities in Germany
    print("Germany average:", germany.aggregate("temperature", mean))

    # Print the max temperature for all the cities in Italy
    print("Italy max:", cities.filter(lambda c: c["country"] == "Italy").aggregate("temperature", max))
