import secrets
import base64
import os
from funcsGDNSU import log, getCSVSettings, setCSVSettings, doGet, doPost

settings = dict()
cwd = os.getcwd()
settingsPath = cwd + "/settings.csv"
settings = getCSVSettings(settingsPath)

log("<<<< RUN START >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", write=settings['logging'])
msg = "Hostname: " + settings['hostname'] + " LastIP: " + settings['lastIP']
log(msg, write=settings['logging'])

agentString = "Chrome/41.0 " + settings['email']
headers = {
    "Host": "domains.google.com",
    "UserAgent": agentString
}

ipuri = "https://domains.google.com/checkip"
curIP = str(doGet(ipuri, headers).content, 'utf-8') #Should get your current public IP
msg = "Current IP: " + curIP
log(msg, write=settings['logging'])

if curIP == settings['lastIP']:
    log("No change to pulbic IP. Exiting...", write=settings['logging'])
else:
    log("IP has changed! Updating...", write=settings['logging'])
    uri = "https://" + settings['uname'] + ":" + settings['pwd'] + "@domains.google.com/nic/update?hostname=" + settings['hostname'] + "&myip=" + curIP

    #Build Headers
    codeVerifier = secrets.token_urlsafe(64)
    codeChallenge = base64.urlsafe_b64encode(bytes(codeVerifier, 'ascii')).rstrip(b'=')
    strCodeChallenge = codeChallenge.decode('utf-8')
    strAuth = "Basic " + strCodeChallenge
    headers.update({"Authorization": strAuth})

    #Send new IP
    response = doPost(uri, headers)
    rcode = str(response.status_code)
    rheaders = str(response.headers)
    rcontent = str(response.content, 'utf-8')
    msg = "Response Code: " + rcode
    log(msg)

    if response.status_code in range(200, 400):
        if 'good' in rcontent or 'nochg' in rcontent: #'nochg' in rconent means the IP was already set to what we were trying to set it to, somehow. Essentially, we made an unnecessary request to G and that should be troubleshot. Could be the last run wasn't able to update the settings file. Could be another instance of this script on your network already made the update.
            settings.update({'lastIP': curIP})
            settingsWrote = setCSVSettings(settings, settingsPath)
            if settingsWrote == True:
                log("Updated settings file with current public IP!", write=settings['logging'])
            else:
                log("Unable to update settings.csv with new IP. Check permissions and file status.")

            if 'good' in rcontent:
                msg = "DDNS IP updated for " + settings['hostname'] + ": " + curIP
            elif 'nochg' in rcontent:
                msg = "DDNS IP for " + settings['hostname'] + " reported as not changed. If it wasnt already updated to match manually, or by another instance of this script, it may be a file permission issue with settings.csv. Check that lastIP setting is being updated to current IP: " + curIP + " and that the Modified Time matches the last time this script was run"
            log(msg, write=settings['logging'])
    else:
        msg = "Failed to send new IP to the cloud! Ensure your hostname, uname, and pwd are valid in settings.csv. POST Response Code: " + rcode
        log(msg, write=settings['logging'])
        msg = "Response Headers:\n" + rheaders
        msg += "\n\nResponse Content:\n" + rcontent
        log(msg, write=settings['logging'])
