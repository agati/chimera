#!/usr/bin/env python

import json
import re
import requests

from bs4 import BeautifulSoup


# http://telops.lcogt.net/dajaxice/netnode.refresh/

def clear_data(name, data):
    # print "*****************************************************"

    a = re.sub('<td><b>', '', str(data))
    b = re.sub('</b></td>', '', a)

    if name == 'insolation':
        c = re.sub('<span style="color:red;', '', b)
        f = re.sub('</span>', '', c)
        f = re.sub('">', '', f)
        b = f



    elif name == 'moon':
        d = re.sub('<span>', '', b)
        e = re.sub('</span></td>', '', d)
        g = re.sub('class=', '', e)
        h = re.sub('<td "moon', '', g)
        i = re.sub('">', '', h)
        b = i

    elif name == 'last_time':
        c = re.sub('As of <b>', '', b)
        d = re.sub('</b>', '', c)
        b = d




    # print "*****************************************************"
    return b


class LCOGTScrapper(object):

    def scrape(self):
        self.client = requests.session()

        self.a = self.client.get('http://telops.lcogt.net/#')

        latest_comet_queue_id = int(re.findall('Telops.latest_comet_queue_id = (.+);', self.a.text)[0])

        self.r = self.client.post(
            url='http://telops.lcogt.net/dajaxice/netnode.refresh/',
            data={'argv': json.dumps({"latest": latest_comet_queue_id})},
            headers={
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                "Content-Type": "application/x-www-form-urlencoded",
                'Host': 'telops.lcogt.net',
                "Origin": "http://telops.lcogt.net",
                "Referer": "http://telops.lcogt.net/",
                'X-CSRFToken': None,
                'X-Requested-With': 'XMLHttpRequest',

            },
            cookies={'pushstate': 'pushed'}

        )

        return json.loads(self.r.text)


c = LCOGTScrapper()
data = c.scrape()

# print 'data is:',data, type(data)
# print "*********************************************************"

temperature = []
dew_point = []
pressure = []
humidity = []
wind = []
insolation = []
brightness = []
transparency = []
ok_to_open = []
interlock_reason = []
moon = []
last_time =''

for val in data:
    if 'id' in val.keys():
        #print 'id', val['id']



        if val['id'] == '#site-lsc-ssb-system-Weather-tip':
            line = val['val']
            # print "line is",line
            html = BeautifulSoup(line, 'lxml')
            temperature.append(html.find_all('td')[1])
            dew_point.append(html.find_all('td')[3])
            pressure.append(html.find_all('td')[5])
            humidity.append(html.find_all('td')[7])
            wind.append(html.find_all('td')[9])
            insolation.append(html.find_all('td')[11])
            brightness.append(html.find_all('td')[13])
            transparency.append(html.find_all('td')[15])
            ok_to_open.append(html.find_all('td')[17])


            try:
                moon.append(html.find_all('td')[21])
                interlock_reason.append(html.find_all('td')[19])


            except IndexError:
                moon.append(html.find_all('td')[19])
                interlock_reason.append("none")


        if val['id'] == '#site-tfn-time':
            last_time = val['val']
            #print "time is:", last_time





# print dew_point
# print pressure
# print humidity
# print wind
# print insolation
# print brightness
# print transparency
# print ok_to_open
# print interlock_reason
# print moon
#print last_time

print "*********************************************************"
print "Temperature:" + clear_data('temperature', temperature[temperature.__len__() - 1])
print "Dew Point:" + clear_data('dew_point', dew_point[dew_point.__len__() - 1])
print "Pressure:" + clear_data('pressure', pressure[pressure.__len__() - 1])
print "Humidity:" + clear_data('humidity', humidity[humidity.__len__() - 1])
print "Wind:" + clear_data('wind', wind[wind.__len__() - 1])
print "Insolation:" + clear_data('insolation', insolation[insolation.__len__() - 1])
print "Brightness:" + clear_data('brightness', brightness[brightness.__len__() - 1])
print "Transparency:" + clear_data('transparency', transparency[transparency.__len__() - 1])
print "OK to Open:" + clear_data('ok_to_open', ok_to_open[ok_to_open.__len__() - 1])
print "Interlock Reason:" + clear_data('interlock_reason', interlock_reason[interlock_reason.__len__() - 1])
print "Moon:" + clear_data('moon', moon[moon.__len__() - 1])
print "Time:", clear_data('last_time', last_time)
print "*********************************************************"
