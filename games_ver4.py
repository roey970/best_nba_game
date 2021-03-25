import requests
from lxml import html
import smtplib
import config
import datetime , timedelta
import time
import pytz


#This will create a list of buyers:
#buyers = tree.xpath('//div[@class="iptbl"]/text()')
#This will create a list of prices

def get_game():
    try:
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        page = requests.get('http://stats.inpredictable.com/nba/preCap.php')
        tree = html.fromstring(page.content)
        games = tree.xpath('//a[@target="_blank"]/text()')
        Excitement= tree.xpath('/html/body/div[5]/div/div/table/tbody/tr/td[4]/text()')
        date = tree.xpath('/html/body/div[5]/div/span/text()')
        web_date = date[0].split(',')[0].split()[5]
        #today_date = str(datetime.date.today()).split('-')[2]
        #tz_NY = pytz.timezone('America/New_York')
        #datetime_NY = datetime.datetime.now(tz_NY)
        #today_date = str(datetime_NY.today()).split('-')[2][0:2]
        before = datetime.date.today() - timedelta.Timedelta(minutes=1440)#24 hours
        today_date = str(before.strftime(fmt)).split('-')[2][0:2]
        print today_date
        print web_date

        if today_date != web_date:
            return "no games today"


        #create list of good games
        c=0
        good_games=[]
        for i in Excitement:
            if float(i)>=9:
                good_games.append(games[c+1])
            c+=1
        #print good_games

        #crete string
        string=""
        if not good_games:
            return "all games were bad"
        for g in good_games:
            string+=g+"  "
        #print string
        return string

    except:
        return "there were no games"


# function for sending SMS
def sendSMS(subject):
    try:
        server =smtplib.SMTP('smtp.gmail.com:587')#587
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADRESS_FROM,config.PASSWORD)
        for email in config.EMAIL_ADRESS_TO:
            server.sendmail(config.EMAIL_ADRESS_FROM, email, 'Subject: {}\n\n{}'.format(subject, ""))
        #server.sendmail(config.EMAIL_ADRESS_FROM,config.EMAIL_ADRESS_TO,'Subject: {}\n\n{}'.format(subject,""))
        server.quit()
        print "email sent"
    except:
        print "email not sent"




def start():
    while True:
        now = datetime.datetime.now()
        print now.hour
        if now.hour == 8:
            massage = get_game()
            sendSMS(massage)
        time.sleep(60 * 60)


start()
"""
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

tz_NY = pytz.timezone('America/New_York')
datetime_NY = datetime.datetime.now(tz_NY)
today_date = str(datetime_NY.today()).split('-')[2][0:2]
before = datetime.date.today() - timedelta.Timedelta(minutes=1500)
"""
#print before.strftime(fmt)
#today_date = str(before.strftime(fmt)).split('-')[2][0:2]
#print today_date

