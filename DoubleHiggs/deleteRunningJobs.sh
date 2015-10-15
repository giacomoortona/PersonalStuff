#!/bin/bash

rm qdel.txt
qstat @llrt3 | grep ortona | grep -o [0-9][0-9][0-9][0-9][0-9][0-9].llrt3 >>qdel.txt
for i in $(cat qdel.txt); do echo $i; qdel $i ;done

