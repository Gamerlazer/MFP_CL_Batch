import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

atr_report = raw_input("What is the name of the ATR report? (Don't include '.csv)")+'.csv'
sfdc = 'SFDC_Report_Cleaned_'+lm+'.csv'

recon_report = 'Recon_File 1_'+lm+'.csv'
cleaned_cc_trans_report = 'Cleaned_CC_Transaction_Report_'+lm+'.csv'

with open(atr_report,'rU') as r1, open(sfdc,'rU') as r2, open(cleaned_cc_trans_report,'r') as r3, open(recon_report,'w') as w1:
	atr_r = csv.DictReader(r1)
	sfdc_r = csv.reader(r2)
	cc_trans = csv.DictReader(r3)
	w = csv.writer(w1)

	atr_list = {row['business_id'] : row['payment_account_id'] for row in atr_r}
	cc_trans_list = {row['advertiser_id'] : row for row in cc_trans}
	

	sfdc_header = r2.readline()
	h = sfdc_header.replace('\n','').split(",")
	biz_id_i = h.index('Yelp Business ID')

	h.extend(['Payment ID','Cleared Status', 'Charge Amount'])
	w.writerow(h)

	for row in sfdc_r:
		biz_id = row[biz_id_i] 
		if biz_id in atr_list:
			payment_id = atr_list[row[biz_id_i]]
			cleared_status = None
			charge_amount = None
		 	if atr_list[row[biz_id_i]] in cc_trans_list:
				cleared_status = cc_trans_list[payment_id]['status']
				charge_amount = cc_trans_list[payment_id]['amount']
			row.extend([payment_id, cleared_status, charge_amount])
		else:
			row.append("___MISSING IN ATR")
		w.writerow(row)

print "Done!"
	


	
