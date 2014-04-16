Python-Twilio Text message server  
==========================  
  
Dependencies  
============  
installed with pip

sqlite3  
twilio  
pytz  
Flask  

How to run  
==========  
1. Initialize database:  
	python test-database.py  
  
2. Write configuration file:  
  - name it config.py  
  - declare the following variables:  
  	default_sms  
  	invalid_sms_response  
  	verification_sms  
  	twilio_sid  
  	twilio_auth_token  
  	gmail_text  
  	gmail_subject  
  	gmail_user  
  	gmail_pwd  

3. Set twilio account information:  
	at: https://www.twilio.com/user/account/phone-numbers/incoming  
	select a number, then under 'Messaging', set the request url to:  
	http://your.ip:5000/receiver   

4. Run the server:  
	python server.py  

5. Use the interface:  
  The server operates on Flask default port 5000  
  The interface exposes the following:
  /new-participant  -- input a new participant  
  /participant/:phone-number   -- view and change a participant  
  /data  -- output the 'log' table of the database (csv, doesnt render well though)  
  /email -- input an email address, complete form to send emails at specified times  


