import secrets
import base64
import os
from funcsGDNSU import doGet, doPost, getTimestamp, writeLog, pw

pw("\n===============Run Start===============")
hostname = "fartss.beesnakez.net"
uname = "Gao5f9zDwEmfq87y"
pwd = "YKp9Odp6zumKQfVg"
ipuri = "https://domains.google.com/checkip"

msg = "Hostname: " + hostname
pw(msg)

ippath = os.getcwd() + "\\ip.txt"
try:
    with open(ippath, 'r') as f:
        lastIP = f.readline()
except:
    lastIP = None
msg = "Last IP: " + lastIP
pw(msg)

headers = {
    "Host": "domains.google.com",
    "UserAgent": "Chrome/41.0 nt04defreece@gmail.com"
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
