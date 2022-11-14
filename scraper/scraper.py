import requests
from bs4 import BeautifulSoup
import pandas as pd


#We will send a user-agent on every HTTP request 
#Because if you make GET request using requests then by default the user-agent is Python which might get blocked.
baseurl = "https://www.thewhiskyexchange.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}



