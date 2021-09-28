# gdnsu
A simple script to update your dynamic DNS host on our favorite not evil platform

This script is not too complicated, but only runs from command-line at this time.

MODULES:

-gdnsu.py
The main module. Run "python3 gdnsu.py" (after filling out settings.csv) to update the hostname listed therein with your current public IP as reported by our favorite primary-colored organization's IP checker.

-funcsGDNSU.py
The functions used by the main module. Must live in the same directory as gdnsu.py. Not merged into main because I may do more with this project.

-settings.csv
Settings used by the program. Fill this out before running. Must live in the same directory as gdnsu.py.
Do not insert any commas. Do not edit the first line (name,value).
Fill in the 'value' column according to the following:

	hostname : The dynamic DNS hostname you wish to update the IP for. Only one at a time for the moment.
	uname    : The username assigned to the host. Found in the DDNS console.
	pwd      : The password assigned to the host. Found in the DDNS console.
	email    : Your email address. Used in the UserAgent string in the request headers.
	logging  : Must be either "True" or "False", depending on if you want gdnsu to log to a file (./gdnsu.log)
	lastIP   : Leave this blank. Used to check if we need to send an update. Will be updated automatically by the program.
	           Edit this field to force the script to send an update to your DDNS host. Don't be surprised if you get a 'no change' response though. Check your DDNS console to see if the IP already matches.
