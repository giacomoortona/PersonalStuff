1) REMEMEBER TO SET THE CONFIG PARAMETERS BEFORE RUNNING!! 
The parameters are controlled by the fitMuonID.py and fitmuonjpsi.py files. You have to hack it to
change
- fit shape
- input filename  
- bin definitions (only definitions, what to use is defined afterwards)
PS 
it would be nice to let everything to be an option in the sh scripts, but
for now it's ok like this

2) Run the scripts
In these scripts you should configure the X variables list and the B (binning
list)

./fitAll.sh <scenario># produces the list of commands to submit for the Z fit
# <scenario> is data or mc (e.g. for 2012 it was "data2012" or "mc2012_weight") 
# Defines how to search for the filenames, so must be coherent with what is
# set in fitMuonId.py. ALWAYS APPEND "_weight" TO THE MC SCENARIOS!!!
 
./fitJPsi.sh # produces the list of commands to submit for the jpsi fit (vedi anche fitmuonid and fitmuonjpsi.py)

./plotAll.sh # makes all the plots

./plotCollage.sh #makes the combined jpsi/zmumu plots

