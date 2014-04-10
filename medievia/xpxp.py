import datetime


def parse(moon=None, eclipse=None, full_text=None):
    moon_time = None
    eclipse_time = None

    if moon and eclipse:
        moon_time = _parse_moon(moon)
        eclipse_time = _parse_eclipse(eclipse)
    else:
        for line in full_text.split('\n'):
            if "next new moon:" in line.lower():
                moon_time = _parse_moon(line)
                continue

            if "eclipse start:" in line.lower():
                eclipse_time = _parse_eclipse(line)
                break

    if moon_time and eclipse_time:
        now = datetime.datetime.now()
        return "{0} {1} {2}".format((eclipse_time - now).days + 2, (moon_time - now).days + 2, "2")
    else:
        return None


def _parse_moon(input_string):
    input_string = input_string.lower()
    # Next New Moon:   Tue Apr 15 20:10:46 2014
    if "next new moon:" in input_string:
        input_string = input_string.split("next new moon:")[1]

    input_string = input_string.strip()
    return datetime.datetime.strptime(input_string, "%a %b %d %H:%M:%S %Y")


def _parse_eclipse(input_string):
    input_string = input_string.lower()
    # Eclipse Start:   Wed Apr 16 14:55:46 2014
    if "eclipse start:" in input_string:
        input_string = input_string.split("eclipse start:")[1]

    input_string = input_string.strip()
    return datetime.datetime.strptime(input_string, "%a %b %d %H:%M:%S %Y")