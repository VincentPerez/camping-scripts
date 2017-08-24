#!/usr/bin/python
import mechanize
import re
import os
import urllib
import json
import smtplib

config = {}
execfile("config.conf", config)

def send_mail(title, text):
    fromaddr = config['username']
    toaddrs = config['recipients']
    msg = """Subject: """ + title + """

""" + text

    username = config['username']
    password = config['password']
    server = smtplib.SMTP_SSL('smtp.gmail.com:465')
    server.ehlo()
    # server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


br = mechanize.Browser()
br.set_handle_robots(False)
br.set_handle_refresh(False)
br.addheaders = [('User-agent', 'Firefox')]
br.open("https://www.recreation.gov/camping/watchman-campground-ut/r/campgroundDetails.do?contractCode=NRSO&parkId=70923")
br.select_form('unifSearchForm')
br.form['arrivalDate'] = "Sat Sep 02 2017"
br.form['departureDate'] = "Sun Sep 03 2017"
resp = br.submit()
txt = resp.read()

txt = txt[txt.find("matchSummary"):txt.find("matchSummary")+txt[txt.find("matchSummary"):].find("</div>")]
txt = txt[txt.rfind(">")+1:][0:1]
# print txt
if txt != "0":
    send_mail("GO GO GO WATCHMAAAAN", "Reservation url : https://www.recreation.gov/camping/watchman-campground-ut/r/campgroundDetails.do?contractCode=NRSO&parkId=70923 ")
