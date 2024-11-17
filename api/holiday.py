import json
import re
from datetime import datetime

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


def get_holidays(year):
    res = requests.get(f'https://raw.githubusercontent.com/NateScarlet/holiday-cn/master/{year}.json', timeout=5)
    try:
        holidays = json.loads(res.text)
    except json.JSONDecodeError:
        return {
            'year': year,
            'holidays': []
        }
    return {
        'year': holidays['year'],
        'holidays': holidays['days']
    }


def is_weekend(date):
    weekDays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return [date.weekday() >= 5, weekDays[date.weekday()]]


def is_holiday(date):
    holidays = get_holidays(date.year)
    if not holidays['holidays']:
        return None
    for holiday in holidays['holidays']:
        if holiday['date'] == date.strftime('%Y-%m-%d'):
            return holiday
    return None


def is_date(date_str):
    current_date = datetime.today()
    if date_str is None:
        return current_date
    else:
        if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                return current_date
        elif re.match(r'^\d{2}-\d{2}$', date_str):
            try:
                date = datetime.strptime(f"{current_date.year}-{date_str}", '%Y-%m-%d')
            except ValueError:
                return current_date
        else:
            return current_date
        return date


@app.route("/", methods=['get'])
def today():
    datetime_date = is_date(request.args.get('date'))
    string_date = datetime_date.strftime('%Y-%m-%d')
    date_name = is_weekend(datetime_date)
    holiday = is_holiday(datetime_date)
    if holiday is None:
        isOffDay = date_name[0]
        holiday = None
    else:
        isOffDay = holiday['isOffDay']
        holiday_name = holiday['name']
        message = '假期愉快'
        if not isOffDay:
            holiday_name = holiday['name'] + '调休'
            message = '调休愉快！'
        holiday = {
            'isLieu': not isOffDay,
            'holiday': holiday_name,
            'message': message
        }
    return jsonify(
        {
            'date': string_date,
            'weekDay': datetime_date.weekday() + 1,
            'name': date_name[1],
            'isOffDay': isOffDay,
            'holiday': holiday
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
    app.json.ensure_ascii = False
