def unix_time_to_time(seconds: int) -> str:
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours >= 12:
        am_pm = "PM"
    if hours > 12:
        hours -= 12
    else:
        am_pm = "AM"
    if hours == 0:
        hours = 12
    if seconds:
        return "{:02d}:{:02d}:{:02d} {}".format(hours, minutes, seconds, am_pm)
    if minutes:
        return "{:02d}:{:02d} {}".format(hours, minutes, am_pm)
    return "{:02d} {}".format(hours, am_pm)


def human_schedule(data: dict) -> dict:
    result = {}
    previous_day = None
    last_week_close = None

    for day, statuses in data.items():
        if not statuses:
            result[day] = 'Closed'
            continue

        if statuses[0]['type'] == 'close':
            if not previous_day:
                last_week_close = unix_time_to_time(statuses[0]['value'])
            else:
                result[previous_day] += unix_time_to_time(statuses[0]['value'])
            statuses.pop(0)
            if not statuses:
                result[day] = 'Closed'
                continue

        for status in statuses:
            if not result.get(day):
                result[day] = (unix_time_to_time(status['value']) + ' - ')
                continue
            if result[day][-1] == ' ':
                result[day] += unix_time_to_time(status['value'])
                continue

            result[day] += (', ' + unix_time_to_time(status['value']) + ' - ')

        previous_day = day

    if last_week_close:
        result['sunday'] += last_week_close

    return result
