import github3
from datetime import datetime

def writeUpdates(filename):
	f = open('/Users/coral/code/reporting-on-congress/gh-pass.txt', 'r')
	password = f.readline()

	# make a github object by logging in
	github = github3.login(username='csheldonhess', password=password)
	# now get the repo we want
	repo = github.repository('csheldonhess', 'reporting-on-congress')
	# craft a helpful commit message that I'll know was machine-generated
	time = str(datetime.now())
	commit_message = 'Made a change on {0}'.format(time)
	# update the files one by one
	f2 = open('/Users/coral/code/reporting-on-congress/docs/%s'%filename)
	words = f2.read()
	update_file = repo.file_contents('docs/%s'%filename)
	update_file.update('blanking', 'Now this is empty.'.encode('utf-8'))
	update_file.update(commit_message, words.encode('utf-8'))
	
writeUpdates('reverse_chronological.md')
writeUpdates('passed.md')
writeUpdates('failed.md')
writeUpdates('house.md')
writeUpdates('senate.md')
