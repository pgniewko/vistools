#! /bin/bash -x

cd `pwd`
IN_PATH=$1
OUT_PATH=$2

for i in `ls $IN_PATH/*.tga`; do 
    j=`basename $i .tga`
    sips -s format tiff $i --out $OUT_PATH/$j.tiff
done
