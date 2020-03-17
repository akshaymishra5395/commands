import datetime

def get_last_update_date(filepath):
    """This function uses a last_ran_dates.txt file to get previouly saved dates ,
    which are dates on which management ran succesfully"""
    import re
    pattern = re.compile(r'last_ran_weekly:"([0-9\/]+)"\nlast_ran_monthly:"([0-9\/]+)"')
    with open(filepath, 'r') as f:
        data = f.read()
    try:
        result = re.match(pattern, data)
        date = datetime.datetime.strptime(result.group(1) , '%d/%m/%Y')
        return date
    except :
        return None

def read_execution_date(filepath):
    with open(filepath) as f:
        exe_date_dict = json.load(f)
        return datetime.strptime(exe_date_dict["last_execution_date"], DATE_FORMAT)

def write_execution_date(filepath, date):
    with open(filepath, "w") as f:
        json.dump({"last_execution_date": date}, f)

def get_week_start_date(dt):
    days = dt.weekday()+1
    wst = dt - datetime.timedelta(days=days)
    print(wst)
    return wst

def write_last_update_date(filepath):
    """This function uses a last_ran_dates.txt file to get previouly saved dates ,
    which are dates on which management ran succesfully"""
    import re
    pattern = re.compile(r'last_ran_weekly:"([0-9\/]+)",last_ran_monthly:"([0-9\/]+)"')
    with open(filepath, 'r') as f:
        data = f.read()
    try:
        result = re.match(pattern, data)
        return datetime.datetime(result.group(1))
    except :
        return None



