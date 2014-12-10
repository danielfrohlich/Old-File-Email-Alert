#!/usr/bin/env python

## import needed modules

import os.path, time, datetime, smtplib, sys

from email.header import Header
from email.mime.text import MIMEText
from getpass import getpass
#from smtplib import SMTP_SSL
from smtplib import SMTP

# Set fixed parameters for this script
mail_user = 'EMAIL USERNAME'
mail_password = 'EMAIL PASSWORD'
mail_server = 'EMAIL SERVER NAME'
mail_from = mail_user + '@DOMAIN.COM'
mail_to = ['EMAIL1', 'EMAIL2']  # string list

## Obtains filename from what is entered in the command line interface. To run, type "python ThisScriptName.py [filename you want to check]"

contentfile = str(sys.argv[1])
scriptfilename = str(sys.argv[1])

## modified checks for the last modified time on the filename given, modifiedtimeformat identifies the time format so that it can be modified and
## converts it into epoch time

modified = time.ctime(os.path.getmtime(contentfile))
modifiedtimeformat = int(time.mktime(time.strptime(modified, "%a %b %d %H:%M:%S %Y")))

## two variables that have the same time format, the modified time of the file and the current time upon script execution
## I divide by 3600 to convert seconds into hours and use epoch time for both currenttime and lastmodified

lastmodified = int(modifiedtimeformat)/3600
currenttime = int(time.time())/3600
datetime = datetime.datetime.now()

## identifies the difference between modified time and current time, the int function converts the time into an integer

timedifference = int(currenttime) - int(lastmodified)

## This message will be included in the body of the email which is sent out

Subject = 'Error: %s Did Not Update' % scriptfilename
Message = 'This file is more than %s hours old and did not execute properly today.' % timedifference

## If statement to see if time difference is greater than 24 hours, TRUE or FALSE is identified, int function converts the time diff into an integer

if int(timedifference) > 24:
   sendemail="TRUE"
else:
   sendemail="FALSE"

## Send Email, starts with if statement to see if it should actually send the email
if(sendemail == "TRUE"):
## 'Message' below is the variable shown above
    msg = MIMEText(Message)
    msg['Subject'] = Subject
    msg['From'] = mail_from
    msg['To'] = ", ".join(mail_to)

    s = smtplib.SMTP(mail_server)
    s.ehlo()
    s.starttls()
    s.login(mail_user, mail_password)
    s.sendmail(mail_from, mail_to, msg.as_string())
    s.close

## print the last modified time and the most current time

print "*** Generated  %s" % datetime
print "    Filename: %s" % scriptfilename
print "    Last Modified (epoch time): %s" % lastmodified
print "    Current Time (epoch time): %s" % currenttime
print "    Time Difference in Hours: %s" % timedifference
print "    Mail recipients: %s" % ", ".join(mail_to)
print "    Send Email? %s" % sendemail
