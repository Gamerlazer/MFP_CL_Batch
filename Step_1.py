import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

# #### Testing 
# input_sfdc = 'SFDC_Report.csv'
# input_atr_report = 'account_transaction_2_1_2016_to_2_29_2016.csv'
# input_cc_trans = 'Cleaned_CC_Transaction_Report_2016-02.csv'
# ####

input_sfdc = raw_input("What is the name of the SFDC report? (Don't include '.csv')")+'.csv'
input_atr_report = raw_input("What is the name of the ATR report? (Don't include '.csv')")+'.csv'
input_cc_trans = raw_input("What is the name of the cleaned CC transaction report? (Don't include '.csv')")+'.csv'

output_sfdc = 'Recon File 1_'+lm+'.csv'

with open(input_sfdc, 'rU') as r1, open(input_atr_report,'rU') as r2, open(input_cc_trans,'rU') as r3, open(output_sfdc, 'w') as outFile1:
	sfdc_raw = csv.reader(r1)
	atr_r = csv.DictReader(r2)
	cc_trans = csv.DictReader(r3)
	w = csv.writer(outFile1)

# Creates dictionaries for ATR: Biz ID to Payment ID map, and CC Transaction report of Payment ID to all attributes
	atr_list = {row['business_id'] : row['payment_account_id'] for row in atr_r}
	cc_trans_list = {row['advertiser_id'] : row for row in cc_trans}
	
# Creating a list from the header row	
	h = r1.readline().replace('"','').replace('\n','').split(',')

# Replace the first 'Yelp Business ID' column with 'Opportunity Biz ID'
	opportunity_biz_id_index = h.index('Yelp Business ID')
	h[opportunity_biz_id_index] = 'Opportunity Biz ID'
	yelp_biz_id_index = h.index('Yelp Business ID')

# Add 'Payment ID','Cleared Status','Charge Amount' to the header
	h.extend(['Payment ID','Cleared Status','Charge Amount'])
	payment_id_index = yelp_biz_id_index + 1
	cleared_status_index = yelp_biz_id_index + 2
	w.writerow(h) # write new header

# Creates a list of all cleaned rows
	cleaned_sfdc = []
	for row in sfdc_raw: 
		if len(row) > 4:
			if row[yelp_biz_id_index] == "":
				row[yelp_biz_id_index] = row[opportunity_biz_id_index]
			cleaned_sfdc.append(row)

# Creates a list of all opportunities with Payment ID, Cleared Status and Charge Amount, if available
	ones_that_got_away_count = 0
	recon_list = []

	for row in cleaned_sfdc:
		business_id = row[yelp_biz_id_index] 
		if business_id in atr_list:
			payment_id = atr_list[business_id]
			cleared_status = "___NO PAYMENT"
			charge_amount = None
			ones_that_got_away_count += 1
		 	if payment_id in cc_trans_list:
				cleared_status = cc_trans_list[payment_id]['status']
				charge_amount = cc_trans_list[payment_id]['amount']
				ones_that_got_away_count -= 1
			row.extend([payment_id, cleared_status, charge_amount])
		else:
			row.append("___MISSING IN ATR")
		recon_list.append(row)

# Sort rows by Missing in ATR, Payment Status
	missing_in_atr = [row for row in recon_list if len(row) == 19]
	recon_list_1 = [row for row in recon_list if len(row) > 19]
	recon_list_2 = sorted(recon_list_1, key=lambda row : row[cleared_status_index], reverse = True)

	recon_list_sorted = missing_in_atr + recon_list_2

# Write rows to csv file
	for row in recon_list_sorted:
		w.writerow(row)

# Prints Stats and Status
print "\nOpportunities Count: %i" % len(recon_list)
print "Missing in ATR: %i" % len(missing_in_atr)
print "Ones that got away: %i" % ones_that_got_away_count
print "Done!"

