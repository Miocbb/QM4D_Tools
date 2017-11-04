#!/usr/bin/python

import time
import source.claim_func as s_func
import source.claim_class as s_class
import source.claim_environ as s_environ



def main():
    print "Executable path: ", s_environ.PATH
    print "User: ", s_environ.USER
    print "User_email: ", s_environ.USER_EMAIL
    print "Sever_email: ", s_environ.MEI_EMAIL

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
