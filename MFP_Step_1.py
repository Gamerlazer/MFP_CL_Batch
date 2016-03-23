import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

input_sfdc = 'SFDC_Report.csv'
output_sfdc = input_sfdc.replace('.csv','') + '_modified_'+lm+'.csv'
sfdc_sql_query = 'SQL_Query_'+lm+'.csv'
cleaned_cc_trans_report = 'Cleaned_CC_Transaction_Report_'+lm+'.csv'

# Creates a Biz List for ATR Query and Modifies SFDC report so each Oppt ID has a BizID

with open(input_sfdc, 'r') as inFile, open(output_sfdc, 'w') as outFile, open(sfdc_sql_query, 'w') as sqlFile:
	r = csv.reader(inFile)
	w = csv.writer(outFile)
	sql_w = csv.writer(sqlFile)

	h = inFile.readline()
	h_m = h.replace('"','').replace('\n','').split(',')
	biz_id_2_index = h_m.index('Yelp Business ID')
	h_m[biz_id_2_index] = 'Yelp Biz ID 2'
	biz_id_index = h_m.index('Yelp Business ID')
	h_m.append('SQL Biz ID')

	next(r, None) # skip the first row from the reader, the old header
	w.writerow(h_m) # write new header
	sql_w.writerow(['SQL Biz ID'])

	for row in r: 
		if len(row) > 4:
			if row[biz_id_index] == "":
				row[biz_id_index] = row[biz_id_2_index]
			w.writerow(row)
			sql_biz_ids = ["'"+row[biz_id_index]+"',"]
			sql_w.writerow(sql_biz_ids)

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
# atr_report = 'MFP - Admin Query - 022016.csv'
# recon_sfdc = 'Recon File_'+lm+'.csv'

# with open(atr_report,'r') as inFile, open(output_sfdc,'r') as sfdc_r:
# 	pass


			
