import unittest
from participant import Participant
from textmessenger import TextMessenger
from datetime import datetime,timedelta
from database import Database

def valid_time(date_text): 
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return False

# phone, twilio, num_today, start_date, lab_day, money_day

class TestEverything(unittest.TestCase):

	def setUp(self):
		self.p_week1 = Participant(16169162477,17348884244,0,datetime.now(),10,20)
		self.p_week5 = Participant(16169162477,17348884244,0,datetime.now()-timedelta(weeks=4,days=2),10,20)
		self.p_week6 = Participant(16169162477,17348884244,0,datetime.now()-timedelta(weeks=5,days=2),10,20)
		self.p_targt = Participant(16169162477,17348884244,0,datetime.now(),0,20)

	def test_next_day_start_time(self):
		now = datetime.now()
		start = self.p_week1.next_day_start_time()
		self.assertNotEqual(start.day, now.day)
		self.assertGreaterEqual(start.hour, 10)
		self.assertLess(start.hour, 16)

		start = self.p_week5.next_day_start_time()
		self.assertNotEqual(start.day, now.day)
		self.assertEqual(start.hour, 10)

		start = self.p_week6.next_day_start_time()
		self.assertNotEqual(start.day, now.day)
		self.assertGreaterEqual(start.hour, 10)
		self.assertLess(start.hour, 22)
		return

	def test_next_time(self):
		now = datetime.now()
		next = self.p_week1.next_message_time()
		self.assertEqual(next.day, now.day)
		self.assertGreaterEqual(next.hour, 10)
		self.assertLess(next.hour, 22)
		return 

	def test_database(self):
		db = Database()
		db.create_and_empty_tables()
		db.log(1234, 'test', 'content')
		logs = db.fetch_logs()
		self.assertEqual(logs[0]['event'],'test')
		db.new_participant(123456789, 987654321, '2014-05-04', '2014-06-05')
		db.update_participant(123456789,"twilio", 1111111111)
		participants = db.load_participants()
		self.assertEqual(participants[0][0],123456789)
		db.log_email('test@test','$0.36')
		emails = db.fetch_email()
		self.assertEqual(emails[0]['email'],'test@test')
		db.create_and_empty_tables()


if __name__ == '__main__':
    unittest.main()