"""
This script is used to check jobs status background.
Based on following linux command:
    write
    who
    tmux
    qstat

Usage:
    Run this script on the session created by tmux,
    so that this script can be executed even user
    is log-off.

This script will check the job status every 15 min,
then send a massage to all the opened terminals in
real-time. When the user is log-off, then an e-mail
will be sent.

Note:
    jobs which are finished during 15 min will not
    be checked and reported, which is not annoying
    to send report too frequently.
"""

import time
import os
import os.path
import sys
import smtplib
from subprocess import Popen, PIPE
from email.mime.text import MIMEText

# root path for job_surveillance dir
PATH = None
# user name
USER = None
# user email address
USER_EMAIL = None
# fake email address from which sending email
# to users.
MEI_EMAIL = None
# check jobs status every JOB_SVLN_INTERVAL seconds.
TIME_INTERVAL = None

def main():
    # INITIALATION SETTING
    init_environ()
    # set old info for jobs_status
    jobs_status_old = get_running_jobs()
    # used to save complete jobs when the user is not login
    COMPLET_POOL = []

    # start suveillance
    while True:
        sleep()
        jobs_status_new = get_running_jobs()
        complete = check_jobs(jobs_status_old, jobs_status_new)
        if (complete + COMPLET_POOL):
            terminal_id = get_terminal()
            if terminal_id:
                send_msg(terminal_id, complete+COMPLET_POOL)
                del COMPLET_POOL[:]
            else:
                COMPLET_POOL += complete
                send_email(complete)
        jobs_status_old = jobs_status_new

def SigExit(*string):
    for i in string:
        print i,
    sys.exit()


def sleep():
    global TIME_INTERVAL
    time.sleep(TIME_INTERVAL)


def init_environ():
    global PATH, USER, USER_EMAIL
    global MEI_EMAIL, TIME_INTERVAL
    PATH = os.environ['JOB_SVLN_PATH'].rstrip('/')+'/'
    PATH = os.path.expanduser(PATH)
    if not os.path.isdir(PATH):
        SigExit("Terminated: JOB_SVLN_PATH is not valid!\n")
    USER = os.environ['JOB_SVLN_USER']
    USER_EMAIL = os.environ['JOB_SVLN_USER_EMAIL']
    MEI_EMAIL = os.environ['JOB_SVLN_MEI_EMAIL']
    try:
        TIME_INTERVAL = int(float(os.environ['JOB_SVLN_INTERVAL']))
    except ValueError:
        SigExit("Terminated: JOB_SVLN_INTERVAL is not a number\n")


def send_msg(terminal_id, complete_jobs):
    """
    send msg is based on linux 'write' command.
    using redirect the file tmp.txt which contains all
    the info about finished jobs to achieve sending msg.

    command: write USER terminal_id < tmp.txt
    """
    global USER
    global PATH
    f = open(PATH+'tmp.txt', 'w')
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('Job ID', 'Partition', 'Job Name', 'Stutas').rstrip()
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('-'*15, '-'*15, '-'*25, '-'*5).rstrip()
    for job in complete_jobs:
        info = job.split()
        print >>f, "{:15s} {:15s} {:25s} {:5s}"\
                .format(info[0], info[1], info[2], 'C').rstrip()
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('-'*15, '-'*15, '-'*25, '-'*5).rstrip()
    f.close()

    for ID in terminal_id:
        cmd = string_combine('write', USER, ID, '<', PATH+'tmp.txt')
        os.system(cmd)
    os.remove(PATH+'tmp.txt')


def send_email(complete_jobs):
    """
    when user is not login, notify user by email when there is a job
    finished.
    """
    # exit function is no jobs completed
    if not complete_jobs:
        return

    global USER
    global PATH
    global USER_EMAIL, MEI_EMAIL
    # write email content into a tmp file
    f = open(PATH+'tmp.txt', 'w')
    print >>f,  "-"*62 + '\n'
    print >>f, ("This is an automatical email from et-mei sever in Yang's\n"
                "Goup at Department of Chemistry, Duke University.\n"
                "Do not reply this email!\n")
    print >>f,  "-"*62  + '\n'
    print >>f,  "Dear " + USER + ':\n'
    print >>f, ("Here is a notification that you have new job(s) completed.\n"
                "Below are the details.\n")
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('Job ID', 'Partition', 'Job Name', 'Stutas').rstrip()
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('-'*15, '-'*15, '-'*25, '-'*5).rstrip()
    for job in complete_jobs:
        info = job.split()
        print >>f, "{:15s} {:15s} {:25s} {:5s}"\
                .format(info[0], info[1], info[2], 'C').rstrip()
    print >>f, "{:15s} {:15s} {:25s} {:5s}"\
            .format('-'*15, '-'*15, '-'*25, '-'*5).rstrip()
    print >>f,  "\nHave a good day!\n"
    print >>f, ("Best,\n"
                "From et-mei\n\n"
                "Department of Chemistry\n"
                "Duke University\n"
                "https://chem.duke.edu/labs/yang")
    f.close()

    # sending email
    f = open(PATH+'tmp.txt', 'r')
    msg = MIMEText(f.read())
    f.close()

    msg['Subject'] = 'et-mei: Job finished!'
    msg['From'] = MEI_EMAIL
    msg['To'] = USER_EMAIL

    s =  smtplib.SMTP('localhost')
    s.sendmail(msg['From'], msg['To'], msg.as_string())
    s.quit()
    os.remove(PATH+'tmp.txt')
    return


def string_combine(*string):
    """
    combine string with whitespace as delimeter
    """
    combined_str = ''
    for i in string:
        combined_str += i + ' '
    return combined_str.rstrip()


def get_running_jobs():
    """
    Filter all the info returned by 'qstat -u user' command.
    Information is a string sperated by space, which contains
    "JobID, PartitionName, JobName, JobStatus".
    Only info of runninng jobs will be collected.

    Return a list of Jobs information.
    """
    cmd = ['qstat', '-u', USER ]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stdout = filter(None, stdout.split('\n'))
    jobs_status = []
    # collect jobs_line into jobs_status
    # criterion is that jobs_line start with jobs_ID
    for line in stdout:
        line_split = line.split()
        if line_split[0].isdigit():
            if line_split[9] == 'R':
                info = string_combine(line_split[0], line_split[2],
                                      line_split[3])
                jobs_status.append(info)
    return jobs_status

def get_terminal():
    """
    Get terminal ID when a user log in through multiple terminals.
    This function is based on linux 'who' command.

    return a list of turminal ID.
    """
    global USER
    cmd = ['who']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    stdout = filter(None, stdout.split('\n'))
    terminal_id = []
    for line in stdout:
        line_split = line.split()
        if USER in line_split:
            terminal_id.append(line_split[1])
    return terminal_id


def check_jobs(jobs_status_old, jobs_status_new):
    """
    compare jobs_status_old with jobs_status_new to find the
    jobs that are finished.

    Return a list of finished jobs with the same pattern as jobs_status_old
    """
    jobid_new = [x.split()[0] for x in jobs_status_new]
    complete_jobs = []
    for job in jobs_status_old:
        jobid = job.split()[0]
        if jobid not in jobid_new: # this jobs finished
            complete_jobs.append(job)
    return complete_jobs

if __name__ == '__main__':
    main()
