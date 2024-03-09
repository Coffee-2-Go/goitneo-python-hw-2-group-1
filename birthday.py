from datetime import datetime, timedelta
from collections import defaultdict
import calendar


def get_birthdays_per_week(users):
    result = defaultdict(list)
    today = datetime.today().date()
    for user in users:
        birthday = user.get("birthday").date()
        try:  # can be ValueError here if the birthday is on February 29
            next_birthday = birthday.replace(year=today.year)
        except ValueError:
            next_birthday = datetime(today.year, 3, 1)

        if next_birthday < today and next_birthday.month == 1:
            next_birthday = next_birthday.replace(year=today.year + 1)

        if next_birthday.weekday() == 5:
            next_birthday = next_birthday + timedelta(days=2)
        if next_birthday.weekday() == 6:
            next_birthday = next_birthday + timedelta(days=1)

        delta_days = (next_birthday - today).days

        if delta_days < 7:
            day_of_the_week = next_birthday.weekday()
            user_name = user.get("name")
            result[day_of_the_week].append(user_name)

    sorted_result = dict(sorted(result.items()))

    day_today = today.weekday()

    birthdays_this_week = dict(
        filter(lambda week_day: week_day[0] >= day_today, sorted_result.items())
    )
    birthdays_next_week = dict(
        filter(lambda week_day: week_day[0] < day_today, sorted_result.items())
    )

    if birthdays_this_week:
        print("This week:")
        for day, names in birthdays_this_week.items():
            print(calendar.day_name[day], ": ", ", ".join(names), sep="")
            
    if birthdays_next_week:
        print("Next week:")
        for day, names in birthdays_next_week.items():
            print(calendar.day_name[day], ": ", ", ".join(names), sep="")


if __name__ == "__main__":
    users = [
        {"name": "Bill Gates", "birthday": datetime(1955, 10, 28)},
        {"name": "Bob Galts", "birthday": datetime(1987, 3, 5)},
        {"name": "Bom Gate", "birthday": datetime(1985, 3, 3)},
        {"name": "Tom Bombom", "birthday": datetime(1990, 3, 9)},
        {"name": "Lom Lomik", "birthday": datetime(1987, 3, 22)},
        {"name": "Tom Tomik", "birthday": datetime(1987, 3, 2)},
    ]

    get_birthdays_per_week(users)
