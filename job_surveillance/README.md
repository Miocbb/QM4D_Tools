# Description:
This program is designed to monitor the status of submitted jobs on a server, and it will automatically notify the user when there are jobs finished, by writing a message on the screen or sending an email.

This program is based on serveral external programs which are normally installed on linux system. In particular, `qstat` is the main external program used to gather jobs' information.

External program list:
* `python 2.7`
* `tmux`
* `write`
* `qstat`
* `who`

# Usage:
* clone this project to any place you like.
* Add following lines into your `.bashrc` or `.zshrc` and set up each variable based on your own case.

```shell
#{{{ jobs_surveillance
# root path for job_surveillance file
export JOB_SVLN_PATH="root_path"
# user name of jobs
export JOB_SVLN_USER="user_name"
# contact email of user
export JOB_SVLN_USER_EMAIL="user_email"
# set your own email of sending side
export JOB_SVLN_SERVER_EMAIL="jobs_surveillance_email"
# alias for turn off jobs_surveillance
alias JOB_SVLN_KILL="kill \$(ps aux | grep \"[p]ython \${JOB_SVLN_PATH}run.py\" | awk '{print \$2}')"

exe=$JOB_SVLN_PATH
exe+="init.sh"
bash $exe
#}}}
```
* To change configuration, navigate to `/root_path/source/config.py`. To make changes effective, you have to manually kill this running process at first, `JOB_SVLN_KILL`, then re-login.
