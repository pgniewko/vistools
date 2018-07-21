## DESCRIPTION ###
Visualize shells in a simulation box.

## USAGE ###

`./shellswire.py ../../assets/data/packing.xyz ../../assets/data/packing.top 1`

The first argument is XYZ coordinates, and the second argument is a topology file.
The thrid argument is a rendering style: 0 - all vertices the same color; 1 - vertex nodes with a degree equal to 6 are grey,
vertex nodes with a degree greater than 6 are red, whereas vertex nodes with a degree less than 6 are blue; 2 - render only surface.

The input files come from the [elasticshells](https://github.com/pgniewko/elasticshells).

![Shells](../../assets/img/shells.png)

COPYRIGHT NOTICE
================
Copyright (C) 2017-2018,  Pawel Gniewek  
Email  : gniewko.pablo@gmail.com  
All rights reserved.  
License: BSD

