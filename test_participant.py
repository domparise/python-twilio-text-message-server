import unittest
from participant import Participant
from textmessenger import TextMessenger
from datetime import datetime,timedelta

def valid_time(date_text): 
    try:
        return datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return False


class TestParticipant(unittest.TestCase):

	def setUp(self):
		self.p_week1 = Participant(16169162477,datetime.now(),valid_time('2014-05-03'),valid_time('2014-06-02'),TextMessenger(17348884244))
		self.p_week5 = Participant(16169162477,datetime.now()-timedelta(weeks=5),valid_time('2014-05-03'),valid_time('2014-06-02'),TextMessenger(17348884244)) 
		self.p_week6 = Participant(16169162477,datetime.now()-timedelta(weeks=6),valid_time('2014-05-03'),valid_time('2014-06-02'),TextMessenger(17348884244))
		self.p_targt = Participant(16169162477,datetime.now(),datetime.now(),valid_time('2014-06-02'),TextMessenger(17348884244))

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


	def test_next_time_when_invalid(self):
		pass


if __name__ == '__main__':
    unittest.main()