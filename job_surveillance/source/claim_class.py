"""
claims for the used class.
"""

import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from subprocess import Popen, PIPE

import claim_environ
import claim_func as sf
import config

class Job():
    """
    Package up all the information of a job.
    """

    job_id    = None # <type: str>
    job_name  = None # <type: str>
    user      = None # <type: str>
    time      = None # <type: int> unit in minutes.
    status    = None # <type: str>
    partition = None # <type: str>

    _byemail  = None # <type: bool> lable if the job is added in the
                     # _email_box.
                     # This var will be only updated by MessageMan.
    _finish_time = None # <type: str>
                        # record the time when the job is finished.
                        # This var will be assigned by CollectMan.
    def __init__(self, qstat_line):
        """
        Input: <type: str> qstat_line.
               qstat_line is a string line obtained from the
               command "qstat". It is sperated by whitespace.
               E.g.
                job_id   user  par   job_name      **  *  *  **  *****  status time
               "1786514  USER  mei3  12.losc-lda   --  1  1  --  166:4  Q      00:00"
        Output: <type: class Job> Job
        """
        line = qstat_line.split()
        self.job_id    = line[0]
        self.user      = line[1]
        self.partition = line[2]
        self.job_name  = line[3]
        self.status    = line[9]
        # convert time info into minutes.
        _time = line[10].split(':')
        self.time = int(_time[0])*60 + int(_time[1])

    def islongrun(self):
        """
        check if the job's running time is longer than the USER specified
        criteria.

        Output: <type: bool>
        """
        return (self.time >= config.RUNTIME_THRESHOLD)

    def isdone(self):
        """
        check if the job is done or not.

        Output: <type: bool>
        """
        return (self.status == "C")

    def isrunning(self):
        """
        check if the job is running or not.

        Output: <type: bool>
        """
        return (self.status == "R")

    def __str__(self):
        return "<Class: Job>: \n"+"{} {} {} {} {} {}"\
                .format(self.job_id, self.user, self.partition,
                        self.job_name, self.status, str(self.time))


class JobOffice():
    """
    This office is like a post office, and it will
    keep recieving and storing job packages, which is finished and
    be notified the user.
    """

    # A box contains jobs (<object: Job>) for writing message
    # to the user.
    # _message_box is THE MAIN BOX.
    # New jobs will ALWAYS be thrown into this box.
    _message_box = {}

    # A box contains jobs (<object: Job>) for writing email
    # to the user.
    # jobs in this box will be copied from "_message_box".
    # !!!
    # _email_box is a subset of _message_box
    _email_box   = {}

    def add(self, job):
        """
        Functionality:
        Add new job to self._message_box in the JobOffice.

        Input: <type: class Job> job
        Output: None
        """
        self._message_box[job.job_id]=job

    def delete(self, job):
        """
        Delete a job from self._message_box in the JobOffice.

        Input: <type: class Job> job
        Output: None
        """
        del self._message_box[job.job_id]

    def add_to_emailbox(self, job):
        """
        copy a job from self._message_box  to self._email_box.

        Input: <type: class Job> job
        Output: None
        """
        self._email_box[job.job_id]=job

    def find(self, job_id):
        """
        Find the job package by its job_id.

        Input: <type: str> job_id
        Output: <type: class Job> Job
        """
        return self._message_box[job_id]

    def __str__(self):
        print "<type: class JobOffice>"
        print "ID of jobs in Message_box <dict>:"
        jobs = [x for x in self._message_box.keys()]
        print jobs
        print "ID of jobs in Email_box <dict>:"
        jobs = [x for x in self._email_box.keys()]
        print jobs
        return ""


class CollectMan():
    """
    A specific JobOffice has to associated to this man.
    This man will collect completed jobs which
    meet the collection requirement, process these jobs
    and add collected jobs into the associated JobOffice.

    Completed jobs collection requirement:
    1. the status of job is completed.
    2. the running time of job is greater than the criteria
    """

    # specify which job_office the man is working for.
    # stores the job_office reference.
    _working_job_office = None

    # old jobs record
    _job_old = None # <type: dict>
    # new jobs record
    _job_new = None # <type: dict>

    def __init__(self, JobOffice):
        self._working_job_office = JobOffice

    def get_terminal(self):
        """
        Get terminal ID in which the uesr is log-in.
        This function is based on linux 'who' command.

        Input: None
        Output: <type: list> terminal_id. Each element in
                terminal_id is a string.
        """
        cmd = ['who']
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        stdout = filter(None, stdout.split('\n'))
        terminal_id = []
        for line in stdout:
            line_split = line.split()
            if claim_environ.USER in line_split:
                terminal_id.append(line_split[1])
        return terminal_id

    def collect(self):
        """
        Functionality:
        Collect completed jobs packages which meet the collection
        requirement, make a time stamp on it and add them to the
        related JobOffice.

        collection requirement: completed job's finish time is longer than specified
        number or the user is not log-in at that collcetion moment.

        Output: None
        """
        def get_qstat():
            """
            running external "qstat" command.
            return a list of jobs info.

            Input: None
            Output: <type: list> stdout. Each element is a string.
            """
            cmd = [ 'qstat', '-u', claim_environ.USER]
            p = Popen(cmd, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            stdout = filter( None, stdout.split('\n') )
            if stdout:
                return stdout[4:]
            # return a empty list when stdout is empty.
            return stdout

        def get_running_jobs(qstat):
            """
            Input: <type: list> qstat. Each element is a string.
                   qstat list is generated from function "qstat()".

            Output: <type: list> running_jobs. Each element is <type: class Job>.
            """
            running_jobs = []
            for i in qstat:
                job = Job(i)
                if job.isrunning():
                    running_jobs.append(job)
            return running_jobs

        qstat = get_qstat()
        # init old and new job info list.
        if self._job_old == None:
            self._job_old = {}
            for i in get_running_jobs(qstat):
                self._job_old[i.job_id] = i
        # get new jobs list
        self._job_new = {}
        for i in get_running_jobs(qstat):
            self._job_new[i.job_id] = i
        # get complete jobs_id.
        complete_jobs_id = set( self._job_old.keys() ) - set( self._job_new.keys() )
        # add complete jobs into JobOffice.
        time = datetime.now().strftime('%H:%M')
        # start collect completed jobs.
        log_in = bool(self.get_terminal())
        if log_in:
            job_list = [ self._job_old[i] for i in complete_jobs_id if self._job_old[i].islongrun() ]
        else:
            job_list = [ self._job_old[i] for i in complete_jobs_id ]
        for job in job_list:
            job._finish_time = time
            job.status = 'C'
            self._working_job_office.add(job)
        #for i in complete_jobs_id:
        #    job = self._job_old[i]
        #    if job.islongrun():
        #        job._finish_time = time
        #        job.status = 'C'
        #        self._working_job_office.add(job)
        # update old jobs list.
        self._job_old = self._job_new
        return

class MessageMan():
    """
    This man will write message to the user, when it is the case.
    He will keep an eye on the JobOffice._message_box.
    This man has to be associated with a specific JobOffice.
    """
    # the office for which this man is working for.
    _working_job_office = None # <type: class JobOffice>

    def __init__(self, JobOffice):
        """
        Input: <type: class JobOffice> JobOffice
        Output: <type: class MessageMan> MessageMan
        """
        self._working_job_office = JobOffice

    def get_terminal(self):
        """
        Get terminal ID in which the uesr is log-in.
        This function is based on linux 'who' command.

        Input: None
        Output: <type: list> terminal_id. Each element in
                terminal_id is a string.
        """
        cmd = ['who']
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        stdout = filter(None, stdout.split('\n'))
        terminal_id = []
        for line in stdout:
            line_split = line.split()
            if claim_environ.USER in line_split:
                terminal_id.append(line_split[1])
        return terminal_id

    def send_msg(self):
        """
        Functionality:
        Every time when the JobOffice._message_box is not empty, MessageMan
        will try to write a message to the user. If the writing message is
        successful, he will clean and empty the JobOffice._message_box and
        JobOffice._email_box. Otherwise, that is in the case the user is not login,
        MessageMan will link the job package into JobOffice._email_box, and
        lable the job's Job._byemail with "True", then return.

        Input: None
        Output: None
        """
        def _send_msg(terminal_id, message_box):
            """
            send msg is based on linux 'write' command.
            using redirect the file tmp.txt which contains all
            the info about finished jobs to achieve sending msg.

            command "write" usage:
            $: write USER terminal_id < tmp.txt

            Input: <type: list> terminal_id. Each element is a string
                   which stands for an opened terminal.
                   <type: dict> message_box. The same type as
                   JobOffice._message_box.
            Output: None
            """
            USER = claim_environ.USER
            PATH = claim_environ.PATH
            f = open(PATH+'tmp.txt', 'w')
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('Job ID', 'Queue', 'Job Name', 'Stutas', 'time').rstrip()
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('-'*15, '-'*8, '-'*25, '-'*5, '-'*6).rstrip()
            IDs = [ int(x) for x in message_box.keys() ]
            IDs.sort()
            IDs = [ str(x) for x in IDs]
            for i in IDs:
                print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                        .format(i, message_box[i].partition,
                                message_box[i].job_name, 'C',
                                message_box[i]._finish_time).rstrip()
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('-'*15, '-'*8, '-'*25, '-'*5, '-'*6).rstrip()
            f.close()
            for ID in terminal_id:
                cmd = sf.string_combine('write', USER, ID, '<', PATH+'tmp.txt')
                os.system(cmd)
            os.remove(PATH+'tmp.txt')
            return

        office = self._working_job_office
        if office._message_box:
            terminal_id = self.get_terminal()
            if terminal_id:
                # send message
                _send_msg(terminal_id, office._message_box)
                # empty JobOffice._message_box and _email_box
                self.del_msg_box()
                self.del_email_box()
                # print office
            else:
                # copy package to JobOffice._email_box
                for i in office._message_box.keys():
                    if office._message_box[i]._byemail is not True:
                        office.add_to_emailbox(office._message_box[i])
                        office._message_box[i]._byemail = True
        return

    def del_msg_box(self):
        """
        delete msg_box when the MessageMan send message successfully.

        Input: None
        Output: None
        """
        message_box = self._working_job_office._message_box
        for i in message_box.keys():
            del message_box[i]
        return

    def del_email_box(self):
        """
        delete emai_box when the MessageMan send message successfully.

        Input: None
        Output: None
        """
        email_box = self._working_job_office._email_box
        for i in email_box.keys():
            del email_box[i]
        return


class EmailMan():
    """
    This man will keep an eye on the JobOffice._email_box.
    When it is the case, he will send an email to the user.
    This man has be associated with a JobOffice.

    Note: this man will not work for the whole day, not like the
          MessageMan. He has his own work hours.
    """

    # the JobOffice for which EmailMan is working.
    _working_job_office = None
    # time to start work (in minutes):
    _start_time = config.EMAIL_START_TIME # 06:00
    # time to go back home (in minute):
    _end_time   = config.EMAIL_END_TIME # 23:59
    # time record when the EmailMan finds the JobOffice._email_box is
    # not empty at the first time. The EmailMan will hold for AN HOUR
    # to wait for more job packages thrown into JobOffice._email_box, then
    # start to send email.
    _hold_time = None # datetime.now()

    def __init__(self, JobOffice):
        self._working_job_office = JobOffice
    
    def check_email_box(self):
        """
        check email_box is empty or not.
        If email_box is not empty, record current time to self._hold_time.
        
        Intput: None
        Output: <type: bool>
        """
        if self._working_job_office._email_box:
            if self._hold_time == None: # initial time counting for holding time.
                self._hold_time = datetime.now()
            return True
        else:
            return False

    def check_hold_time(self):
        """
        check self._hold_time is greater than 1 hour or not.

        Input: None
        Output: <type: bool>
        """
        record = self._hold_time
        if record == None:
            return False
        holding_time = datetime.now() - record
        return (holding_time.second // 60) > config.EMAIL_HOLD_TIME

    def isworking(self):
        """
        Check if the EmailMan is at working period or not.

        Output: <type: bool>
        """
        # get current local time.
        get_time = datetime.now()
        time = get_time.hour*60 + get_time.minute
        return (self._start_time <= time <=  self._end_time)

    def del_email_box(self):
        """
        delete email_box when the EmailMan send email successfully.

        Input: None
        Output: None
        """
        email_box = self._working_job_office._email_box
        for i in email_box.keys():
            del email_box[i]
        return

    def send_email(self):
        """
        Send email requirement:
        - the JobOffice._email_box is not empty.
        - self._hold_time >= config.EMAIL_HOLD_TIME.
        - EmailMan himself is at the working period.
        when all the requirements are met, the EmailMan will start
        to send an Email to the user. Otherwise, he will do nothing.
        After the EmailMan send an Email successfully, he will empty
        the JobOffice._email_box and reset self._hold_time.

        Input: None
        Output: None
        """
        def _send_email(email_box):
            """
            real function for sending email.

            Input: <type: list> email_box. The same as JobOffice._email_box.
            Output: None 
            """
            USER = claim_environ.USER
            PATH = claim_environ.PATH
            USER_EMAIL = claim_environ.USER_EMAIL
            SERVER_EMAIL  = claim_environ.SERVER_EMAIL
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
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('Job ID', 'Queue', 'Job Name', 'Stutas', 'time').rstrip()
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('-'*15, '-'*8, '-'*25, '-'*5, '-'*6).rstrip()
            IDs = [ int(x) for x in email_box.keys() ]
            IDs.sort()
            IDs = [ str(x) for x in IDs]
            for i in IDs:
                print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                        .format(i, email_box[i].partition,
                                email_box[i].job_name, 'C',
                                email_box[i]._finish_time).rstrip()
            print >>f, "{:15s} {:8s} {:25s} {:5s} {:6s}"\
                    .format('-'*15, '-'*8, '-'*25, '-'*5, '-'*6).rstrip()
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
            msg['From'] = SERVER_EMAIL
            msg['To'] = USER_EMAIL
            s =  smtplib.SMTP('localhost')
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()
            os.remove(PATH+'tmp.txt')
            return

        if self.check_email_box():
            if self.check_hold_time() and self.isworking():
                email_box = self._working_job_office._email_box
                _send_email(email_box)
                self.del_email_box()
                self._hold_time = None
        return



if __name__ == "__main__":
    pass
