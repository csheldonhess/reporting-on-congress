import requests, json, datetime

# go out to ProPublica and get the votes, appending them to a list that
# has been passed in (all_actions); because this may get called multiple times,
# we have an optional offset (the multiple calls are also why we're passing
# around this dictionary, all_actions)
def getTheVotes(all_actions, offset=0):
	url = 'https://api.propublica.org/congress/v1/both/votes/recent.json'
	head = {'X-API-Key': key}
	params = {'offset': offset}
	r = requests.get(url, params=params, headers=head)
	assert(r.status_code == 200), 'Unable to fetch data from server: %s'%str(r.status_code)
	data = r.json()
	a_week_ago = aWeekAgo()
	for item in data['results']['votes']: # a list! of dicts?! ... ok.
		if item['date'] >= a_week_ago: # if it's within the last week
			if len(item['bill']) == 0: # it's a nomination
				nom = nominationFormatter(item) # format it my way!
				# let's avoid duplicates
				if nom not in all_actions and 'Cloture' not in nom['result']: 
					all_actions.append(nom)
			else: # a bill!
				bill = billFormatter(item)
				if bill not in all_actions:
					all_actions.append(bill)
	return all_actions

# returns True if we need to make another call to ProPublica's API
# returns False if we have data older than a week already
# the list we pass in is formatted my way, not ProPublica's way
def goBackFurther(all_actions):
	# loop through the whole dictionary, looking for a date older than
	# a week old; if none are found, we probably need to look further back
	a_week_ago = aWeekAgo()
	for item in all_actions: 
		if item['date'] >= a_week_ago:
			return False
	return True

# we want to separate out all of the actions that have been taken
# into passed/failed, bill/nomination, and maybe other categories,
# for a nice, user-friendly display
def breakIntoSubCategories(all_actions):
	# set myself up with some nice empty lists
	accepted_nominees = []
	rejected_nominees = []
	passed_bills = []
	rejected_bills = []
	house_actions = []
	senate_actions = []
	for item in all_actions:
		if item['type'] == 'nom': # it's a nomination
			if "Confirmed" in item['result'] or "Agreed" in item['result']: #passed
				accepted_nominees.append(item)
			else: #failed nomination
				rejected_nominees.append(item)
		else: # a bill!
			if "Passed" in item['result'] or "Agreed" in item['result']:
				passed_bills.append(item)
			else:
				rejected_bills.append(item)
		if item['chamber'] == 'House':
			house_actions.append(item)
		else:
			senate_actions.append(item)
	subdivided_actions = {
		'accepted_nominees': accepted_nominees,
		'rejected_nominees': rejected_nominees,
		'passed_bills': passed_bills,
		'rejected_bills': rejected_bills,
		'house_actions': house_actions,
		'senate_actions': senate_actions
	}
	# useful to make sure my logic's good, but not something I always want
	# print('everything: ', str(len(all_actions)))
	# print('accepted noms: ', str(len(accepted_nominees)))
	# print('rejected noms: ', str(len(rejected_nominees)))
	# print('passed bills: ', str(len(passed_bills)))
	# print('rejected bills: ', str(len(rejected_bills)))
	return subdivided_actions

# this expects a single vote, formatted my way (by nominationFormatter/billFormatter)
def votePrintToFile(dictionary, filehandler):
	if dictionary['type'] == 'bill': # if it's a nomination
		filehandler.write('%(question)s, [%(title)s](%(url)s) (%(chamber)s: %(bill_id)s): %(result)s, %(date)s' %dictionary)
		#filehandler.write('%s, %s (%s): %s, %s'%(item['question'], item['bill']['title'], item['bill']['bill_id'], item['result'], item['date']))
		filehandler.write('\n* Democrats: ')
		filehandler.write('Yes: %(democratic_yes)s, No: %(democratic_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['democratic_not_voting'])
		filehandler.write('\n* Republicans: ')
		filehandler.write('Yes: %(republican_yes)s, No: %(republican_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['republican_not_voting'])
		filehandler.write('\n* Independents: ')
		filehandler.write('Yes: %(independent_yes)s, No: %(independent_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['independent_not_voting'])
		filehandler.write('\n\n')	
	else: # if it's a bill
		filehandler.write('%(result)s: [%(description)s*](%(url)s), %(chamber)s %(date)s' %dictionary)
		#filehandler.write('%s: %s, %s'%(item['result'], item['description'], item['date']))
		filehandler.write('\n* Democrats: ')
		filehandler.write('Yes: %(democratic_yes)s, No: %(democratic_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['democratic_not_voting'])
		filehandler.write('\n* Republicans: ')
		filehandler.write('Yes: %(republican_yes)s, No: %(republican_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['republican_not_voting'])
		filehandler.write('\n* Independents: ')
		filehandler.write('Yes: %(independent_yes)s, No: %(independent_no)s, ' %dictionary)
		filehandler.write('Not voting: %s' %dictionary['independent_not_voting'])
		filehandler.write('\n\n')

# there's nothing wrong with ProPublica's formatting of their data, but
# if I can make it more convenient for myself, why wouldn't I? right?
# So this puts bills into a flat, easy-to-access dictionary for me
def billFormatter(item):
	dictionary = {
		'type': 'bill',
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

# this puts nominations into a flat, easy-to-access dictionary for me
def nominationFormatter(item):
	dictionary = {
		'type': 'nom',
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

# this function expects to receive the main list of nicely-formatted actions
# and it also wants all of the filehandlers passed in nicely
def writeTheMarkdown(all_actions, all_fh, pass_fh, fail_fh, house_fh, senate_fh):
	# first we write the reverse chronological/all page
	all_fh.write('All votes held, in reverse chronological order:\n')
	all_fh.write('============================================== \n\n')
	for item in all_actions:
		votePrintToFile(item, all_fh)
		addNews(item, all_fh)

	# now we subdivide our item
	sub_actions = breakIntoSubCategories(all_actions)

	#now we write the passed bills & noms
	writeOneSection(sub_actions['passed_bills'], 'bills', 'passed', pass_fh)
	writeOneSection(sub_actions['accepted_nominees'], 'nominees', 'were accepted', pass_fh)
	writeOneSection(sub_actions['rejected_bills'], 'bills', 'failed', fail_fh)
	writeOneSection(sub_actions['rejected_nominees'], 'nominees', 'were rejected', fail_fh)
	writeOneSection(sub_actions['senate_actions'], 'Senate actions', 'occurred', senate_fh)
	writeOneSection(sub_actions['house_actions'], 'House actions', 'occurred', house_fh)

# writes a title with underline and then all of the appropriate votes 
# for a given section
def writeOneSection(category, noun, verb, filehandler):
	# this is a little bit ridiculous, but it pleases me
	# (generalizing my headers)
	my_string = 'All of the %s that %s'%(noun, verb)
	underline = ''
	for i in range(0,len(my_string)):
		underline += '='
	filehandler.write('%s:\n%s\n\n'%(my_string, underline))
	if len(category) == 0:
		filehandler.write('No %s %s this week.\n\n' %(noun, verb))
	else:
		for item in category:
			votePrintToFile(item, filehandler)
			addNews(item, filehandler)

# returns a string representing a date one week ago
def aWeekAgo():
	today = datetime.date.today()
	a_week_ago = today - datetime.timedelta(days=10)
	return str(a_week_ago)

# returns a string representing a date roughly a month ago
def aMonthAgo():
	today = datetime.date.today()
	# look, if I go back a full month, sometimes they throw an error
	# so I'm doing 28 days
	a_month_ago = today - datetime.timedelta(days = 28)
	return str(a_month_ago)

# formats articles pulled from the news api for nice display
def articleFormatter(articles):
	if len(articles) > 0:
		bullets = "\t*Related articles*:\n"
		for article in articles:
			title = article['title']
			url = article['url']
			author = article['author']
			source = article['source']['name']
			bullets += '\t* [%s](%s)'%(title, url)
			if author:
				bullets += ' by %s - %s\n'%(author, source)
			else:
				bullets += ' - %s\n'%source
		return bullets + '\n'
	else: # if we have nothing to add, let's not add it!
		return ''

# takes a single vote and looks for articles related to it
# a thesis could be written on how best to do this search
# but I'm not writing that thesis today
def addNews(item, filehandler):
	# there is room for improvement in choosing our search query
	# but this is how I'm doing it for now
	if item['type'] == 'nom':
		question = item['nominee'] + ' ' + item['chamber']
	else:
		question = item['title'] + ' ' + item['chamber']

	# grab the api key, which I've got in my .gitignore file so I don't
	# push it to GitHub
	with open('news-key.txt', 'r') as f:
		key = f.readline()
		key = key.strip()
		try:
			url = 'https://newsapi.org/v2/everything'
			params = {'q': question,
					  'from': aMonthAgo(),
					  'sortBy': 'relevancy',
					  'excludeDomains': 'aol.com,thehill.com,seattletimes.com,stltoday.com',
					  'apiKey': key
			}
			response = requests.get(url, params=params)
			assert(response.status_code == 200), 'Unable to fetch data from server: %s'%str(r.status_code)
			data = response.json()
			# what an incredibly straightforward schema they have
			articles = data['articles']

			# no more than five articles about any one thing; arbitrary but fair
			if len(articles) > 5:
				articles = articles[0:5]
			# write nicely formatted articles 
			filehandler.write(articleFormatter(articles))

		except AssertionError as e: 
			print('The News API is currently unavailable.')

# getting the output files ready
try: 
	all_file = open('docs/reverse_chronological.md', 'w')
	passed_file = open('docs/passed.md', 'w')
	failed_file = open('docs/failed.md', 'w')
	house_file = open('docs/house.md', 'w')
	senate_file = open('docs/senate.md', 'w')
	# just making nice breadcrumbs for usability of the site
	all_file.write('[Reporting on Congress](index.md) &gt; Everything\n\n')
	passed_file.write('[Reporting on Congress](index.md) &gt; Passed\n\n')
	failed_file.write('[Reporting on Congress](index.md) &gt; Failed\n\n')
	house_file.write('[Reporting on Congress](index.md) &gt; House\n\n')
	senate_file.write('[Reporting on Congress](index.md) &gt; Senate\n\n')
except OSError as e:
	print('Cannot open files. ', e)

# grab the api key, which I've got in my .gitignore file so I don't
# push it to GitHub
with open('propublica-key.txt', 'r') as f:
	key = f.readline()
	key = key.strip()
	try:
		offset = 0
		votes = []
		votes = getTheVotes(votes, offset) # initial call
		# this loop is here in case they did more than 20 things this week
		# (ProPublica's API returns 20 items per call, with an optional offset)
		while goBackFurther(votes):
			offset += 20
			votes = getTheVotes(votes, offset)
		writeTheMarkdown(votes, all_file, passed_file, failed_file, house_file, senate_file)
	except AssertionError as e: 
		print('The ProPublica API is currently unavailable.')

all_file.close()
passed_file.close()
failed_file.close()
house_file.close()
senate_file.close()
