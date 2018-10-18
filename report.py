import requests, json, datetime

# TODO: Change it back so that a week is actually a single week!

# grab the api key, which I put one directory up so I wouldn't accidentally
# push it to GitHub
# TODO: figure out what the best practice for this is
f = open('../congress-api-key.txt', 'r')
key = f.readline()
key = key.strip()

f2 = open('output.txt', 'w')

# just checking that they key got pulled correctly
# print('__%s__'%key)

def getTheVotes(offset=0):
	flag = False # checking to see if we need to go back further
	url = 'https://api.propublica.org/congress/v1/both/votes/recent.json'
	head = {'X-API-Key': key}
	params = {'offset': offset}
	r = requests.get(url, params=params, headers=head)
	if r.status_code == 200:
		data = r.json()
		flag = prettyPrintToFile(data, f2)
	else:
		print(r.status_code)
		return False # gotta quit before we get in an infinite recursive loop
	if flag == False:
		offset += 20
		getTheVotes(offset=offset)

def nominationPrintToFile(item, filehandler):
	filehandler.write('%s: %s, %s'%(item['result'], item['description'], item['date']))
	filehandler.write('\n\tDemocrats: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['democratic']['yes'], item['democratic']['no']))
	filehandler.write('Not voting: %s' %item['democratic']['not_voting'])
	filehandler.write('\n\tRepublicans: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['republican']['yes'], item['republican']['no']))
	filehandler.write('Not voting: %s' %item['republican']['not_voting'])
	filehandler.write('\n\tIndependents: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['independent']['yes'], item['independent']['no']))
	filehandler.write('Not voting: %s' %item['independent']['not_voting'])
	filehandler.write('\n\n')

def billPrintToFile(item, filehandler):
	filehandler.write('%s, %s (%s): %s, %s'%(item['question'], item['bill']['title'], item['bill']['bill_id'], item['result'], item['date']))
	filehandler.write('\n\tDemocrats: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['democratic']['yes'], item['democratic']['no']))
	filehandler.write('Not voting: %s' %item['democratic']['not_voting'])
	filehandler.write('\n\tRepublicans: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['republican']['yes'], item['republican']['no']))
	filehandler.write('Not voting: %s' %item['republican']['not_voting'])
	filehandler.write('\n\tIndependents: ')
	filehandler.write('Yes: %s, No: %s, ' %(item['independent']['yes'], item['independent']['no']))
	filehandler.write('Not voting: %s' %item['independent']['not_voting'])
	filehandler.write('\n\n')	

def prettyPrintToFile(dictionary, filehandler):
	# we need a way to know if the records we're grabbing are old enough
	# presumably, Congress could do more in a week than 20 things!
	old_enough = False 
	a_week_ago = aWeekAgo()
	for item in dictionary['results']['votes']: # a list! of dicts?! ... ok.
		if item['date'] >= a_week_ago: # if it's within the last week
			if len(item['bill']) == 0: # it's a nomination
				if "Confirmed" in item['result'] or "Agreed" in item['result']: #passed
					nominationPrintToFile(item, filehandler)
				else: #failed 
					nominationPrintToFile(item, filehandler)
			else: # a bill!
				if "Passed" in item['result'] or "Agreed" in item['result']:
					billPrintToFile(item, filehandler)
				else:
					billPrintToFile(item, filehandler)
		else: # if we have something more than a week old
			old_enough = True
	return old_enough


def aWeekAgo():
	today = datetime.date.today()
	a_week_ago = today - datetime.timedelta(days=30)
	return str(a_week_ago)

getTheVotes()
