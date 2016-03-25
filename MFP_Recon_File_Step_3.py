import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')


	
