import requests
import re
import pandas as pd
from bs4 import BeatifulSoup

def run(url):
    html = requests.get(url)
    soup = BeatifulSoup(html.text, 'html.parser')
    yearMonth = soup.find_all('option', selected='selected')
    selectedYear = yearMonth[0].string
    selectedMonth = yearMonth[1].string
    workingDatesTag = soup.find_all('input', id="date")
    workingDates = []
    for workingDate in workingDatesTag:
        workingDates.append(workingDate.get('value'))
    workingDatesNotNone = filter(None, workingDates)
    businessDays = list(workingDatesNotNone)
    workingTimesTag = soup.find_all('input', id="workTime")
    workingTimes = []
    for workingTime in workingTimesTag:
        workingTimes.append(workingTime.get('value'))
    startedHoursTag =soup.find_all('input', id=re.compile('opngTime'))
    startedHours = []
    for startedHour in startedHoursTag:
        startedHours.append(startedHour.get('value'))
    endedHoursTag = soup.find_all('input', id=re.compile('clsngTime'))
    endedHours = []
    for endedHour in endedHoursTag:
        endedHours.append(endedHour.get('value'))
    yearMonthDays = []
    for businessDay in businessDays:
        yearMonthDays.append(selectedYear + '/' + selectedMonth + '/' + businessDay) 
    workingTimesDone = []
    for workingTime in workingTimes:
        workingTimesDone.append(workingTime.replace('ï½\x9e', ' - '))
    businessHours = []
    for businessHour in workingTimesDone:
        businessHours.append('フレックス勤務 (' + businessHour + ')')
    titles = []
    for item in businessHours:
        if item == 'フレックス勤務 (-)':
            titles.append('休み')
        else: 
            titles.append(item)
    wholeDayEvents = []
    for item in businessHours:
        wholeDayEvents.append('フレックス勤務 (-)' in item)
    df = pd.DataFrame()
    df['件名'] = titles
    df['開始日'] = yearMonthDays
    df['開始時刻'] = startedHours
    df['終了時刻'] = endedHours
    df['終日イベント'] = wholeDayEvents
    df['アラーム オン/オフ'] = [False] * len(yearMonthDays)
    df['プライベート'] = [False] * len(yearMonthDays)
    df['分類'] = ['フレックス'] * len(yearMonthDays)
    df.to_csv('converted.csv', encoding="shift_jis")