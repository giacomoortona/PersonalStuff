from ROOT import *
import os,re

#lambdas = [1.0,0.5,0.9,0.95,1.03,1.05,1.1,1.5]
#lambdas = [1.0,0.5,0.9,0.95,0.96,0.97,0.98,0.99,1.01,1.02,1.03,1.04,1.05,1.1,1.5]
lambdas = [1.0,0.9,0.95,0.96,0.97,0.98,0.99,1.01,1.02,1.03,1.04,1.05,1.1]
lambaboos = [1.0,0.5,0.9,0.95,1.05,1.1,1.5]

for klambda in lambdas :
	print klambda
	inFile = TFile.Open("hhbbaa/root_HH_kappa_l_{0:.2f}/histos.root".format(klambda))
	if not inFile : 
		continue
	else : print "found"
	outFile = TFile.Open("hhbbaa/root_HH_kappa_l_{0:.2f}/shapes.root".format(klambda),"RECREATE")
	for entry in inFile.GetListOfKeys() :
		#inFile.GetListOfKeys().Print() 
		#entry.Print()
		oldName = entry.GetName()
		outObj = inFile.Get(oldName)
		newName = oldName.replace('(#kappa_{l}=',"") #
		newName = newName.replace("{0:.2f})".format(klambda),"")
		newName = newName.replace("j#gamma + Jets","jgjj")
		newName = newName.replace("#gamma#gamma + Jets","ggjj")
		outObj.SetName(newName)
		outObj.SetTitle(newName)
		outFile.cd()
		outObj.Write()
	
	processes = ["jgjj","ggjj","ttH"]	
	
	for sel in range(0,11) : 
		for tipo in ["maa_mhh","maa_mbb","h_m","aa_m"] :
			if klambda ==1 : obs = inFile.Get("HH_sel{0}_h{1}".format(sel,tipo)).Clone("data_obs")
			else :
				fileone = TFile.Open("hhbbaa/root_HH_kappa_l_{0:.2f}/shapes.root".format(1.0))
				obs = fileone.Get("HH_sel{0}_h{1}".format(sel,tipo)).Clone("data_obs")
			for iproc in processes :
				#print "{2}_sel{0}_h{1}".format(sel,tipo,iproc)
				#outFile.Get("{2}_sel{0}_h{1}".format(sel,tipo,iproc)).Print()
				obs.Add(outFile.Get("{2}_sel{0}_h{1}".format(sel,tipo,iproc)))
			obs.SetName("data_obs_sel{0}_h{1}".format(sel,tipo))
			obs.SetTitle("data_obs_sel{0}_h{1}".format(sel,tipo))
			outFile.cd()
			obs.Write()
	outFile.Close()

for klambda in lambaboos :
	print klambda
	inFile = TFile.Open("hh_boosted/root_HH_kappa_l_{0:.2f}/histos.root".format(klambda))
	if not inFile : 
		continue
	else : print "found"
	outFile = TFile.Open("hh_boosted/root_HH_kappa_l_{0:.2f}/shapes.root".format(klambda),"RECREATE")
	for entry in inFile.GetListOfKeys() :
		#inFile.GetListOfKeys().Print() 
		#entry.Print()
		oldName = entry.GetName()
		outObj = inFile.Get(oldName)
		newName = oldName.replace('(#kappa_{l}=',"") #
		newName = newName.replace("{0:.2f})".format(klambda),"")
		#newName = newName.replace("j#gamma + Jets","jgjj")
		#newName = newName.replace("#gamma#gamma + Jets","ggjj")
		outObj.SetName(newName)
		outObj.SetTitle(newName)
		outFile.cd()
		outObj.Write()
	
	processes = ["QCD"]	
	
	for sel in range(0,13) : 
		for tipo in ["mbb_mbb","h_m"] :
			if klambda ==1 : obs = inFile.Get("HH_sel{0}_h{1}".format(sel,tipo)).Clone("data_obs")
			else :
				fileone = TFile.Open("hh_boosted/root_HH_kappa_l_{0:.2f}/shapes.root".format(1.0))
				obs = fileone.Get("HH_sel{0}_h{1}".format(sel,tipo)).Clone("data_obs")
			for iproc in processes :
				#print "{2}_sel{0}_h{1}".format(sel,tipo,iproc)
				#outFile.Get("{2}_sel{0}_h{1}".format(sel,tipo,iproc)).Print()
				obs.Add(outFile.Get("{2}_sel{0}_h{1}".format(sel,tipo,iproc)))
			obs.SetName("data_obs_sel{0}_h{1}".format(sel,tipo))
			obs.SetTitle("data_obs_sel{0}_h{1}".format(sel,tipo))
			outFile.cd()
			obs.Write()
	outFile.Close()

