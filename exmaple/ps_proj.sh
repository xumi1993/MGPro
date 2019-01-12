#!/bin/bash
ps=magproj.eps
proj=mag_proj.dat

r=`gmt info -C $proj | awk '{print $1"/"$2"/"$3"/"$4}'`
gmt psbasemap -R$r -JX6i -Bafg -BWSne -K > $ps
gmt surface $proj -R -I1000/1000 -Gout.grd
gmt grd2cpt out.grd -Cjet -Z > tc1.cpt
gmt grdimage out.grd -Ctc1.cpt -R -J -O -K >> $ps
gmt psbasemap -R -J -O -K -Bg >> $ps

rm out.grd tc1.cpt gmt*
open $ps