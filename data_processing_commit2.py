import csv


def load_cities(path="Cities.csv"):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["latitude"] = float(r["latitude"])
        r["longitude"] = float(r["longitude"])
        r["temperature"] = float(r["temperature"])
    return rows


def filter_items(condition, dict_list):
    """
    Return a new list containing only the dictionaries that satisfy
    the given condition function.

    Args:
        condition: A function that takes a dictionary and returns True or False.
        dict_list: A list of dictionaries.

    Returns:
        A list of dictionaries for which condition(item) is True.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]
        >>> filter_items(lambda s: s["score"] >= 85, students)
        [{'name': 'Alice', 'score': 90}, {'name': 'Charlie', 'score': 85}]

        >>> filter_items(lambda s: s["name"].startswith("A"), students)
        [{'name': 'Alice', 'score': 90}]

        >>> filter_items(lambda s: s["score"] > 100, students)
        []
    """
    return [item for item in dict_list if condition(item)]


def aggregate(aggregation_key, aggregation_function, dict_list):
    """
    Aggregate values associated with aggregation_key using the
    provided aggregation function.

    Args:
        aggregation_key: The dictionary key whose values should be aggregated.
        aggregation_function: A function such as sum, max, min, etc.
        dict_list: A list of dictionaries.

    Returns:
        The aggregated result.

    Examples:
        >>> students = [
        ...     {"name": "Alice", "score": 90},
        ...     {"name": "Bob", "score": 70},
        ...     {"name": "Charlie", "score": 85}
        ... ]

        >>> aggregate("score", sum, students)
        245

        >>> aggregate("score", max, students)
        90

        >>> aggregate("score", min, students)
        70

        >>> aggregate(
        ...     "score",
        ...     lambda scores: sum(scores) / len(scores),
        ...     students
        ... )
        81.66666666666667
    """
    return aggregation_function([item[aggregation_key] for item in dict_list])


if __name__ == "__main__":
    cities = load_cities()
    mean = lambda values: sum(values) / len(values)
    in_country = lambda name: (lambda c: c["country"] == name)

    # Print the average temperature of all the cities
    print("Average temperature:", aggregate("temperature", mean, cities))

    # Print all cities in Germany
    for c in filter_items(in_country("Germany"), cities):
        print(c["city"])

    # Print all cities in Spain with a temperature above 12°C
    spain_warm = filter_items(
        lambda c: c["country"] == "Spain" and c["temperature"] > 12, cities
    )
    for c in spain_warm:
        print(c["city"], c["temperature"])

    # Count the number of unique countries
    print("Unique countries:", aggregate("country", lambda xs: len(set(xs)), cities))

    # Print the average temperature for all the cities in Germany
    germany = filter_items(in_country("Germany"), cities)
    print("Germany average:", aggregate("temperature", mean, germany))

    # Print the max temperature for all the cities in Italy
    italy = filter_items(in_country("Italy"), cities)
    print("Italy max:", aggregate("temperature", max, italy))
