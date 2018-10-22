import requests, datetime

# TODO: Change it back so that a week is actually a single week!

# grab the api key, which I've got in my .gitignore file so I don't
# push it to GitHub
f = open('api-key.txt', 'r')
key = f.readline()
key = key.strip()

# getting the output files ready
f2 = open('reverse_chronological_output.md', 'w')
f3 = open('pass_fail_order.md', 'w')

# using global vars to store each class of item on the pass/fail bill/nomination matrix
accepted_nominees = []
rejected_nominees = []
passed_bills = []
failed_bills = []

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
		flag = printInReverseChronOrder(data, f2)
	else:
		print(r.status_code)
		return False # gotta quit before we get in an infinite recursive loop
	if flag == True:
		printInPassFailOrder(f3)
	else:
		offset += 20
		getTheVotes(offset=offset)

def nominationPrintToFile(dictionary, filehandler):
	filehandler.write('%(result)s: [%(description)s*](%(url)s), %(date)s' %dictionary)
	#filehandler.write('%s: %s, %s'%(item['result'], item['description'], item['date']))
	filehandler.write('\n\tDemocrats: ')
	filehandler.write('Yes: %(democratic_yes)s, No: %(democratic_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['democratic_not_voting'])
	filehandler.write('\n\tRepublicans: ')
	filehandler.write('Yes: %(republican_yes)s, No: %(republican_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['republican_not_voting'])
	filehandler.write('\n\tIndependents: ')
	filehandler.write('Yes: %(independent_yes)s, No: %(independent_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['independent_not_voting'])
	filehandler.write('\n\n')

def nominationFormatter(item):
	dictionary = {
		'result': item['result'],
		'description': item['description'],
		'nominee': item['nomination']['name'],
		'number': item['nomination']['number'],
		'nomination_id': item['nomination']['nomination_id'],
		'agency': item['nomination']['agency'],
		'url': item['url'],
		'vote_uri': item['vote_uri'],
		'chamber': item['chamber'],
		'date': item['date'],
		'democratic_yes': item['democratic']['yes'],
		'democratic_no': item['democratic']['no'],
		'democratic_not_voting': item['democratic']['not_voting'],
		'republican_yes': item['republican']['yes'],
		'republican_no': item['republican']['no'],
		'republican_not_voting': item['republican']['not_voting'],
		'independent_yes': item['independent']['yes'],
		'independent_no': item['independent']['no'],
		'independent_not_voting': item['independent']['not_voting']
	}
	return dictionary

def billPrintToFile(dictionary, filehandler):
	filehandler.write('%(question)s, [%(title)s](%(url)s) (%(bill_id)s): %(result)s, %(date)s' %dictionary)
	#filehandler.write('%s, %s (%s): %s, %s'%(item['question'], item['bill']['title'], item['bill']['bill_id'], item['result'], item['date']))
	filehandler.write('\n\tDemocrats: ')
	filehandler.write('Yes: %(democratic_yes)s, No: %(democratic_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['democratic_not_voting'])
	filehandler.write('\n\tRepublicans: ')
	filehandler.write('Yes: %(republican_yes)s, No: %(republican_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['republican_not_voting'])
	filehandler.write('\n\tIndependents: ')
	filehandler.write('Yes: %(independent_yes)s, No: %(independent_no)s, ' %dictionary)
	filehandler.write('Not voting: %s' %dictionary['independent_not_voting'])
	filehandler.write('\n\n')	

def billFormatter(item):
	dictionary = {
		'question': item['question'],
		'title': item['bill']['title'],
		'bill_id': item['bill']['bill_id'],
		'result': item['result'],
		'number': item['bill']['number'],
		'url': item['url'],
		'vote_uri': item['vote_uri'],
		'api_uri': item['bill']['api_uri'],
		'sponsor_id': item['bill']['sponsor_id'],
		'chamber': item['chamber'],
		'date': item['date'],
		'democratic_yes': item['democratic']['yes'],
		'democratic_no': item['democratic']['no'],
		'democratic_not_voting': item['democratic']['not_voting'],
		'republican_yes': item['republican']['yes'],
		'republican_no': item['republican']['no'],
		'republican_not_voting': item['republican']['not_voting'],
		'independent_yes': item['independent']['yes'],
		'independent_no': item['independent']['no'],
		'independent_not_voting': item['independent']['not_voting']
	}
	return dictionary

def printInReverseChronOrder(dictionary, filehandler):
	# we need a way to know if the records we're grabbing are old enough
	# presumably, Congress could do more in a week than 20 things!
	old_enough = False 
	a_week_ago = aWeekAgo()
	for item in dictionary['results']['votes']: # a list! of dicts?! ... ok.
		if item['date'] >= a_week_ago: # if it's within the last week
			if len(item['bill']) == 0: # it's a nomination
				if "Confirmed" in item['result'] or "Agreed" in item['result']: #passed
					nom = nominationFormatter(item)
					accepted_nominees.append(nom)
					nominationPrintToFile(nom, filehandler)
				else: #failed 
					nom = nominationFormatter(item)
					nominationPrintToFile(nom, filehandler)
					rejected_nominees.append(nom)
			else: # a bill!
				if "Passed" in item['result'] or "Agreed" in item['result']:
					bill = billFormatter(item)
					billPrintToFile(bill, filehandler)
					passed_bills.append(bill)
				else:
					bill = billFormatter(item)
					billPrintToFile(bill, filehandler)
					failed_bills.append(bill)
		else: # if we have something more than a week old
			old_enough = True
	return old_enough

def printInPassFailOrder(filehandler): # using global variables, ehhhh?
		# now we will print a second output file, in order by what passed/failed
	filehandler.write('Passed Bills and Accepted Nominations:\n')
	filehandler.write('=====================================\n\n')
	for item in passed_bills:
		billPrintToFile(item, filehandler)
	for item in accepted_nominees:
		nominationPrintToFile(item, filehandler)
	filehandler.write('Failed Bills and Rejected Nominations:\n')
	filehandler.write('=====================================\n\n')
	for item in failed_bills:
		billPrintToFile(item, filehandler)
	for item in rejected_nominees:
		nominationPrintToFile(item, filehandler)

def aWeekAgo():
	today = datetime.date.today()
	a_week_ago = today - datetime.timedelta(days=30)
	return str(a_week_ago)

getTheVotes()
