"""
set environment variables.
"""
import os
import sys


# root path for job_surveillance dir
PATH = None
# user name
USER = None
# user email address
USER_EMAIL = None
# fake email address from which sending email
# to users.
SERVER_EMAIL = None


# initial environment var
PATH = os.environ['JOB_SVLN_PATH'].rstrip('/')+'/'
PATH = os.path.expanduser(PATH)
if not os.path.isdir(PATH):
    print "Terminated: JOB_SVLN_PATH is not valid!\n"
    sys.eixt()

USER       = os.environ['JOB_SVLN_USER']
USER_EMAIL = os.environ['JOB_SVLN_USER_EMAIL']
SERVER_EMAIL  = os.environ['JOB_SVLN_SERVER_EMAIL']
