#!/bin/bash

region_list=('us-west-2.json' 'ap-south-1.json' 'ap-southeast-1.json' 'ap-northeast-1.json')
for region in ${region_list[@]}
do
	scp -P ** ******:~/AWS_SCRIPT/jsonfile/$region ./jsonfile/$region
done
