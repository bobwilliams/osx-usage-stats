#!/bin/bash
# script to get memory stats and log them to TurbineDB

# $2  = wired
# $4  = active
# $6  = inactive
# $8  = used
# $10 = free

while sleep 15; do
	MEM_WIRED=`top -l 1 | awk '/PhysMem/ {print $2}'`
	MEM_WIRED=${MEM_WIRED//M}

	MEM_ACTIVE=`top -l 1 | awk '/PhysMem/ {print $4}'`
	MEM_ACTIVE=${MEM_ACTIVE//M}

	MEM_INACTIVE=`top -l 1 | awk '/PhysMem/ {print $6}'`
	MEM_INACTIVE=${MEM_INACTIVE//M}

	MEM_USED=`top -l 1 | awk '/PhysMem/ {print $8}'`
	MEM_USED=${MEM_USED//M}

	MEM_FREE=`top -l 1 | awk '/PhysMem/ {print $10}'`
	MEM_FREE=${MEM_FREE//M}

	POST_DATA_INIT="'"
	POST_DATA_BEGIN='{"timestamp":'
	POST_DATA_TIMESTAMP=$((`date +%s` * 1000)) 
	POST_DATA_MIDDLE=', "data": {'

	POST_DATA_MEM_WIRED='"MEM_WIRED":'$MEM_WIRED
	POST_DATA_MEM_ACTIVE=', "MEM_ACTIVE":'$MEM_ACTIVE
	POST_DATA_MEM_INACTIVE=', "MEM_INACTIVE":'$MEM_INACTIVE
	POST_DATA_MEM_USED=', "MEM_USED":'$MEM_USED
	POST_DATA_MEM_FREE=', "MEM_FREE":'$MEM_FREE

	POST_DATA_END="}}'"

	DATA=$POST_DATA_INIT$POST_DATA_BEGIN$POST_DATA_TIMESTAMP$POST_DATA_MIDDLE$POST_DATA_MEM_WIRED$POST_DATA_MEM_ACTIVE$POST_DATA_MEM_INACTIVE$POST_DATA_MEM_USED$POST_DATA_MEM_FREE$POST_DATA_END

	echo
	echo $DATA

	eval curl -X POST http://localhost:8080/db/macbookair/memory -d $DATA
done