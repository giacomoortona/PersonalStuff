#! /usr/bin/env python

# This macro modify the cards of the different channels that go in the  
# combinationin order to uniformize naming conventions, apply proper 
# cross-sections and other small tweaks. It should be run on the combined
# card of each individual channel.
# Author: G. Ortona (LLR)

import sys, pwd, commands, optparse
import os
import re
import math
import string
from ROOT import *
import ROOT

## bbbb: OK, need to upate files from SVN
## bbWW: OK
## bbtt: missing TES, btag (vedere se e il solo a usare l/f)
## bbgg: vedi sotto

#Channels: bbtt, bbww, bbgg,bbbb
#files: 
#theory flag not implemented yet

def parseOptions():

    usage = ('usage: %prog [options] datasetList\n'
             + '%prog -h for help')
    parser = optparse.OptionParser(usage)
    
    parser.add_option('-c', '--channel',   dest='channel', type='string', default='MuTau',  help='final state')
    parser.add_option('-i', '--inputFile',   dest='inputFile', type='string', default='',  help='input card')
    parser.add_option('-l', '--lambda', dest='overLambda', type=int, default=1, help='for lambda scan. 1=SM, >100 = resonant')
    parser.add_option('-t', '--theory',  action="store_true", dest='theory', help='add theory systematics')
    parser.add_option('-b', '--cleanHist',  action="store_true", dest='cleanHist', help='clean bbbb histo names as well')
    parser.add_option('-o', '--outDir',  dest="outDir", type='string', default='', help='outDir')
    parser.add_option('-g', '--graviton',  dest="graviton", action='store_true', default=False, help='switch to graviton instead of Radion')
    parser.add_option('-p', '--projection',  dest="projection", type=float, default=-1, help='lumi to which project')

    # store options and arguments as global variables
    global opt, args
    (opt, args) = parser.parse_args()
    global lambdaName

def comments():
	print "==== COMMENTS/TO DO LIST ====" 
	print "this to do list is print every time the macro is run"
	print "please update the list if you change the input cards"
	print "*Common*"
	print "Check MC x-section uncertainties"
	print "check finite top mass (for sure bbgg, bbtt have it)"
	print "check JER naming and JES naming. JES->bbtt, bbVV split (or will split). bbbb do not (at the moment). bbgg is a mess"
	print "      JER bbww,bbbb have it and correlate it. bbgg is a mess"
	print "*bbtt*"
	print ". Should separate btag"
	print "*bbgg*"
	print ". check theory uncertainties and make them compatible"
	print ". verify theory against QCDscale_ggHH -> replace and fix number"
	print ". Should separate JES/JER??"
	print "*bbbb*"
	print ". JES splitting"
	print "*bbWW*"
	print "============================="
	print ""

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def GetBenchmarkPoint(nb) :
	if nb == 10 : return "CombinedCard_ARW_kl_10p0_kt_1p5_cg_0p0_c2_m1p0_c2g_0p0"
	elif nb == 12 : return "CombinedCard_ARW_kl_15p0_kt_1p0_cg_0p0_c2_1p0_c2g_0p0"
	elif nb == 8 : return "CombinedCard_ARW_kl_15p0_kt_1p0_cg_m1p0_c2_0p0_c2g_1p0"
	elif nb == 3 : return "CombinedCard_ARW_kl_1p0_kt_1p0_cg_0p0_c2_m1p5_c2g_m0p8"
	elif nb == 5 : return "CombinedCard_ARW_kl_1p0_kt_1p0_cg_0p8_c2_0p0_c2g_m1p0"
	elif nb == 9 : return "CombinedCard_ARW_kl_1p0_kt_1p0_cg_m0p6_c2_1p0_c2g_0p6"
	elif nb == 2 : return "CombinedCard_ARW_kl_1p0_kt_1p0_cg_m0p8_c2_0p5_c2g_0p6"
	elif nb == 6 : return "CombinedCard_ARW_kl_2p4_kt_1p0_cg_0p2_c2_0p0_c2g_m0p2"
	elif nb == 11 : return "CombinedCard_ARW_kl_2p4_kt_1p0_cg_1p0_c2_0p0_c2g_m1p0"
	elif nb == 7 : return "CombinedCard_ARW_kl_5p0_kt_1p0_cg_0p2_c2_0p0_c2g_m0p2"
	elif nb == 1 : return "CombinedCard_ARW_kl_7p5_kt_1p0_cg_0p0_c2_m1p0_c2g_0p0"
	elif nb == 4 : return "CombinedCard_ARW_kl_m3p5_kt_1p5_cg_0p0_c2_m3p0_c2g_0p0"

def bbttCleaner(inFile,outfile):
	for line in inFile :
		outLine = line
		if "input.root" in line : outLine =line.replace("input.root","input2.root") #new files with normalized JES shape fatto prima in redobbtt
		if "MASS" in line :  
			if opt.overLambda < -100 : outLine =line.replace("$MASS",str(-1*opt.overLambda-100))
			elif opt.overLambda < 100 : outLine =line.replace("$MASS",str(20+opt.overLambda)) #This is true only for the SM
		if "CMS_eff_btag" in line : outLine =line.replace("CMS_eff_btag","CMS_eff_b_heavy")
		if "QCDscale_tw" in line : outLine =line.replace("QCDscale_tw","QCDscale_SingleTop") #Maybe better to change in bbWW
		if "QCDscale_tt" in line : outLine =line.replace("QCDscale_tt ","ttbar_xsec")#"QCDscale_ttbar")#"ttbar_xsec") #Maybe better to change in bbWW, QCDscale_ttbar
		if "QCDscale_ZH" in line : outLine =line.replace("QCDscale_ZH","QCDscale_SMHiggs") #TBU QCDscale_VH
		if "pdf_ggHH" in line : outLine =line.replace("pdf_ggHH","pdf") 
		if "CMS2016_eff_b" in line : outLine = line.replace("CMS2016_eff_b","CMS_eff_btag")
		outfile.write(outLine)
	if opt.overLambda <100 :
		outfile.write("hh_bbtt_deconv rateParam * ggHH_bbtt 0.0024477\n") # sigma*BR*1pb
		outfile.write("nuisance edit freeze hh_bbtt_deconv\n")
	if opt.overLambda >100  and opt.overLambda < 920:
		if not opt.graviton : outfile.write("hh_bbtt_deconv rateParam * Radion 0.000072682208\n") # BR*1pb -> 7.3/100 *1/1000 fb ->0.073/1000
		else : outfile.write("hh_bbtt_deconv rateParam * Graviton 0.000072682208\n") # BR*1pb -> 7.3/100 *1/1000 fb ->0.073/1000
		outfile.write("nuisance edit freeze hh_bbtt_deconv\n") 
	if opt.overLambda >920 :
		if opt.graviton : outfile.write("hh_bbtt_deconv rateParam * XHH2_M* 0.000072682208\n") # BR*1pb -> 7.3/100 *1/1000 fb ->0.073/1000
		else : outfile.write("hh_bbtt_deconv rateParam * XHH_M* 0.000072682208\n") # BR*1pb -> 7.3/100 *1/1000 fb ->0.073/1000
		outfile.write("nuisance edit freeze hh_bbtt_deconv\n") 

def bbwwCleaner(inFile,outfile):
	procNameLine = False
	numberProc = []
	for line in inFile :
		outLine = line
		if "kmax" in line and not "*" in line: 
			words = line.split()
			outLine = "kmax {0}\n".format(int(words[1])+2) #Adding the 2 BR uncertainties
		if "lumi_13TeV_2016" in line : outLine =line.replace("lumi_13TeV_2016","lumi_13TeV") 
                #if "QCDscale_ttbar" in line : outLine =line.replace("QCDscale_ttbar","ttbar_xsec") #Maybe better to change in bbWW, QCDscale_ttbar
		#if "CMS_eff_b_heavy" in line : outLine =line.replace("CMS_eff_b_heavy","CMS_eff_b") #finche gli altri non aggiustano il loro 
		if "process" in line :
			words = line.split()
			if words[0] == "process" and not procNameLine : procNameLine = True
			if words[0] == "process" and procNameLine :
				words.pop(0)
				numberProc = words
		#if "QCDscale_ZH" in line : outLine =line.replace("QCDscale_ZH","QCDscale_SMHiggs") #TBU -> shape in bbww, easier like this
		outfile.write(outLine)
	outfile.write("  \n")
	outLineBr = "HH_BR_Hbb lnN "
	for adder in range(len(numberProc)) :
		if int(numberProc[adder]) <= 0 : outLineBr += " 1.012/0.987 "
		else : outLineBr += " - "
	outLineBr += " \n"
	outfile.write(outLineBr)
	outLineBr = "HH_BR_HWW lnN "
	for adder in range(len(numberProc)) :
		if int(numberProc[adder]) <= 0 : outLineBr += " 1.015 "
		else : outLineBr += " - "
	outLineBr += " \n"
	outfile.write(outLineBr)

	if opt.overLambda < 100:
		outfile.write("hh_bbWW_deconv rateParam * ggHH 0.911\n")
		outfile.write("nuisance edit freeze hh_bbWW_deconv\n") 
	if opt.overLambda > 100:
		if opt.graviton : outfile.write("hh_bbWW_deconv rateParam * ggX2HH 0.0272\n")
		else : outfile.write("hh_bbWW_deconv rateParam * ggX0HH 0.0272\n")
		outfile.write("nuisance edit freeze hh_bbWW_deconv\n") 

def bbggCleaner(inFile,outfile):
	procNameLine = False
	numberProc = []
	for line in inFile :
		outLine = line
		if "kmax" in line and not "*" in line: 
			words = line.split()
			outLine = "kmax {0}\n".format(int(words[1])+2) #Adding the 2 BR uncertainties
		if "process" in line :
			words = line.split()
			if words[0] == "process" and not procNameLine : procNameLine = True
			if words[0] == "process" and procNameLine :
				words.pop(0)
				numberProc = words

		if "lumi_13TeV" in line : outLine =line.replace("1.027","1.025") 
		if "PDF_as" in line : outLine =line.replace("PDF_as","pdf")
		if "CMS_eff_cats" in line : outLine = line.replace("CMS_eff_cats","CMS_eff_b_heavy") #not present in new btagged cards
		if "QCDscale_vh" in line : outLine =line.replace("QCDscale_vh","QCDscale_SMHiggs") #TBU
		if "shapes" in line and ("rateixei" in line or "Btag" in line):
			if "May8" in line : outLine = line.replace("/afs/cern.ch/work/r/rateixei/work/DiHiggs/bbggLimits_May8/CMSSW_7_4_7/src/HiggsAnalysis/bbggLimits/./","bbggWS/LIMS_NOscale/")
			elif "Goodbye" in line : 
				#print "tochange"
				outLine = line.replace("/afs/cern.ch/work/r/rateixei/work/DiHiggs/bbggLimits_Goodbye/CMSSW_7_4_7/src/HiggsAnalysis/bbggLimits/.","bbggWS/LIMS_NOscale")
			elif "BtagAntiCorr" in line :
				outLine = line.replace("./LIMS_BtagAntiCorr/","/afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_BtagAntiCorr/") #"/afs/cern.ch/work/r/rateixei/work/DiHiggs/bbggLimits_Goodbye/CMSSW_7_4_7/src/HiggsAnalysis/bbggLimits/.","bbggWS/LIMS_NOscale")
		if "CombiFinal" in line: 
			outLine = line.replace("./LIMS_CombiFinal/","/afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_CombiFinal/") 
		if "LIMS_FinalRun" in line :
			outLine = line.replace("/afs/cern.ch/work/a/andrey/hh/LimitCode/CMSSW_7_4_7/src/HiggsAnalysis/bbggLimits/","") #
			outLine = outLine.replace("./LIMS_FinalRun","cadi/HIG-17-008/LIMS_FinalRun") 
		#Questi Andrey dovrebbe averli messi a posto, ma solo in klambda=1
		if "CMS_hgg_sig_m0_absShift_cat3" in line : outLine = "CMS_hgg_sig_m0_absShift_cat3 param  1 0.005\n"
		if "CMS_hgg_sig_m0_absShift_cat2" in line : outLine = "CMS_hgg_sig_m0_absShift_cat2 param  1 0.005\n"
		if "CMS_hgg_sig_m0_absShift_cat1" in line : outLine = "CMS_hgg_sig_m0_absShift_cat1 param  1 0.005\n"
		if "CMS_hgg_sig_m0_absShift_cat0" in line : outLine = "CMS_hgg_sig_m0_absShift_cat0 param  1 0.005\n"
		if "CMS_hgg_sig_sigmaScale_cat3" in line : outLine = "CMS_hgg_sig_sigmaScale_cat3 param  1 0.05\n"
		if "CMS_hgg_sig_sigmaScale_cat2" in line : outLine = "CMS_hgg_sig_sigmaScale_cat2 param  1 0.05\n"
		if "CMS_hgg_sig_sigmaScale_cat1" in line : outLine = "CMS_hgg_sig_sigmaScale_cat1 param  1 0.05\n"
		if "CMS_hgg_sig_sigmaScale_cat0" in line : outLine = "CMS_hgg_sig_sigmaScale_cat0 param  1 0.05\n"
		if opt.overLambda != 1:
			if "shapes" in line and "Benchmarks" in line:
				if "cat0" in line :
					if "hhbbgg.ggh.inputhig.root" in line:
						outLine = "shapes ggh ch2_cat0 hhbbgg.ggh.inputhig.root w_all:CMS_hig_ggh_cat0\n"
						#print "CHANGED!"
					elif "hhbbgg.vbf.inputhig.root" in line:
						outLine = "shapes vbf ch2_cat0 hhbbgg.vbf.inputhig.root w_all:CMS_hig_vbf_cat0\n"
						#print "CHANGED VBF 0"
				elif "cat1" in line:
					if "hhbbgg.ggh.inputhig.root" in line:
						outLine = "shapes ggh ch2_cat1 hhbbgg.ggh.inputhig.root w_all:CMS_hig_ggh_cat1\n"
						#print "CHANGED! 1"
					elif "hhbbgg.vbf.inputhig.root" in line:
						outLine = "shapes vbf ch2_cat1 hhbbgg.vbf.inputhig.root w_all:CMS_hig_vbf_cat1\n"
		outfile.write(outLine)
	outLineBr = "HH_BR_Hbb lnN "
	for adder in range(len(numberProc)) :
		if int(numberProc[adder]) <= 0 : outLineBr += " 1.012/0.987 "
		else : outLineBr += " - "
	outLineBr += " \n"
	outfile.write(outLineBr)
	outLineBr = "HH_BR_Hgg lnN "
	for adder in range(len(numberProc)) :
		if int(numberProc[adder]) <= 0 : outLineBr += " 1.0206/0.9792 "
		else : outLineBr += " - "
	outLineBr += " \n"
	outfile.write(outLineBr)

	if opt.overLambda < 100 :
		outLineBr = "QCDscale_ggHH lnN "
		for adder in range(len(numberProc)) :
			if int(numberProc[adder]) <= 0 : outLineBr += " 1.043/0.940 "
			else : outLineBr += " - "
		outLineBr += " \n"
		outfile.write(outLineBr)
		outfile.write("hh_bbgg_deconv rateParam * Sig 0.087\n")
		outfile.write("nuisance edit freeze hh_bbgg_deconv\n")
	elif opt.overLambda > 100 :
		outfile.write("hh_bbgg_deconv rateParam * Sig 0.00262\n")
		outfile.write("nuisance edit freeze hh_bbgg_deconv\n")

def bbbbCleaner(inFile,outfile,bbbbPath):
	procNameLine = True
	isB2G = False
	numberProc = []
	lastLine = "" #this is for a weird shapeN2 issue
	for line in inFile :
		if "B2G" in line : isB2G = True
		outLine = line
		#Non-resonant
		if "kmax" in line and not "*" in line: 
			words = line.split()
			outLine = "kmax {0}\n".format(int(words[1])+1) #Adding the H->bb BR uncertainty
		if "process" in line :
			words = line.split()
			#if words[0] == "process" and not procNameLine : procNameLine = True
			if words[0] == "process" and RepresentsInt(words[1]) :
				words.pop(0)
				numberProc = words

		if opt.overLambda < 100:
			if "CMS_eff_trig" in line: 
				lastLine = line.replace("shapeN2","shape")
				continue
			#if "hists_ggHHbbbb-nonRes_sum-20170502-234140.root" in line : outLine =line.replace("hists_ggHHbbbb-nonRes_sum-20170502-234140.root","hh_bbbb_hist.root")
			if "shapes" in line:
				if "B2G" in line:
					if "Giacomo" in line : outLine = line.replace("outputs/datacards/forGiacomo/","")
					else : outLine = line.replace("outputs/datacards/","")
				else: 
					outLine = "shapes  *       *       hh_bbbb_hist_"+str(opt.overLambda)+".root $PROCESS        $PROCESS_$SYSTEMATIC \n"
				#print "CHANGED!"
			#if "shapes " in line  and opt.overLambda != 1: outLine = "shapes  *       *       hh_bbbb_hist_"+str(opt.overLambda)+".root $PROCESS        $PROCESS_$SYSTEMATIC"
			if "CMS_scale_j" in line : outLine = line.replace("CMS_scale_j","CMS_scale_j_13TeV")
			#if "CMS_eff_b_lf" in line : outLine = line.replace("CMS_eff_b_lf","CMS_eff_b_light")
			#if "CMS_eff_b_hf" in line : outLine = line.replace("CMS_eff_b_hf","CMS_eff_b_heavy")
			if "CMS_eff_b" in line : outLine = line.replace("CMS_eff_b","CMS_btag")
			if "CMS_eff_bbtag_sf" in line : outLine = line.replace("CMS_eff_bbtag_sf","CMS_eff_btag")
			if "CMS_pileup" in line : outLine = line.replace("CMS_pileup","CMS_pu")
			if "pdf_HH_gg" in line : outLine = line.replace("pdf_HH_gg","pdf")
			if isB2G :
				if "process" in line :  
					#outLine = line.replace("ggHH_hbbhbb","Signal")
					outLine = line.replace("ggHH_hbbhbb_mX_"+str(-1*opt.overLambda-100)+"_HH","Signal_mX_"+str(-1*opt.overLambda-100)+"_HH")
					#outLine = outLine.replace("QCDEST","EST")

		else :
			#Resonant
			if "shapes" in line and opt.overLambda <= 1200 : 
				outLine = line.replace("w_",bbbbPath+"w_")
			if "shapes " in line and opt.overLambda > 1200 :
				outLine = line.replace("outputs/datacards/",bbbbPath) #cadi/B2G-16-026/AABH/outputs/datacards/
			if "bTag" in line : outLine = line.replace("bTag","CMS_btag")
			if "lumi" in line and not "TeV" in line : outLine = line.replace("lumi","lumi_13TeV")
			if "JEC" in line : outLine = line.replace("JEC","CMS_scale_j_13TeV")
			if "JER" in line : outLine = line.replace("JER","CMS_res_j")
			if "CMS_PDF_Scales" in line : outLine = line.replace("CMS_PDF_Scales","pdf")
			if "trigger" in line : outLine = line.replace("trigger","triggerbbbb")
			if "CMS_PU" in line : outLine = line.replace("CMS_PU","CMS_pu")
			if "CMS_eff_tau21_sf" in line : outLine = line.replace("CMS_eff_tau21_sf","CMS_eff_t")

		outfile.write(outLine)
	outfile.write(lastLine)
	outLineBr = "HH_BR_Hbb lnN "
	for adder in range(len(numberProc)) :
		if int(numberProc[adder]) <= 0 : outLineBr += " 1.024/0.974 "
		else : outLineBr += " - "
	outLineBr += " \n"
	outfile.write(outLineBr)

	if opt.overLambda < 100:
		outLineBr = "QCDscale_ggHH lnN "
		for adder in range(len(numberProc)) :
			if int(numberProc[adder]) <= 0 : outLineBr += " 1.043/0.940 "
			else : outLineBr += " - "
		outLineBr += " \n"
		outfile.write(outLineBr)

		outfile.write("hh_bbbb_deconv rateParam * ggh_hh_bbbb 11.37\n") 
		outfile.write("nuisance edit freeze hh_bbbb_deconv\n")
		#if opt.overLambda == 1:
		#	fileHists = TFile.Open("hists_Training0_kl_1_kt_1.root")
		#else : fileHists = TFile.Open("cadi/HIG-17-017/BSMscan/hists_Training0_kl_"+str(opt.overLambda)+"_kt_1.root")
		fileHists = TFile.Open(bbbbPath)
		newFH = TFile.Open(opt.outDir+"hh_bbbb_hist_"+str(opt.overLambda)+".root","RECREATE")
		     
		listReplacebbbb = ["CMS_scale_j","CMS_eff_b_jes","CMS_eff_b_lf" ,"CMS_eff_b_hf" ,"CMS_eff_b_lfstats1","CMS_eff_b_lfstats2","CMS_eff_b_hfstats1","CMS_eff_b_hfstats2","CMS_eff_b_cferr1","CMS_eff_b_cferr2","CMS_pileup"]
		listOutbbbb = ["CMS_scale_j_13TeV","CMS_btag_jes","CMS_btag_lf" ,"CMS_btag_hf" ,"CMS_btag_lfstats1","CMS_btag_lfstats2","CMS_btag_hfstats1","CMS_btag_hfstats2","CMS_btag_cferr1","CMS_btag_cferr2","CMS_pu"]
		for item in fileHists.GetListOfKeys() :
			iname = item.GetName()
			obj = fileHists.Get(iname)
			#if not "TH" in obj.ClassName():
			#	print obj.Class()
			#	continue
			for sub in range(len(listReplacebbbb)):
				if listReplacebbbb[sub] in iname :
					oldName  = item.GetName()
					newName = oldName.replace(listReplacebbbb[sub],listOutbbbb[sub])
					#newName = listOutbbbb[sub]
					obj.SetName(newName)
					obj.SetTitle(newName)
			newFH.cd()
			obj.Write()
		newFH.Close()
	elif opt.overLambda <= 550:
		outfile.write("hh_bbbb_deconv rateParam * signal 0.00033918976 \n")  #1pb
		outfile.write("nuisance edit freeze hh_bbbb_deconv\n")
	elif opt.overLambda <= 1200 :
		outfile.write("hh_bbbb_deconv rateParam * signal 0.16959488 \n") #Move to 2fb in MMR
		outfile.write("nuisance edit freeze hh_bbbb_deconv\n")
	else :
		outfile.write("hh_bbbb_deconv rateParam * Signal* 0.033918976 \n") #Move to 10fb in HMR
		outfile.write("nuisance edit freeze hh_bbbb_deconv\n")


parseOptions()
comments()
if opt.outDir is not "" : opt.outDir += "/"

#if opt.overLambda == 1 :
#	destName = "{1}hh_{0}_comb.txt".format(opt.channel,opt.outDir)
#else : destName = "{2}hh_{0}_comb_{1}.txt".format(opt.channel,opt.overLambda,opt.outDir)
if opt.graviton :destName = "{2}hh_{0}_combGraviton_{1}.txt".format(opt.channel,opt.overLambda,opt.outDir)
else : destName = "{2}hh_{0}_comb_{1}.txt".format(opt.channel,opt.overLambda,opt.outDir)

listFiles = {}
bbbbPath = "" 
#if opt.overLambda == 1 :
#bbgg = /afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_CombiFinal/
#	listFiles['bbtt'] = "datacard_bbtt_1.txt"
#	listFiles['bbww'] = "datacard_bbww_1.txt"
#	#listFiles['bbgg'] = "Combi/CombinedCard_ARW_kl_1p0_kt_1p0_cg_0p0_c2_0p0_c2g_0p0/hhbbgg_13TeV_DataCard.txt" #"SM_hhbbgg_13TeV_DataCard_forCombination.txt"
#	listFiles['bbgg'] = "/afs/cern.ch/user/a/andrey/public/HH/Combi_24Jan2018/LIMS_BtagAntiCorr/CombinedCard_ARW_/hhbbgg_13TeV_DataCard.txt" #"SM_hhbbgg_13TeV_DataCard_forCombination.txt"
gravitonString = "" 
if opt.graviton : gravitonString = "Graviton"
listFiles['bbtt'] = "datacard_bbtt"+gravitonString+"_"+str(opt.overLambda)+".txt"
listFiles['bbww'] = "datacard_bbww"+gravitonString+"_"+str(opt.overLambda)+".txt"
if opt.overLambda <= -100 :
	#benchmarks
	#non ho ancora i benchmarks bbgg, uso SM instead
	#print GetBenchmarkPoint(-1*opt.overLambda-100), -1*opt.overLambda-100
	#listFiles['bbgg'] = "/afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_CombiFinal/"+GetBenchmarkPoint(-1*opt.overLambda-100)+"/hhbbgg_13TeV_DataCard.txt"  
	listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun/"+GetBenchmarkPoint(-1*opt.overLambda-100)+"/hhbbgg_13TeV_DataCard.txt"  
	listFiles['bbbb'] = "datacard_bbbb_"+str(opt.overLambda)+".txt" #"cadi/HIG-17-017/BM"+str(-1*opt.overLambda-100)+"/datacard_DedicatedTraining-bias.txt"
	bbbbPath = "cadi/HIG-17-017/BM"+str(-1*opt.overLambda-100)+"/hists_SMTraining-bias.root"
elif opt.overLambda < 100: 
	#listFiles['bbtt'] = "datacard_bbtt_"+str(opt.overLambda)+".txt"
	#listFiles['bbww'] = "datacard_bbww_"+str(opt.overLambda)+".txt"
	#if opt.overLambda >=0 : listFiles['bbgg'] = "cadi/HIG-17-008/NonResonant/Kl_Scan/CombinedCard_Node_SMkl"+str(opt.overLambda)+"p0_kt1p0_cg0p0_c20p0_c2g0p0/hhbbgg_13TeV_DataCard.txt"
	#else : listFiles['bbgg'] = "cadi/HIG-17-008/NonResonant/Kl_Scan/CombinedCard_Node_SMklm"+str(abs(opt.overLambda))+"p0_kt1p0_cg0p0_c20p0_c2g0p0/hhbbgg_13TeV_DataCard.txt"
	listFiles['bbbb'] = "cadi/HIG-17-017/BSMscan/datacard_Training0_kl_"+str(opt.overLambda)+"_kt_1.txt" #"datacard_ggHHbbbb-nonRes_sum-20170502-234140.txt"
	bbbbPath = "cadi/HIG-17-017/BSMscan/hists_Training0_kl_"+str(opt.overLambda)+"_kt_1.root"
	#if 	opt.overLambda == 1 :
	#	#listFiles['bbgg'] = "Combi/CombinedCard_ARW_kl_1p0_kt_1p0_cg_0p0_c2_0p0_c2g_0p0/hhbbgg_13TeV_DataCard.txt" #"SM_hhbbgg_13TeV_DataCard_forCombination.txt"
	#	listFiles['bbgg'] = "/afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_CombiFinal/CombinedCard_ARW_/hhbbgg_13TeV_DataCard.txt" #"SM_hhbbgg_13TeV_DataCard_forCombination.txt"
	#if opt.overLambda >=0 : listFiles['bbgg'] = "/afs/cern.ch/user/a/andrey/public/HH/Combi_01Feb2018/LIMS_CombiFinal/CombinedCard_ARW_kl_"+str(opt.overLambda)+"p0_kt_1p0_cg_0p0_c2_0p0_c2g_0p0/hhbbgg_13TeV_DataCard.txt"
	if opt.overLambda >=0 : listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun/CombinedCard_ARW_kl_"+str(abs(opt.overLambda))+"p0_kt_1p0_cg_0p0_c2_0p0_c2g_0p0/hhbbgg_13TeV_DataCard.txt"
	else : listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun/CombinedCard_ARW_kl_m"+str(abs(opt.overLambda))+"p0_kt_1p0_cg_0p0_c2_0p0_c2g_0p0/hhbbgg_13TeV_DataCard.txt"
	#print listFiles['bbgg']
elif opt.overLambda > 100 :
	spinbbbb = "spin0"
	if opt.graviton : spinbbbb = "spin2"
	#listFiles['bbtt'] = "datacard_bbtt_"+str(opt.overLambda)+".txt"
	#listFiles['bbww'] = "datacard_bbww_"+str(opt.overLambda)+".txt"
	if not opt.graviton :
		if opt.overLambda > 550 : listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun_Res_HM/Radion_Node_"+str(opt.overLambda)+"/datacards/hhbbgg_13TeV_DataCard.txt"	
		else :listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun_Res_LM/Radion_Node_"+str(opt.overLambda)+"/datacards/hhbbgg_13TeV_DataCard.txt"
	else :
		if opt.overLambda > 550 : listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun_Res_HM/BulkGraviton_Node_"+str(opt.overLambda)+"/datacards/hhbbgg_13TeV_DataCard.txt"	
		else :listFiles['bbgg'] = "cadi/HIG-17-008/LIMS_FinalRun_Res_LM/BulkGraviton_Node_"+str(opt.overLambda)+"/datacards/hhbbgg_13TeV_DataCard.txt"

	if opt.overLambda < 320 :
		listFiles['bbbb'] = "cadi/HIG-17-009/"+spinbbbb+"/LMR/LMR_"+str(opt.overLambda)+"_gaus_exp_250_330/datacard_"+str(opt.overLambda)+"_gaus_exp_250_330.txt" #"datacard_ggHHbbbb-nonRes_sum-20170502-234140.txt"
		bbbbPath = "cadi/HIG-17-009/"+spinbbbb+"/LMR/LMR_"+str(opt.overLambda)+"_gaus_exp_250_330/"
	elif opt.overLambda <= 550 :
		listFiles['bbbb'] = "cadi/HIG-17-009/"+spinbbbb+"/LMR/LMR_"+str(opt.overLambda)+"_novo_285_625/datacard_"+str(opt.overLambda)+"_novo_285_625.txt" #"datacard_ggHHbbbb-nonRes_sum-20170502-234140.txt"
		bbbbPath = "cadi/HIG-17-009/"+spinbbbb+"/LMR/LMR_"+str(opt.overLambda)+"_novo_285_625/"		
	elif opt.overLambda <= 1200 :
		listFiles['bbbb'] = "cadi/HIG-17-009/"+spinbbbb+"/MMR/MMR_"+str(opt.overLambda)+"_novo_550_1200/datacard_"+str(opt.overLambda)+"_novo_550_1200.txt" #"datacard_ggHHbbbb-nonRes_sum-20170502-234140.txt"
		bbbbPath = "cadi/HIG-17-009/"+spinbbbb+"/MMR/MMR_"+str(opt.overLambda)+"_novo_550_1200/"
	else :
		if not opt.graviton :
			listFiles['bbbb'] = "cadi/B2G-16-026/AABH/Datacards_newFitRange/Radion/HH_mX_"+str(opt.overLambda)+"_bump_13TeV.txt"
			bbbbPath = "cadi/B2G-16-026/AABH/Datacards_newFitRange/Radion/"
		else : 
			listFiles['bbbb'] = "cadi/B2G-16-026/AABH/Datacards_newFitRange/BulkGrav/HH_mX_"+str(opt.overLambda)+"_bump_13TeV.txt"
			bbbbPath = "cadi/B2G-16-026/AABH/Datacards_newFitRange/BulkGrav/"

		#devo prendere l'high mass da B2G
groupth = []
groupExp = []
groupSys = []

if opt.inputFile is not "" :
	inFile = open(opt.inputFile)
	print "opening",opt.inputFile,"and sending to",destName
else: 
	inFile = open(listFiles[opt.channel])
	print "opening",listFiles[opt.channel],"and sending to",destName

outfile = open(destName, "wb")

if opt.channel == "bbtt" : bbttCleaner(inFile,outfile)
elif opt.channel == "bbww" : bbwwCleaner(inFile,outfile)
elif opt.channel == "bbgg" : bbggCleaner(inFile,outfile)
elif opt.channel == "bbbb" : bbbbCleaner(inFile,outfile,bbbbPath) #Ask authors to change these, it would be better

if opt.projection > 0 :
	lumiRate = opt.projection / 35.9
	lsstring = "lumiscale rateParam * * {0} \n".format(lumiRate)
	outfile.write(lsstring) #Move to 10fb in HMR
	outfile.write("nuisance edit freeze lumiscale\n")
