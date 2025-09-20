import json
import difflib


def load_locations():
    with open("../locations/locations.json") as f:
        return json.load(f)


def search_location(name, locations, limit=10):
    names = [loc["name"] for loc in locations]
    matches = difflib.get_close_matches(name.title(), names, n=limit)
    return [loc for loc in locations if loc["name"] in matches]


def add_new_search_term():
    locations = load_locations()

    query = input("Enter search term (e.g. ps3): ").strip()
    min_price = int(input("Enter min price: ").strip())
    max_price = int(input("Enter max price: ").strip())
    loc_input = input("Enter location name to search: ").strip()

    matches = search_location(loc_input, locations)
    if not matches:
        print("No matching locations found.")
        return

    print("\nSelect a location:")
    for i, loc in enumerate(matches):
        print(f"{i + 1}. {loc['name']} (ID: hidden)")

    choice = int(input("Enter your choice [1-{}]: ".format(len(matches)))) - 1
    selected = matches[choice]

    new_entry = {
        "query": query,
        "min_price": min_price,
        "max_price": max_price,
        "location_name": selected["name"],
        "location_id": selected["id"]
    }

    try:
        with open("search_terms.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(new_entry)

    with open("search_terms.json", "w") as f:
        json.dump(data, f, indent=2)

    print("\n✅ Entry added successfully!")


if __name__ == "__main__":
    add_new_search_term()
