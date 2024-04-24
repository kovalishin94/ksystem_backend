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
            value = unix_time_to_time(statuses.pop(0)['value'])
            if not previous_day:
                last_week_close = value
            else:
                result[previous_day] += value
            
            if not statuses:
                result[day] = 'Closed'
                continue

        for status in statuses:
            value = unix_time_to_time(status['value'])
            if not result.get(day):
                result[day] = f'{value} - '
                continue
            if result[day][-1] == ' ':
                result[day] += value
                continue

            result[day] += f', {value} - '

        previous_day = day

    if last_week_close:
        result['sunday'] += last_week_close

    return result
