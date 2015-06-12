#!/bin/bash
if [[ "$1" == "jpsi" ]]; then
    X="PF"
    for X in PF Tight2012noIP Tight2012withIP ZZLoose Glb TMA; do
    for B in pt_abseta pt_abseta2; do
    #for B in pt_abseta; do
        for Y in 2012; do 
        #for Y in 2011 2012; do 
            YM=$(echo $Y | sed -e s/2011[AB]/2011/);
            root.exe -b -l -q TnP_JPsi_MuonID_data${Y}_${X}_${B}.root TnP_JPsi_MuonID_mc${YM}_${X}_${B}.root plotMuonID_JPsi_ZZ4L.cxx;
        done;
    done;
    done;
else
    #for Y in 2011; do 
    for Y in 2012; do 
    #for Y in 2011 2012; do 
        #for X in PFIso40_from_PF_and_SIP4 PFIso40DB_from_PF_and_SIP4 PFIso20DB_from_PF_and_SIP4; do
	for X in PFIso20_from_PF_and_SIP4 ; do
        #for X in PF_from_2011A PF_from_2011B; do
        #for X in SIP4_from_PF; do
        #for X in HLT_Mu17_from_PF_and_SIP4_and_PFIso40  HLT_Mu8_from_PF_and_SIP4_and_PFIso40; do
        #for X in HLT_Mu17_from_PF_and_SIP4_and_PFIso40_and_2011A  HLT_Mu8_from_PF_and_SIP4_and_PFIso40_and_2011A HLT_Mu17_from_PF_and_SIP4_and_PFIso40_and_2011B  HLT_Mu8_from_PF_and_SIP4_and_PFIso40_and_2011B; do
        #for X in HLT_OrMu17_from_PF_and_SIP4_and_PFIso40 HLT_OrMu8_from_PF_and_SIP4_and_PFIso40; do
        #for X in $(bash fitAll.sh echo_$Y | grep -v HLT); do
        #for X in $(bash fitAll.sh echo_$Y); do
            XM=$(echo $X | sed -e 's/_and_PostTS//' -e 's/_\(from\|and\)_2011[AB]//');
            for B in pt_abseta vtx eta; do
            #for B in eta; do
            #for B in eta2; do
            #for B in pt_abseta ; do
            #for B in pt_abseta2 ; do
                test -f TnP_MuonID_temporary2_data${Y}ABC_${X}_${B}.root || continue;
#		hadd TnP_MuonID_temporary2_data${Y}ABC_${X}_${B}.root TnP_MuonID_temporary2_data${Y}_${X}_${B}.root TnP_MuonID_temporary2_data${Y}C_${X}_${B}.root
                root.exe -b -l -q TnP_MuonID_temporary2_data${Y}ABC_${X}_${B}.root TnP_MuonID_temporary2_mc${Y}_weight_${X}_${B}.root plotMuonID_ZZ4L.cxx;
            done
        done
    done
fi
