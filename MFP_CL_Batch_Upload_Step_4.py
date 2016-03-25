import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

# Assuming all of the ones that got away are fixed
recon_file = raw_input("What is the name of the final recon report? (Don't include '.csv)")+'.csv'
cl_batch = 'CL_Batch_Upload_'+lm+'.csv'

# Creates upload to move to closed lost
with open(recon_file,'rU') as r, open(cl_batch,'w') as f1:
	recon_report = csv.DictReader(r)
	cl_oppts = {row['Opportunity ID'] : row for row in recon_report if row['Cleared Status'] != 'Cleared'} # creates a dictionary

	w = csv.writer(f1)
	header = ['Opportunity ID', 'Ops Error Notes','Missed First Payment','Stage','Reason Closed Lost - Local']
	w.writerow(header)

	for row in cl_oppts:
		new_row = []
		mfp_balance = "Missed First Payment Outstanding Balance: $%.2f" % float(cl_oppts[row]['Charge Amount'])
		new_row.extend([row,mfp_balance,'TRUE','Closed Lost','Missed First Payment'])
		w.writerow(new_row)
print "Done!"

