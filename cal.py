import calendar, datetime
from django.utils import timezone


class Calendar(calendar.Calendar):
    def __init__(self, year, month):
        super().__init__(firstweekday=6)
        self.year = year
        self.month = month
        self.day_names = ("Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat")
        self.months = (
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        )

    def get_days(self):
        now = timezone.now()
        weeks = self.monthdays2calendar(self.year, self.month)
        new_weeks = []
        for week in weeks:
            new_week = []
            for day_tuple in week:
                day, _ = day_tuple
                if day < now.day:
                    if now.year < self.year or now.month < self.month:
                        new_week.append(day_tuple + (True,))
                    else:
                        new_week.append(day_tuple + (False,))
                else:
                    new_week.append(day_tuple + (True,))

            new_weeks.append(new_week)
        print(new_weeks)
        return new_weeks
        # days = []
        # for week in weeks:
        #     for day, _ in week:
        #         days.append(day)
        # return days

    def get_month(self):
        return self.months[self.month - 1]
