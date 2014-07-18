"""Get the current lake level for Lake Travis"""

import re

import scraperwiki
from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parse

html = scraperwiki.scrape("http://travis.uslakes.info/Level.asp")

soup = BeautifulSoup(html)
level_label = soup.find(text="Water Level")
td = level_label.parent.parent.parent

level = float(td.find('font', attrs={'color': 'Green'}).strong.text)
unit = td.findAll('font')[2].strong.text
date = td.findAll('font')[3].text
time = td.findAll('font')[4].text.strip()
timestamp = date_parse(u"%s %s" % (date, time))

full_text_re = re.compile("below full pool of (.*)")
full_text = td.find(text=full_text_re)
full_level = float(full_text_re.match(full_text).group(1))

scraperwiki.sqlite.save(
    unique_keys=['timestamp'],
    data={"timestamp": timestamp, "level": level, "unit": unit}
)
