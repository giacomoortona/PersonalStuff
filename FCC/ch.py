from ROOT import *
import os,re, optparse
import CombineHarvester.CombineTools.ch as ch
#from libCombineHarvesterCombinePdfs import *
import CombineHarvester.CombinePdfs.morphing as morphing
import glob
### 
##This macro loads a bunch of cards and creates a combined one with morphed signal
##To create the cards with cardMaker, disable parametric option and run on all the lambdas 

##STATUS:
#RooMorphing PDF: 	rebinnare
#					Funziona solo con istogrammi 1D
#					non sono sicuro norm si chiami giusto (un underscore di troppo?) fare una prova mettendo un rate enorme solo a un punto
#Per qualche motivo fallisce la normalizzazione della RooSpline (perche e costante magari?)
#FastVertical:		Per ora non funziona,  non capisco perche ma non prende le shapes
#Nuisance:			Sembra funzionare, ma posso usare solo 3 punti
def parseOptions():

    usage = ('usage: %prog [options] datasetList\n'+ '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('-t', '--tag', dest='tag', type='string', default="2D_aahh", help='')
    #parser.add_option('-u', '--unfold', dest='unfold', type='int', default=1, help='unfold (1) or not (0)')
    #parser.add_option('-s', '--stop', dest='stop', type='int', default=1, help='stop to see the plot')
    global opt, args
    (opt, args) = parser.parse_args()

parseOptions()
global opt, args



##RooMorphingPDF
cmb1 = ch.CombineHarvester()
#cmb1.SetFlag('workspaces-use-clone', True)
#lambdas = [0.5,0.9,0.95,1.0,1.03,1.05,1.1,1.5] #ho eliminato 1.05,1.03 per fare aa,bb
#lambdas = [0.5,0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.1,1.5] 
#lambdas = [0.9,0.95,0.96,0.98,1.00,1.02,1.04,1.05,1.1]
#lambdas = [0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.1]
lambdas = [0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.02,1.03,1.05,1.1]
if "boosted" in opt.tag : lambdas = [1.0,0.5,0.9,0.95,1.05,1.1,1.5]

for klambda in lambdas :
	cmb1.ParseDatacard("card{0:.2f}.txt".format(klambda), "htt", "14TeV", "mt", 1, "{0:.2f}".format(klambda))
#cmb1.ParseDatacard("card1_orig.txt", "htt", "14TeV", "mt", 1, "1")
#cmb1.ParseDatacard("card2.txt", "htt", "14TeV", "mt", 1, "1.2")
#cmb1.ParseDatacard("card3.txt", "htt", "14TeV", "mt", 1, "0.8")
cmb1.PrintObs().PrintProcs().PrintSysts()
ws = RooWorkspace("morph","morph") #TFile.Open("ws.root","RECREATE")
ch.SetStandardBinNames(cmb1);

print "======= after parsing"
print " "
cmb1.PrintAll()
#w.
#cmb1.WriteDatacard("cardAll.txt","ws.root")

#kl = RooRealVar("kl","kl",0,-1,1)
kl = ws.factory("kl[1,0.5,1.5]")
#def BuildRooMorphing(ws, cb, bin, process, mass_var
for b in cmb1.bin_set():
    for p in cmb1.cp().bin([b]).signals().process_set():
		morphing.BuildRooMorphing(ws, cmb1, b, p, kl, verbose=False)

print "built morphing"
print "======= after morphing"
print " "
cmb1.PrintAll()

#for i in ["uno","due","tre"]:
#	BuildRooMorphing(ws, cmb1, cmb1.bin_set(), i , kl);
cmb1.ForEachObj(lambda obj: obj.set_bin(obj.channel()))
# The process name also needs to be common between bins
#cmb1.ForEachProc(lambda obj: obj.set_process('signal'))
#cmb1.ForEachSyst(lambda obj: obj.set_process('signal'))
cmb1.FilterObs(lambda obj: obj.mass() != '1.00')
#cmb1.backgrounds().FilterAll(lambda obj: obj.mass() != '1.00' and not obj.set_process('HH')) # FilterObs(lambda obj: obj.mass() != '1')
cmb1.FilterAll(lambda obj: obj.mass() != '1.00' and not "HH" in obj.process() )
print "======= after stranezze"
print " "

cmb1.PrintObs().PrintProcs().PrintSysts()

# Just to be safe
kl.setConstant(True)

#cmb1.cp().PrintBins()

# Now the workspace is copied into the CH instance and the pdfs attached to the processes
# (this relies on us knowing that BuildRooMorphing will name the pdfs in a particular way)
cmb1.AddWorkspace(ws, True)
#cmb1.process(['signal']).PrintProcs() 
#cmb1.process(['signal']).ExtractPdfs(cmb1, 'morph', '$BIN_$PROCESS_morph', '')
cmb1.cp().process(['HH']).ExtractPdfs(cmb1, 'morph', 'htt_mt_1_14TeV_HH_morph', '')
print "======= after ExtractPDF"
cmb1.PrintObs().PrintProcs().PrintSysts()
ws.Print()

# Adjust the rateParams a bit - we currently have three for each bin (one for each mass),
# but we only want one. Easiest to drop the existing ones completely and create new ones
#cmb1.syst_type(['rateParam'], False)
#cmb1.cp().process(['signal']).AddSyst(cmb1, 'norm_$BIN', 'rateParam', ch.SystMap()(1.00))

# Have to set the range by hand
#for sys in cmb1.cp().syst_type(['rateParam']).syst_name_set():
#    cmb1.GetParameter(sys).set_range(0.5, 1.5)

# Print the contents of the model
#cmb1.PrintAll()

# Write out the cards, one per bin
writer = ch.CardWriter('$TAG/$BIN.txt', '$TAG/shapes.root')
writer.SetVerbosity(1)
#writer.WriteCards('w_cards_v3_morphed1D_maa', cmb1)
writer.WriteCards('w_cards_v5_morphed'+opt.tag, cmb1)

### ###Trying verticalInterp.
### ws = RooWorkspace("morph","morph")
### kl = RooRealVar("kl","kl",1,0.8,1.2)
### TemplateName = "2dfunc"
### 
### #retrieve histos
### x = RooRealVar("x","x",1,0,8)
### x.setBins(20)
### y = RooRealVar("y","y",1,0,8)
### y.setBins(20)
### 
### varList = RooArgList(x)
### varSet = RooArgSet(x)
### files = [TFile.Open("out1.root"),TFile.Open("out2.root"),TFile.Open("out3.root")]
### #templates = [files[0].Get("signal2D").Clone("central"),files[1].Get("signal2D").Clone("Up"),files[2].Get("signal2D").Clone("Down"),files[0].Get("bkg2D"),files[0].Get("data_obs2D")]
### templates = [files[0].Get("signal").Clone("central"),files[1].Get("signal").Clone("Up"),files[2].Get("signal").Clone("Down"),files[0].Get("bkg"),files[0].Get("data_obs")]
### datahist = [
### 	RooDataHist("datacentral","datacentral",varList,templates[0]),
### 	RooDataHist("dataup","dataup",varList,templates[1]),
### 	RooDataHist("datadown","datadown",varList,templates[2]),
### 	RooDataHist("dataBkg","dataBkg",varList,templates[3]),
### 	RooDataHist("data_obs","data_obs",varList,templates[4])
### ]
### pdfs = [
### 	RooHistPdf("pdfcentral","pdfcentral",varSet,datahist[0]),
### 	RooHistPdf("pdfup","pdfup",varSet,datahist[1]),
### 	RooHistPdf("pdfdown","pdfdown",varSet,datahist[2]),
### ] #= RooHistPdf(TemplateName,TemplateName,RooArgSet(CMS_zz4l_mass,VD),Fisher_ggH_dataHist)
### bkg = 	RooHistPdf("bkg","bkg",varSet,datahist[3])
### #obs =	RooHistPdf("data_obs","data_obs",RooArgSet(x,y),datahist[4])
### 
### #signal = FastVerticalInterpHistPdf2D("signal","signal",x,y,False,RooArgList(pdfs[0],pdfs[1],pdfs[2]),RooArgList(kl))
### signal = FastVerticalInterpHistPdf("signal","signal",x,RooArgList(pdfs[0],pdfs[1],pdfs[2]),RooArgList(kl))
### getattr(ws,'import')(signal,RooFit.RecycleConflictNodes())
### bkg.Print()
### getattr(ws,'import')(bkg,RooFit.RecycleConflictNodes())
### getattr(ws,'import')(datahist[4],RooFit.RecycleConflictNodes())
### ws.writeToFile("morphFile.root")
