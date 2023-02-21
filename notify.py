#!/usr/bin/env python3
# encoding: utf-8
# 用于FCGI的简易通知脚本
import os
import json
import sys
from urllib import request, parse

chat_id = ""
bot_token = ""
ret = "Hello"
status = "Status: 200"
evt = {}
want_send = True
try:
    evt = json.loads(sys.stdin.read())
except json.JSONDecodeError:
    status = "Status: 400"
    ret = "JSON error"
    want_send = False

con_type = os.environ.get('CONTENT_TYPE', None)
if con_type != "application/json":
    status = "Status: 403"
    ret = "content-type error"
    want_send = False
if want_send:
    bot_message = "%s" % (evt.get('msg', None))
    qs = parse.urlencode(
        {"chat_id": chat_id, "parse_mode": "HTML", "text": bot_message})
    url = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?'+qs
    # print(url)
    # with open("notify.log","a") as fp:
    #    fp.write(json.dumps(evt))
    #    fp.write("\n")
    #    fp.write(url)
    #    fp.write("\n")
    try:
        req = request.Request(url)
        resp = request.urlopen(req)
    except Exception as e:
        print(url, file=sys.stderr)
        raise e

print(status)
print("Content-Type: text/plain\r\n")
print(ret)
