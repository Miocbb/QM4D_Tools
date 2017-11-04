"""
configuration file.
"""

# When a job's running is equal or greater than this var,
# the job will be recorded for notification. Otherwise, the
# job will be ignored.
# <type: int>
RUNTIME_THRESHOLD = -1

# Time period in which the email is allow to be send to the user.
# Use 24-hours time format and then convert it to in minutes.
# <type: int>
# 06:00 to 23:59 is suggested.
EMAIL_START_TIME = 360  # 06:00
EMAIL_END_TIME   = 1439 # 23:59

# How long time should the sending email process hold, so that
# it can wait for more finished jobs to be sent at one time.
# 1 hour is suggested.
# <type: int> in minutes.
EMAIL_HOLD_TIME = -1
