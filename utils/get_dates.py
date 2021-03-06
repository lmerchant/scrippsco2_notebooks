import re
import datetime as DT
from datetime import datetime, date


def get_todays_date():

    # Get variations of todays date

    def dt_to_dec(dt):
        """Convert a datetime to decimal year."""
        year_start = datetime(dt.year, 1, 1)
        year_end = year_start.replace(year=dt.year+1)
        return dt.year + (dt - year_start) / (year_end - year_start)

    today = date.today()
    today_with_time = datetime(
        year=today.year, month=today.month, day=today.day)

    today_decimal = dt_to_dec(today_with_time)

    todays_day = today.day
    todays_month = today.strftime("%B")
    todays_year = today.year
    todays_date_moyr = today.strftime("%B %Y")
    todays_date_modyyr = f"{todays_month} {todays_day}, {todays_year}"

    return todays_date_moyr, todays_date_modyyr, today_decimal, todays_year


def get_file_archive_date(data_file):

    # Get data file archive date

    # Sample archive line from file
    # " Baseline data in this file through 01-Jul-2021 from archive dated 02-Jul-2021 09:04:47    "

    pattern_archive = re.compile("archive")
    pattern_archive_date = re.compile(r'archive dated (\d\d-\w{3}-\d\d\d\d)')

    for line in open(data_file):
        for match in re.finditer(pattern_archive, line):
            m = pattern_archive_date.search(line)
            archive_date = m.group(1)
            archive_datetime = datetime.strptime(archive_date, '%d-%b-%Y')
            # Reformat to Month name Month day, Month year
            month = archive_datetime.strftime("%B")
            archive_date = f"{month} {archive_datetime.day}, {archive_datetime.year}"
            break

    return archive_date


def datetime_to_float(adatetime):
    """
    Convert adatetime into a float. The integer part of the
    float should represent the year.
    Order should be preserved. If adate < bdate, then datetime_to_float(adate) < datetime_to_float(bdate)
    Time distances should be preserved:
    If bdate - adate =  ddate-cdate then
    datetime_to_float(bdate) - datetime_to_float(adate) = datetime_to_float(ddate) - datetime_to_float(cdate)

    # Need: import datetime as DT

    https://stackoverflow.com/questions/19305991/convert-fractional-years-to-a-real-date-in-python
    """

    year = adatetime.year
    begin_of_year = DT.datetime(year, 1, 1)
    end_of_year = DT.datetime(year + 1, 1, 1)
    return year + ((adatetime - begin_of_year).total_seconds() / ((end_of_year - begin_of_year).total_seconds()))


def float_to_datetime(atime):
    """
    Convert atime (a float) to a datetime
    assert datetime_to_float(float_to_datetime(atime)) == atime

    # Need: import datetime as DT

    https://stackoverflow.com/questions/19305991/convert-fractional-years-to-a-real-date-in-python
    """

    year = int(atime)
    remainder = atime - year
    boy = DT.datetime(year, 1, 1)
    eoy = DT.datetime(year + 1, 1, 1)
    seconds = remainder * (eoy - boy).total_seconds()
    return boy + DT.timedelta(seconds=seconds)
