#!/bin/bash

rm -rf magnetization
for i in {0..9}0
do
	grep mag $i/OSZICAR | awk '{print $10,$11,$12}' >> magnetization
done

for i in {0..9}0
do 
	grep SAXIS $i/INCAR | awk '{print $3,$4,$5}' >> magnetization
done
