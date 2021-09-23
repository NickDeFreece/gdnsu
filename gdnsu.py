import secrets
import base64
import os
from funcsGDNSU import doGet, doPost, getTimestamp, writeLog, pw

pw("\n===============Run Start===============")

#Fill in your own details here


################################################# DO NOT EDIT BELOW THIS LINE ########################################################
ipuri = "https://domains.google.com/checkip"
cwd = os.getcwd()
settingsPath = cwd + "/settings.csv"
ippath = cwd + "\\ip.txt"
settings = dict()
settingList = csvToDictList(settingsPath)
for d in settingList:
    settings.update({d['name'], d['value']}) #This line is why settings.csv needs to keep the same header: name,value

msg = "Hostname: " + settings['hostname']
pw(msg)

try:
    with open(ippath, 'r') as f:
        lastIP = f.readline()
except:
    lastIP = None
msg = "Last IP: " + str(lastIP)
pw(msg)

agentString = "Chrome/41.0 " + settings['email']
headers = {
    "Host": "domains.google.com",
    "UserAgent": agentString
}
curIP = str(doGet(ipuri, headers).content, 'utf-8') #Should get current public IP
msg = "Current IP: " + curIP
pw(msg)

if curIP == lastIP:
    pw("No change to pulbic IP. Exiting...")
else:
    pw("IP has changed! Updating...")
    uri = f'https://{uname}:{pwd}@domains.google.com/nic/update?hostname={hostname}&myip={curIP}'
    #print("\nURI: ", uri)

    #Build Headers
    codeVerifier = secrets.token_urlsafe(64)
    codeChallenge = base64.urlsafe_b64encode(bytes(codeVerifier, 'ascii')).rstrip(b'=')
    strCodeChallenge = codeChallenge.decode('utf-8') #This is just to get a string that python can cat to the query string. bytes not allowed by Python.
    strAuth = "Basic " + strCodeChallenge
    #print("\nAuth:\n", strAuth)
    headers.update({"Authorization": strAuth})
    response = doPost(uri, headers)
    msg = "\nResponse Code: " + response.status_code
    pw(msg)
    #print("Response Headers:\n", response.headers)
    if response.status_code in range(200, 400):
        rcontent = str(response.content, 'utf-8')
        msg = "\nContent: " + rcontent
        pw(msg)
        if 'good' or 'nochg' in rcontent: #Want to ensure the file is updated no matter what, so that we know when this was last run
            with open(ippath, 'w') as g:
                g.write(curIP)
            if 'good' in rcontent:
                msg = "\nIP updated for " + hostname + ": "+ curIP
                pw(msg)
