import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

cleaned_cc_trans_report = 'Cleaned_CC_Transaction_Report_'+lm+'.csv'

## Cleans up CC Transaction report, remove delines if payment account id clears.
cc_report = {}
cc = 'credit_card_transaction_2_1_2016_to_3_3_2016_11_00_pm.csv.crdownload.csv'
with open(cc,'r') as f1, open(cleaned_cc_trans_report, 'w') as f2:
	r = csv.reader(f1)
	h = f1.readline()

	header_row = h.split(',') # Grab the headers

	f1.seek(0) # Reset to start of csv
	cc_trans = csv.DictReader(f1)
	fieldnames = header_row

	w = csv.DictWriter(f2, fieldnames=fieldnames,extrasaction='ignore')
	w.writeheader()

	for row in cc_trans:
		if row['status'] == 'Cleared':
			cc_report[row['advertiser_id']] = row
		elif row['advertiser_id'] not in cc_report:
			cc_report[row['advertiser_id']] = row
	
	for row in cc_report:
		w.writerow(cc_report[row])

print "Done!"
 