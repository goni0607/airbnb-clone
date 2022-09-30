import calendar, datetime
from django.utils import timezone
from django.db.models.query import Q


class ReserveDate:
    def __init__(self, date, is_past, is_booked):
        self.date = date
        self.is_past = is_past
        self.is_booked = is_booked


class Calendar(calendar.Calendar):
    def __init__(self, room, year, month):
        super().__init__(firstweekday=6)
        self.room = room
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
        self.reservations = list(
            self.room.reservations.filter(
                Q(check_in__year=self.year, check_in__month=self.month)
                | Q(check_out__year=self.year, check_out__month=self.month)
            )
        )

    def is_booked(self, date):
        for r in self.reservations:
            if date >= r.check_in and date < r.check_out:
                return True
        return False

    def get_days(self):

        now = timezone.now().date()
        weeks = self.monthdays2calendar(self.year, self.month)
        new_weeks = []
        for week in weeks:
            new_week = []
            for day_tuple in week:
                cal_day, _ = day_tuple
                if cal_day > 0:
                    cal_date = datetime.date(self.year, self.month, cal_day)
                    is_past = cal_date <= now
                    is_booked = self.is_booked(cal_date)
                    new_week.append(ReserveDate(cal_date, is_past, is_booked))
                else:
                    new_week.append(None)
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


# result = filter(
#     lambda reserv: test_date >= reserv.check_in
#     and test_date <= reserv.check_out,
#     self.reservations,
# )
