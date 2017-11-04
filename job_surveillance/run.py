#!/usr/bin/python

import time
import source.claim_func as s_func
import source.claim_class as s_class
import source.claim_environ as s_environ
import source.config as s_config



def main():
    print "Executable path: ", s_environ.PATH
    print "User: ", s_environ.USER
    print "User_email: ", s_environ.USER_EMAIL
    print "Sever_email: ", s_environ.SERVER_EMAIL
    print "Runtime_threshold: %d minutes" %s_config.RUNTIME_THRESHOLD
    start = s_config.EMAIL_START_TIME
    end   = s_config.EMAIL_END_TIME
    print "Email sending peirod: {:02d}:{:02d} - {:02d}:{:02d}"\
            .format(start/60, start%60, end/60, end%60)
    print "Email_hold_time: {} minutes".format(s_config.EMAIL_HOLD_TIME)

    joboffice = s_class.JobOffice()
    collector = s_class.CollectMan(joboffice)
    messager  = s_class.MessageMan(joboffice)
    emailer   = s_class.EmailMan(joboffice)
    while True:
        time.sleep(1)
        collector.collect()
        messager.send_msg()
        emailer.send_email()


if __name__ == "__main__":
    main()
