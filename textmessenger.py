# Dom Parise - 4/13/2014
# Text messaging / twilio wrapper module
# To install dependencies: sudo pip install twilio
#
# experiment variables:
import config_vars
from twilio.rest import TwilioRestClient

class TextMessenger:
    # initialize twilio client
    def __init__ (self, from_number):
        self.client = TwilioRestClient(config_vars.twilio_sid, config_vars.twilio_auth_token)
        self.from_number = '+'+str(from_number)
    # send a text message
    def send_default_sms (self, to_number):
        self.client.sms.messages.create(body=config_vars.default_sms, to='+'+str(to_number), from_=self.from_number)

    def send_verification (self, to_number):
    	self.client.sms.messages.create(body=config_vars.verification_sms, to='+'+str(to_number), from_=self.from_number)