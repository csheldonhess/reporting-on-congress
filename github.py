import github3
from datetime import datetime

f = open('gh-pass.txt', 'r')
password = f.readline()

# make a github object by logging in
github = github3.login(username='csheldonhess', password=password)
# now get the repo we want
repo = github.repository('csheldonhess', 'reporting-on-congress')
# craft a helpful commit message that I'll know was machine-generated
time = str(datetime.now())
commit_message = 'Made a change on {0}'.format(time)

# update the files one by one
f2 = open('docs/failed.md')
words = f2.read()
update_file = repo.file_contents('docs/failed.md')
update_file.update(commit_message, words.encode('utf-8'))
