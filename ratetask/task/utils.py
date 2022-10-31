from datetime import timedelta,datetime


def format_date(day_from,day_to):
    date_list = []
    new_date_from = datetime.strptime(day_from, "%Y-%m-%d")
    new_date_to = datetime.strptime(day_to, "%Y-%m-%d")

    ###restructure in a new function
    if new_date_to < new_date_from:
        return None

    for n in range(int((new_date_to - new_date_from).days) + 1):
        dt = (new_date_from + timedelta(n))
        dates = dt.strftime("%Y-%m-%d")
        date_list.append(dates)
    return date_list