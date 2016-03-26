import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

# #### Testing 
# input_recon_file = 'Recon File 2_'+lm+'.csv'
# input_cc_trans_report = 'credit_card_transaction_3_3_2016_to_3_3_2016_11_00_pm.csv_Cleaned.csv'

# output_mfp_opportunities = 'MFP_Opportunities_' + lm + '.csv'
# output_master_recon = 'MFP_Master_Recon_' + lm + '.csv'
# output_closed_lost_batch = 'Closed_Lost_Batch_Upload_' + lm + '.csv' 
# #### Testing

input_recon_file = 'Recon File 2_'+lm+'.csv'
input_cc_trans_report = raw_input("What is the name of the cleaned CC transaction report? (Don't include '.csv')")+'.csv'

output_mfp_opportunities = 'MFP_Opportunities_' + lm + '.csv'
output_master_recon = 'MFP_Master_Recon_' + lm + '.csv'
output_closed_lost_batch = 'Closed_Lost_Batch_Upload_' + lm + '.csv' 

# Creates upload to move to closed lost
with open(input_recon_file,'rU') as inFile1, open(input_cc_trans_report,'rU') as inFile2, open(output_mfp_opportunities,'w') as outFile1:
	recon_file = csv.reader(inFile1)	
	cc_trans = csv.DictReader(inFile2)
	w_mfp_opportunities = csv.writer(outFile1)

	header_row = inFile1.readline().replace('"','').replace('\n','').split(',')

	# Pre-sets useful variables
	opportunity_id_index = header_row.index('Opportunity ID')
	yelp_biz_id_index = header_row.index('Yelp Business ID')
	payment_id_index = header_row.index('Payment ID')
	cleared_status_index = header_row.index('Cleared Status')
	charge_amount_index = header_row.index('Charge Amount')
	
	# Creating dictionary for CC transactions report	
	cc_trans_list = {row['advertiser_id'] : row for row in cc_trans}

	# Write header row of MFP Opportunities
	w_mfp_opportunities.writerow(header_row)

	# Updates clear status of all opportunities based on new CC transaction report
	mfp_opportunities = []
	for row in recon_file:
		payment_id = row[payment_id_index]
		if row[cleared_status_index] == 'Cleared':
			mfp_opportunities.append(row)
		else:
			if payment_id in cc_trans_list:
				row[cleared_status_index] = cc_trans_list[payment_id]['status']
				row[charge_amount_index] = cc_trans_list[payment_id]['amount']
				mfp_opportunities.append(row)
			else:
				mfp_opportunities.append(row)

	# Sort MFP Opportunities report and writes file
	mfp_opportunities_sorted = sorted(mfp_opportunities, key=lambda row: row[cleared_status_index], reverse = True)
	for row in mfp_opportunities_sorted:
		w_mfp_opportunities.writerow(row)


# Write Master Recon List. Sets Biz ID = Payment ID
with open(input_recon_file,'rU') as inFile1, open(output_master_recon,'w') as outFile1:
	recon_file = csv.reader(inFile1)
	w = csv.writer(outFile1)

	# Writes header of Master Recon File
	w.writerow(['Yelp Business ID','Payment ID'])
	for row in recon_file:
		w.writerow([row[yelp_biz_id_index],row[payment_id_index]])

# Write CL Batch Upload
with open(output_mfp_opportunities, 'rU') as inFile1, open(output_closed_lost_batch,'w') as outFile1:
	mfp_opportunities = csv.reader(inFile1)
	w_closed_lost_batch = csv.writer(outFile1)

	# Write header of Closed Lost Batch Upload
	closed_lost_batch_header = ['Opportunity ID', 'Ops Error Notes','Missed First Payment','Stage','Reason Closed Lost - Local']
	w_closed_lost_batch.writerow(closed_lost_batch_header)

	closed_lost_counter = 0
	closed_lost_revenue = 0
	for row in mfp_opportunities:
		if row[cleared_status_index] == 'Declined':
			new_row = []
			mfp_balance = "Missed First Payment Outstanding Balance: $%.2f" % float(row[charge_amount_index])
			new_row.extend([row[opportunity_id_index],mfp_balance,'TRUE','Closed Lost','Missed First Payment'])
			w_closed_lost_batch.writerow(new_row)
			closed_lost_counter += 1
			closed_lost_revenue += float(row[charge_amount_index])

# Prints Stats and Status
print "\nTotal Opportunities Moving to Closed Lost %i" % closed_lost_counter
print "Total Revenue Moving to Closed Lost $%.2f" % closed_lost_revenue
print "Done!"
