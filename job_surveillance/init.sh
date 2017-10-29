# init bash script for starting jobs_surveillance

exe=${JOB_SVLN_PATH}
exe+="run.py"

# check if jobs_surveillance is running
run_status="False"
for i in $(ps aux | grep $JOB_SVLN_USER | awk '{print $NF}')
do
    if [ "$exe" == "$i" ]
    then
        run_status="True"
    fi
done

if [ "$run_status" == "False" ]
then
    session_on="False"
    # check is session is created by tmux
    for i in $(tmux ls | awk -F ":" '{print $1}')
    do
        if [ $i == "jobs_surveillance" ]
        then
            session_on="True"
        fi
    done

    if [ $session_on == "False" ]
    then
        echo "-------------------------------------------"
        echo "Notice: Start jobs_surveillance failed!"
        echo "Execute the following command to achieve."
        echo " "
        echo "tmux new -s jobs_surveillance"
        echo "-------------------------------------------"
    else
        tmux new -s jobs_surveillance
        python $exe &
        tmux detach
        echo "-------------------------------------------"
        echo "Notice: jobs_surveillance is on."
        echo " "
        echo "Turn off command: JOB_SVLN_KILL"
        echo "-------------------------------------------"
    fi
else
    # re-start the jobs_surveillance every time when user login.
    kill $(ps aux | grep "[p]ython ${JOB_SVLN_PATH}run.py" | awk '{print $2}')
    tmux new -s jobs_surveillance
    python $exe &
    tmux detach
    echo "-------------------------------------------"
    echo "Notice: jobs_surveillance is on."
    echo " "
    echo "Turn off command: JOB_SVLN_KILL"
    echo "-------------------------------------------"
fi
