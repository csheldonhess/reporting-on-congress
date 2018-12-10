question = "Bernard L. McNamee AND Senate"

import requests, json, datetime

def aMonthAgo():
	today = datetime.date.today()
	a_month_ago = today - datetime.timedelta(days = 28)
	return str(a_month_ago)

def articleFormatter(articles):
	bullets = ""
	for article in articles:
		title = article['title']
		url = article['url']
		author = article['author']
		source = article['source']['name']
		bullets += '* [%s](%s)'%(title, url)
		if author:
			bullets += ' by %s - %s\n'%(author, source)
		else:
			bullets += ' - %s\n'%source
	return bullets

# grab the api key, which I've got in my .gitignore file so I don't
# push it to GitHub
with open('news-key.txt', 'r') as f:
	key = f.readline()
	key = key.strip()
	try:
		url = ('https://newsapi.org/v2/everything?'
       'q=%s&'
       'from=%s&'
       'sortBy=popularity&'
       'excludeDomains=aol.com,thehill.com,seattletimes.com,stltoday.com&'
       'apiKey=%s'%(question, aMonthAgo(), key))

		response = requests.get(url)
		assert(response.status_code == 200), 'Unable to fetch data from server: %s'%str(r.status_code)
		data = response.json()

		# with open('testfile.txt', 'w') as testfile:
		# 	testfile.write(json.dumps(data, sort_keys=True, indent=4))

		articles = data['articles']

		# no more than five articles about any one thing
		if len(articles) > 5:
			articles = articles[0:5]

		print(articleFormatter(articles))
		
	except AssertionError as e: 
		print('The API is currently unavailable.')