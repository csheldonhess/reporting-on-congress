# Reporting on Congress

What has Congress passed and not passed, lately? 

This page lives at [https://csheldonhess.github.io/reporting-on-congress/](https://csheldonhess.github.io/reporting-on-congress/). If you want to see the code, you're in the right place.
* Markdown files corresponding to each page on the site are in the `docs` folder
* The code that generates those pages is in `report.py`
* `_config.yml` is just a little bit of configuration for GitHub's Jekyll renderer.

To download and run this code yourself, you're going to want to register for an API key from [ProPublica](https://projects.propublica.org/api-docs/congress-api/) and put it in a file called `propublica-key.txt`, in the same directory as the code. You'll also need an API key from [News API](https://newsapi.org/docs/get-started), which you'll put in `news-key.txt`. You'll need to make sure you have [requests](http://docs.python-requests.org/en/master/) installed, as well. And, finally, unless you're on a Mac running under the username "coral," you'll need to change all of my file paths. They are fully specified for my machine because of the way I'm keeping this page up to date, which brings us to the next point:

`github.py` is there to update the markdown files in github automatically, via a cron job on my laptop. This is not the best possible way to deploy a web service, for a lot of reasons, but it has the advantage of being 100% free of charge and not requiring me to figure out how to wake up a Heroku servo when I need it. If you decide to go this route, I can tell you from experience that 1) you'll need to fully specify all of your file paths, both in the crontab command list and in the code itself, and 2) it's not going to run when your machine is idle. Like I said, not ideal. Anyway, if you decide you want to try `github.py` out for yourself, you'll want to remove all mention of my GitHub account and replace it with your own. You'll also need to put your GitHub password into a file called `gh-pass.txt`.

`old_report.py` is deprecated and is only included in this repo because I made an example of myself in a lesson, one time, and the lesson links here. 😁 And, I mean, if you want to see how I go about ripping up a working piece of code and refactoring it into something more readable, there you go. `old_report.py` was the alpha version of this project.

All of the votes are available courtesy of [ProPublica](https://www.propublica.org/), and related news articles are thanks to [News API](https://newsapi.org/). All the code is my own, and is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike license.
 
![CC-by-nc-sa](cc-by-nc-sa.png)
