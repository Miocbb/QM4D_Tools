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
        echo "Attention: jobs_surveillance is on."
        if [ $(($JOB_SVLN_INTERVAL / 60)) -ne 0 ];then
            echo "           check jobs every" $(($JOB_SVLN_INTERVAL / 60)) min $(($JOB_SVLN_INTERVAL % 60)) sec.
        else
            echo "           check jobs every" $(($JOB_SVLN_INTERVAL % 60)) sec.
        fi
        echo " "
        echo "Turn-off:  JOB_SVLN_KILL"
        echo "-------------------------------------------"
    fi
else
    echo "-------------------------------------------"
    echo "Attention: jobs_surveillance is on."
    if [ $(($JOB_SVLN_INTERVAL / 60)) -ne 0 ];then
        echo "           check jobs every" $(($JOB_SVLN_INTERVAL / 60)) min $(($JOB_SVLN_INTERVAL % 60)) sec.
    else
        echo "           check jobs every" $(($JOB_SVLN_INTERVAL % 60)) sec.
    fi
    echo " "
    echo "Turn-off:  JOB_SVLN_KILL"
    echo "-------------------------------------------"
fi
