import participant
from database import Database
from textmessenger import TextMessenger
from datetime import datetime
import pytz,math
from random import random
from datetime import datetime,timedelta,date

def valid_time(date_text): 
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return False

def valid_number(number):
    if isinstance(number,int):
        if len(number) == 11:
            return int(number)
    return False

db = Database()

txt = TextMessenger(17348884244)
p = participant.Participant(16169162477,datetime.now(),valid_time('2014-05-03'),valid_time('2014-06-02'),txt)
start_time = p.next_day_start_time()
print 'Tomorrow start time: '+ str(start_time.hour) + ':' + str(start_time.minute)
with_poisson = participant.add_poisson(1.5,start_time)
print 'start time with poisson: '+ str(with_poisson.hour) + ':' + str(with_poisson.minute)

if p.tmr_is_target_day():
	print 'p target day'

p2 = participant.Participant(16169162477,datetime.now(),valid_time('2014-05-03'),valid_time('2014-04-14'),txt)
if p2.tmr_is_target_day():
	print 'p2 target day'


oneMin = datetime.now() + timedelta(minutes=1)
p.set_next_msg(oneMin)
# throws error, because there is no timers to cancel

# need to test to ensure timers are cancelled
# also need to verify stops sending after 6


