#!/bin/bash

iostat -x -k 2 1

sys_name=$(iostat -x -k 2 1 | awk  '{print $1}' | head -1)


user_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $1}')
nice_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $2}')
system_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $3}')
iowait_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $4}')
steal_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $5}')
idle_val=$(iostat -c  | grep -v avg | grep '[^/s]' | grep -v $sys_name | awk  '{print $6}')

echo '================================================================================='
echo 'CPU situations: '

echo 'the percentage of CPU utilization that occurred while executing at the user level (application) :  ' $user_val
echo 'the percentage of CPU utilization that occurred while executing at the user level with nice priority : ' $nice_val
echo 'the percentage of CPU utilization that occurred while executing at the system level (kernel) : ' $system_val
echo 'the percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request :' $iowait_val
echo 'the percentage of time spent in involuntary wait by the virtual CPU or CPUs while the hypervisor was servicing another virtual processor : ' $steal_val
echo 'the percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request : ' $idle_val

echo ''

awk -v a=$idle_val 'BEGIN{b=0.1;if (a<b) print "Conclusion: CPU full"; else print "Conclusion: CPU not full"}'

echo ''

echo '================================================================================='
echo Devices situations:

i=1

Device_names=$(iostat -x -k 2 1  | grep -A 100 De | awk '{print $1}' | grep -v De)
for Device_name in $Device_names
do

let i++

echo '----------------------------------------------------------------------------------'
echo ''
echo Device name: $Device_name

Device_status=$(iostat -x -k 2 1 | grep -A 100 De | tail -n +$i | head -1)

rrqms=$(echo $Device_status | awk '{print $2}')
wrqms=$(echo $Device_status | awk '{print $3}')
rs=$(echo $Device_status | awk '{print $4}')
ws=$(echo $Device_status | awk '{print $5}')
rsec=$(echo $Device_status | awk '{print $6}')
wsec=$(echo $Device_status | awk '{print $7}')
avgrq=$(echo $Device_status | awk '{print $8}')
avgqu=$(echo $Device_status | awk '{print $9}')
await=$(echo $Device_status | awk '{print $10}')
rawait=$(echo $Device_status | awk '{print $11}')
wawait=$(echo $Device_status | awk '{print $12}')
util=$(echo $Device_status | awk '{print $14}')

echo 'The number of read requests merged per second that were queued to the device: ' $rrqms 
echo 'The number of write requests merged per second that were queued to the device: ' $wrqms
echo 'The number (after merges) of read requests completed per second for the device: ' $rs
echo 'The number (after merges) of write requests completed per second for the device: ' $ws
echo 'The number of sectors (kilobytes, megabytes) read from the device per second: ' $rsec
echo 'The number of sectors (kilobytes, megabytes) written to the device per second: ' $wsec
echo 'The average size (in sectors) of the requests that were issued to the device: ' $avgrq
echo 'The average queue length of the requests that were issued to the device: ' $avgqu
echo 'The average time (in milliseconds) for I/O requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them: ' $await
echo 'The average time (in milliseconds) for read requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them: ' $rawait
echo 'The average time (in milliseconds) for write requests issued to the device to be served. This includes the time spent by the requests in queue and the time spent servicing them: ' $wawait
echo 'Percentage of elapsed time during which I/O requests were issued to the device (bandwidth utilization for the device). Device saturation occurs when this value is close to  100% for devices serving requests serially.  But for devices serving requests in parallel, such as RAID arrays and modern SSDs, this number does not reflect their performance limits: ' $util

echo ''

awk -v a=$util 'BEGIN{b=99.5;if (a>b) print "Conclusion: this device is almost full"; else print "Conclusion: this device is not busy"}'

echo ''

done




