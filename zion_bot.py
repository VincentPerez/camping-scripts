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


camp_list = ["30027001", "30027003", "30027005",
             "30027007", "30027009", "30027012"]
for item in camp_list:
    br = mechanize.Browser()
    br.set_handle_robots(False)   # ignore robots
    br.set_handle_refresh(False)  # can sometimes hang without this
    br.addheaders = [('User-agent', 'Firefox')]
    br.open("https://zionpermits.nps.gov/wilderness.cfm?TripTypeID=1")
    br.select_form('chgresourceform')
    br.form['ResourceID'] = [item]
    resp = br.submit()
    txt = resp.read()
    txt = txt[txt.find("September 3,"):txt.find(
        "September 3,") + txt[txt.find("September 3,"):].find("</p></td>")]
    txt = txt[txt.rfind(">") + 1:]
#   print txt
    if txt != "0":
        send_mail("Places libres au camp Narrows numero " + item[item.rfind("0") + 1:], "Verifier le camp numero " + item[item.rfind(
        "0") + 1:] + "\nhttps://zionpermits.nps.gov/wilderness.cfm?TripTypeID=1")
