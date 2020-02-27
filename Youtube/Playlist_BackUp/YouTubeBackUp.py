from __future__ import unicode_literals
import youtube_dl
import json
import os
import os.path
import datetime
import smtplib, ssl

path = os.getcwd()
filename= "config.json"

with open(filename) as f:
    data = json.load(f)
    # print(data['schedule']['start'])
    # print(data['schedule']['end'])
playlists = data['playlist']
for playlist in playlists:
    # un passage tous les 24h
    if "dlDate" in playlist:
        dt = datetime.datetime.strptime( playlist['dlDate'], "%Y-%m-%d %H:%M:%S")
        if (datetime.datetime.now()-dt).days<1 :
            continue
    pathDir = playlist['directory']
    url = playlist['url']
    print("\n=== ", pathDir.upper(), " ===\n")
    if not os.path.isdir(pathDir):
        try:
            os.mkdir(pathDir)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)
    os.chdir(pathDir)
    ydl_opts = {'ignoreerrors': True,
    'playlistrandom': True}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except ValueError:
        print("!! Download Error !! ")
        os.chdir(path)
        continue
    os.chdir(path)
    with open(filename,'w') as output:
        playlist['dlDate'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json.dump(data, output)


port = 587  # For starttls
smtp_server = "smtp.xmail.com"
sender_email = "xxx@xmail.com"  # Enter your address
receiver_email = "xxx@xmail.com"  # Enter receiver address
password = "xxxx"
message = "Subject: Serveur 1 YouTubeBackUp.py closed"

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    
    