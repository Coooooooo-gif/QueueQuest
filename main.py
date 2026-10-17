"""
QueueQuest: Theme Park Strategy Analyser.

Run:
    python main.py

Uses Python standard libraries only.

Advanced topics:
    Recursion, File I/O and Testing.

Assumptions:
    Fixed waiting times, one visit per attraction, additive preferences.
    Walking time, breaks and opening hours are excluded.
"""

import json
from pathlib import Path

BASE_FOLDER = Path(__file__).resolve().parent
SESSION_FILE = BASE_FOLDER / "session.json"
REPORT_FILE = BASE_FOLDER / "analysis_report.txt"

available_time = 0

attractions = []


def get_integer(prompt, minimum, maximum=None):
    while True:
        try:
            value = int(input(prompt))

            if value < minimum:
                print(f"Please enter a number of at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Please enter a number no greater than {maximum}.")
                continue

            return value

        except ValueError:
            print("Please enter a whole number.")


def add_attraction():
    if len(attractions) >= 16:
        print("You can add up to 16 attractions.")
        return

    while True:
        name = input("Enter the attraction name: ").strip()

        if not name:
            print("The name cannot be empty.")
            continue

        if any(
            attraction["name"].strip().casefold() == name.casefold()
            for attraction in attractions
        ):
            print("This attraction already exists.")
            continue

        break

    waiting_time = get_integer(
        "Enter the estimated waiting time in minutes: ", 0
    )

    ride_time = get_integer(
        "Enter the ride duration in minutes: ", 1
    )

    preference = get_integer(
        "Enter your preference score (1-10): ", 1, 10
    )

    attraction = {
        "name": name,
        "waiting_time": waiting_time,
        "ride_time": ride_time,
        "preference": preference
    }

    attractions.append(attraction)
    print(f"{name} added successfully!")


def view_attractions():
    print(f"\nAvailable time: {available_time} minutes")

    if not attractions:
        print("No attractions have been added.")
        return

    for number, attraction in enumerate(attractions, start=1):
        total_time = (
            attraction["waiting_time"] + attraction["ride_time"]
        )

        print(
            f"{number}. {attraction['name']} | "
            f"Waiting: {attraction['waiting_time']} min | "
            f"Ride: {attraction['ride_time']} min | "
            f"Total: {total_time} min | "
            f"Preference: {attraction['preference']}"
        )


def total_time(plan):
    return sum(
        attraction["waiting_time"] + attraction["ride_time"]
        for attraction in plan
    )


def total_preference(plan):
    return sum(
        attraction["preference"]
        for attraction in plan
    )


def find_best_plan(items, remaining_time, index=0):
    """Find the highest-scoring feasible combination recursively.

    Compare skipping and selecting each attraction.
    For equal scores, prefer the combination taking less time.
    For equal scores and times, retain the skipped combination.
    """
    if index == len(items):
        return []

    skipped_plan = find_best_plan(
        items, remaining_time, index + 1
    )

    current = items[index]
    required_time = current["waiting_time"] + current["ride_time"]

    if required_time > remaining_time:
        return skipped_plan

    selected_plan = [current] + find_best_plan(
        items,
        remaining_time - required_time,
        index + 1
    )

    selected_score = total_preference(selected_plan)
    skipped_score = total_preference(skipped_plan)

    if selected_score > skipped_score:
        return selected_plan

    if selected_score == skipped_score:
        if total_time(selected_plan) < total_time(skipped_plan):
            return selected_plan

    return skipped_plan


def analyse_best_plan():
    if not attractions:
        print("Please add attractions first.")
        return

    best_plan = find_best_plan(attractions, available_time)

    print("\n--- Best Attraction Combination ---")

    if not best_plan:
        print("No attractions fit within your available time.")
        return

    for number, attraction in enumerate(best_plan, start=1):
        required_time = (
            attraction["waiting_time"] + attraction["ride_time"]
        )

        print(
            f"{number}. {attraction['name']} | "
            f"Time: {required_time} min | "
            f"Preference: {attraction['preference']}"
        )

    waiting = sum(
        attraction["waiting_time"] for attraction in best_plan
    )

    riding = sum(
        attraction["ride_time"] for attraction in best_plan
    )

    print(f"\nTotal preference score: {total_preference(best_plan)}")
    print(f"Total waiting time: {waiting} minutes")
    print(f"Total ride time: {riding} minutes")
    print(f"Total time used: {total_time(best_plan)} minutes")
    print(
        f"Remaining time: "
        f"{available_time - total_time(best_plan)} minutes"
    )

def greedy_plan(items, time_limit):
    selected = []
    remaining = time_limit

    for attraction in items:
        required_time = (
            attraction["waiting_time"] + attraction["ride_time"]
        )

        if required_time <= remaining:
            selected.append(attraction)
            remaining -= required_time

    return selected


def display_plan_summary(title, plan, time_limit):
    print(f"\n--- {title} ---")

    names = ", ".join(
        attraction["name"] for attraction in plan
    )

    print(f"Selected attractions: {names or 'None'}")
    print(f"Total preference score: {total_preference(plan)}")
    print(f"Total time used: {total_time(plan)} minutes")
    print(
        f"Remaining time: "
        f"{time_limit - total_time(plan)} minutes"
    )


def compare_strategies():
    if not attractions:
        print("Please add attractions first.")
        return

    preference_order = sorted(
        attractions,
        key=lambda attraction: (
            -attraction["preference"],
            attraction["waiting_time"] + attraction["ride_time"],
            attraction["name"]
        )
    )

    shortest_order = sorted(
        attractions,
        key=lambda attraction: (
            attraction["waiting_time"] + attraction["ride_time"],
            -attraction["preference"],
            attraction["name"]
        )
    )

    optimal = find_best_plan(attractions, available_time)
    preference_first = greedy_plan(preference_order, available_time)
    shortest_first = greedy_plan(shortest_order, available_time)

    display_plan_summary(
        "Optimal combination", optimal, available_time
    )

    display_plan_summary(
        "Highest preference first", preference_first, available_time
    )

    display_plan_summary(
        "Shortest total time first", shortest_first, available_time
    )


def analyse_time_change():
    if not attractions:
        print("Please add attractions first.")
        return

    alternative_time = get_integer(
        "Enter an alternative available time in minutes: ", 0
    )

    current_plan = find_best_plan(attractions, available_time)
    alternative_plan = find_best_plan(
        attractions, alternative_time
    )

    display_plan_summary(
        f"Current budget: {available_time} minutes",
        current_plan,
        available_time
    )

    display_plan_summary(
        f"Alternative budget: {alternative_time} minutes",
        alternative_plan,
        alternative_time
    )

    score_change = (
        total_preference(alternative_plan)
        - total_preference(current_plan)
    )

    print(f"\nPreference score change: {score_change:+d}")
    print("Your original available time has not changed.")


def confirm_overwrite(path):
    if not path.exists():
        return True

    answer = input(
        f"{path.name} already exists. Overwrite? (y/N): "
    ).strip().lower()

    return answer == "y"


def save_session():
    if not confirm_overwrite(SESSION_FILE):
        print("Save cancelled.")
        return

    data = {
        "available_time": available_time,
        "attractions": attractions
    }

    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        print(f"Session saved to: {SESSION_FILE}")

    except OSError as error:
        print(f"Could not save the session: {error}")


def validate_session(data):
    if not isinstance(data, dict):
        raise ValueError("Invalid session format.")

    time_limit = data.get("available_time")
    items = data.get("attractions")

    if type(time_limit) is not int or time_limit < 0:
        raise ValueError("Invalid available time.")

    if not isinstance(items, list) or len(items) > 16:
        raise ValueError("Invalid attraction list.")

    names = set()

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid attraction.")

        name = item.get("name")
        waiting = item.get("waiting_time")
        riding = item.get("ride_time")
        preference = item.get("preference")

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid attraction name.")

        clean_name = name.strip().casefold()

        if clean_name in names:
            raise ValueError("Duplicate attraction names.")

        names.add(clean_name)

        if type(waiting) is not int or waiting < 0:
            raise ValueError("Invalid waiting time.")

        if type(riding) is not int or riding <= 0:
            raise ValueError("Invalid ride duration.")

        if type(preference) is not int or not 1 <= preference <= 10:
            raise ValueError("Invalid preference score.")


def load_session():
    global available_time

    if attractions:
        answer = input(
            "Replace your current inputs? (y/N): "
        ).strip().lower()

        if answer != "y":
            print("Load cancelled.")
            return

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        validate_session(data)

        available_time = data["available_time"]
        attractions[:] = data["attractions"]

        print("Session loaded successfully!")
        view_attractions()

    except FileNotFoundError:
        print("No saved session found. Use option 7 to save one.")

    except (OSError, ValueError, RecursionError) as error:
        print(f"Could not load the session: {error}")


def export_report():
    if not attractions:
        print("Please add attractions first.")
        return

    if not confirm_overwrite(REPORT_FILE):
        print("Export cancelled.")
        return

    best_plan = find_best_plan(attractions, available_time)

    lines = [
        "QueueQuest: Theme Park Strategy Analyser",
        "=" * 45,
        f"Available time: {available_time} minutes",
        "",
        "INPUT ATTRACTIONS"
    ]

    for attraction in attractions:
        lines.append(
            f"{attraction['name']} | "
            f"Waiting: {attraction['waiting_time']} min | "
            f"Ride: {attraction['ride_time']} min | "
            f"Preference: {attraction['preference']}"
        )

    lines.extend([
        "",
        "BEST COMBINATION"
    ])

    if best_plan:
        for number, attraction in enumerate(best_plan, start=1):
            lines.append(f"{number}. {attraction['name']}")
    else:
        lines.append("No attractions fit within the time budget.")

    waiting = sum(
        attraction["waiting_time"] for attraction in best_plan
    )

    riding = sum(
        attraction["ride_time"] for attraction in best_plan
    )

    lines.extend([
        "",
        f"Total preference score: {total_preference(best_plan)}",
        f"Total waiting time: {waiting} minutes",
        f"Total ride time: {riding} minutes",
        f"Total time used: {total_time(best_plan)} minutes",
        f"Remaining time: {available_time - total_time(best_plan)} minutes",
        "",
        "ASSUMPTIONS",
        "Times are fixed user-provided estimates.",
        "Each attraction can be selected at most once.",
        "Preference scores are added together.",
        "Equal scores are resolved by choosing the shorter total time.",
        "Walking, breaks and opening times are excluded.",
        "The selected combination is not a recommended route."
    ])

    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as file:
            file.write("\n".join(lines) + "\n")

        print(f"Report exported to: {REPORT_FILE}")

    except OSError as error:
        print(f"Could not export the report: {error}")


def remove_attraction():
    if not attractions:
        print("No attractions to remove.")
        return

    view_attractions()

    number = get_integer(
        "Enter the attraction number to remove (0 to cancel): ",
        0,
        len(attractions)
    )

    if number == 0:
        print("Removal cancelled.")
        return

    attraction = attractions[number - 1]

    answer = input(
        f"Remove {attraction['name']}? (y/N): "
    ).strip().lower()

    if answer == "y":
        removed = attractions.pop(number - 1)
        print(f"{removed['name']} removed successfully.")
    else:
        print("Removal cancelled.")


if __name__ == "__main__":
    print("Welcome to QueueQuest!")
    print("Theme Park Strategy Analyser")

    available_time = get_integer(
        "Enter your available time in minutes: ", 0
    )

    print(f"You have {available_time} minutes available.")

    while True:
        print("\n--- QueueQuest Menu ---")
        print("1. Add an attraction")
        print("2. View attractions")
        print("3. Change available time")
        print("4. Find the best combination")
        print("5. Compare strategies")
        print("6. Analyse a different time budget")
        print("7. Save session")
        print("8. Load session")
        print("9. Export analysis report")
        print("10. Remove an attraction")
        print("0. Exit")

        choice = get_integer("Choose an option: ", 0, 10)

        if choice == 1:
            add_attraction()

        elif choice == 2:
            view_attractions()

        elif choice == 3:
            available_time = get_integer(
                "Enter your available time in minutes: ", 0
            )
            print(f"Available time updated to {available_time} minutes.")

        elif choice == 4:
            analyse_best_plan()

        elif choice == 5:
            compare_strategies()

        elif choice == 6:
            analyse_time_change()

        elif choice == 7:
            save_session()

        elif choice == 8:
            load_session()

        elif choice == 9:
            export_report()

        elif choice == 10:
            remove_attraction()

        elif choice == 0:
            print("Thank you for using QueueQuest!")
            break