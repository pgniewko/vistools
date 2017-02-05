#! /bin/bash -x


PREFIX=$1
FRAME_NUM=$2
NUM_PART=$3

VX=$((NUM_PART+1))
V1=$(($VX*$FRAME_NUM))
echo $V1

head -n $V1 $PREFIX.xyz >  $PREFIX.xyz.$FRAME_NUM.tmp

tail -n $((NUM_PART+1)) $PREFIX.xyz.$FRAME_NUM.tmp > $PREFIX".frame_"$FRAME_NUM".xyz.tmp"

if [ $? ]; then
    rm $PREFIX.xyz.$FRAME_NUM.tmp
fi


V1=$(($FRAME_NUM+0))
head -n $V1 $PREFIX.box.xyz >  $PREFIX.box.xyz.$FRAME_NUM.tmp
tail -n 1 $PREFIX.box.xyz.$FRAME_NUM.tmp >  $PREFIX."frame_"$FRAME_NUM".box.xyz"

if [ $? ]; then
    rm $PREFIX.box.xyz.$FRAME_NUM.tmp
fi

paste -d ' ' $PREFIX".frame_"$FRAME_NUM".xyz.tmp" $PREFIX."frame_"$FRAME_NUM".box.xyz" > $PREFIX".frame_"$FRAME_NUM".xyz"
if [ $? ]; then
    rm $PREFIX."frame_"$FRAME_NUM".box.xyz"
    rm $PREFIX".frame_"$FRAME_NUM".xyz.tmp"
fi


V1=$(($FRAME_NUM+1))
head -n $V1 $PREFIX.out >  $PREFIX.out.$FRAME_NUM.tmp
tail -n 1 $PREFIX.out.$FRAME_NUM.tmp >  $PREFIX."frame_"$FRAME_NUM".out"

if [ $? ]; then
    rm $PREFIX.out.$FRAME_NUM.tmp
fi

./fix_frame.py $PREFIX".top" $PREFIX".frame_"$FRAME_NUM".xyz" > $PREFIX".frame_"$FRAME_NUM".HR.xyz"
