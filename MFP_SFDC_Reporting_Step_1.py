import csv
import datetime
import os

today = datetime.date.today()
first = today.replace(day=1)
lastMonth = first - datetime.timedelta(days=1)
lm = lastMonth.strftime('%Y-%m')

input_sfdc = raw_input("What is the name of the SFDC report? (Don't include '.csv)")+'.csv'
output_sfdc = input_sfdc.replace('.csv','') + '_Cleaned_'+lm+'.csv'
# sfdc_sql_query = 'SQL_Query_'+lm+'.csv' # Generates list for ATR query

# Creates a Biz List for ATR Query and Modifies SFDC report so each Oppt ID has a BizID

# Remove 'open(sfdc_sql_query, 'w') as sqlFile'
with open(input_sfdc, 'rU') as inFile, open(output_sfdc, 'w') as outFile:
	r = csv.reader(inFile)
	w = csv.writer(outFile)
	# sql_w = csv.writer(sqlFile) # Generates list for ATR query
	
	h = inFile.readline()
	h_m = h.replace('"','').replace('\n','').split(',')

	biz_id_2_index = h_m.index('Yelp Business ID')
	h_m[biz_id_2_index] = 'Opportunity Biz ID'
	biz_id_index = h_m.index('Yelp Business ID')

	w.writerow(h_m) # write new header
	# sql_w.writerow(['SQL Biz ID']) # Generates list for ATR query

	for row in r: 
		if len(row) > 4:
			if row[biz_id_index] == "":
				row[biz_id_index] = row[biz_id_2_index]
			w.writerow(row)
			# sql_biz_ids = ["'"+row[biz_id_index]+"',"] # Generates list for ATR query
			# sql_w.writerow(sql_biz_ids) # Generates list for ATR query

print "Done!"

			
