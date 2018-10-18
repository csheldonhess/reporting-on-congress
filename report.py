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
	url = 'https://api.propublica.org/congress/v1/both/votes/recent.json'
	payload = {'X-API-Key': key}
	r = requests.get(url, headers=payload)
	if r.status_code == 200:
		data = r.json()
		prettyPrintToFile(data, f2)
	else:
		print(r.status_code)

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


def aWeekAgo():
	today = datetime.date.today()
	a_week_ago = today - datetime.timedelta(days=14)
	return str(a_week_ago)

getTheVotes()
