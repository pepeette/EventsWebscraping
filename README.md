# EventsWebscraping

Jupyter notebook explanation on how to
webscrape websites with beautiful soup
and extract gaming event name and dates
for further use. The intent is to feed those dates 
to our system via google calendar. 
Hence, the creation of ws.py as a python program
running on flask that creates api endpoint for http://127.0.0.1:8000/process_events
after running flask run --port=8000 on terminal
