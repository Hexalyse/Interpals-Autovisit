#!/usr/bin/env python

import time
import sys
import os
import requests
import re
import random
import getpass

##
## CONFIG VARIABLES : YOU CAN EDIT THESE VARIABLES TO CHANGE TIMER VALUES ##
##
MIN_DELAY_BETWEEN_PROFILE_VIEWS = 1
MAX_DELAY_BETWEEN_PROFILE_VIEWS = 5
DELAY_BETWEEN_RUNS = 30
sex = '' # Possible values: 'male', 'female', or empty '' for both
cont = '' # Possible values: 'AF' (Africa) 'AS' (Asia), 'EU' (Europe)
            #'NA' (North America), 'OC' (Oceania), 'SA' (South America)
age1 = 18 # minimum age
age2 = 38 # maximum age

# We keep already visited profile in a file to avoid visiting
# a profile multiple times on consecutive execution of this script
# YOU CAN DELETE THIS FILE IF YOU WANT TO VISIT EVERYBODY ONCE AGAIN
visitedUsersFilename = "users_visited.txt"

# Set this variable to True to output debug log,
# or False for more concise output
DEBUG = False
##
## END OF CONFIG VARIABLES
##


sessioncount = 0
run_number = 1
f = open(visitedUsersFilename, 'a+')
processedUsers = [line.strip() for line in f]
print "Already processed " + str(len(processedUsers)) + " users."
s = requests.Session()
login = raw_input('Username (mail): ')
password = getpass.getpass('Password: ')
payload = {'action': 'login',
           'login': login,
           'auto_login' : '1',
           'password': password}

print "Logging in..."
s.get("https://www.interpals.net/")
r = s.post("https://www.interpals.net/login.php", data=payload)
print "Logged in: Starting the dance \o/"
time.sleep(2)
#print r.headers
#print r.text
while True:
    runcount = 0
    if DEBUG:
        print "Fetching online users page..."
    r = s.get("https://www.interpals.net/online.php?sex=%s&cont=%s&age1=%d&age2=%d" % (sex, cont, age1, age2))
    data = r.text
    usernames = re.findall(r'<div class=\'online_prof\'><a href=\'([a-zA-Z0-9\-_]+)\'', data, re.M)
    for username in usernames:
        if username not in processedUsers:
            if DEBUG:
                print "Visiting profile of " + username + " (" + str(sessioncount) + ")"
            runcount += 1
            sessioncount += 1
            r = s.get("https://www.interpals.net/" + username)
            waitTime = random.randrange(MIN_DELAY_BETWEEN_PROFILE_VIEWS*10, MAX_DELAY_BETWEEN_PROFILE_VIEWS*10) / float(10)
            if DEBUG:
                print "Waiting " + str(waitTime) + "s"
            else:
                os.system('cls' if os.name=='nt' else 'clear')
                print ('\rRun %d - Fetched %d users (%d total)' % (run_number, runcount, sessioncount))
            time.sleep(waitTime)
            processedUsers.append(username)
            f.write(username + "\n")
        elif DEBUG:
            print "Already visited " + username
    run_number += 1
    if (runcount < 20):
        print ('[-] Waiting (%d)s before next run (fetched %d users this run, %d total)\n' % (DELAY_BETWEEN_RUNS * 4, runcount, sessioncount))
        time.sleep(DELAY_BETWEEN_RUNS * 4)
    else:
        print ('[+] Waiting (%d)s before next run (fetched %d users this run, %d total)\n' % (DELAY_BETWEEN_RUNS, runcount, sessioncount))
        time.sleep(DELAY_BETWEEN_RUNS)

# This script is ugly. It was made rapidly, for fun. At least, it does its job.

