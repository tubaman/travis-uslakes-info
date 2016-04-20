"""Get the current lake level for Lake Travis"""

import re

import scraperwiki
from bs4 import BeautifulSoup
from dateutil.parser import parse as date_parse

html = scraperwiki.scrape("http://travis.uslakes.info/Level.asp")

soup = BeautifulSoup(html)
level_label = soup.find(text="WATER LEVEL")
td = level_label.parent.parent.parent
level = float(td.find(text=re.compile("\d\d\d\.\d\d")))
unit = "Feet MSL"
date = td.findAll('font')[0].text
time = td.findAll('font')[1].text.strip()
timestamp = date_parse(u"%s %s" % (date, time))

full_text_re = re.compile("full pool of (.*)")
full_text = td.find(text=full_text_re)
full_level = float(full_text_re.search(full_text).group(1))

scraperwiki.sqlite.save(
    unique_keys=['timestamp'],
    data={"timestamp": timestamp, "level": level, "unit": unit}
)
