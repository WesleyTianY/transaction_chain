from chinese_calendar import is_workday, is_holiday
from dateutil.rrule import rrule, DAILY
from datetime import datetime


def generate_workdays(start_date, end_date):
    workdays = []
    for dt in rrule(DAILY, dtstart=start_date, until=end_date):
        # 检查日期是否是工作日且不是中国的节假日
        if is_workday(dt.date()) and not is_holiday(dt.date()):
            workdays.append(dt.date())
    return workdays
