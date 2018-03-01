from ROOT import *
import os,re, optparse
import CombineHarvester.CombineTools.ch as ch
#devo importare higgsanalyssi?
#selections:
# 1D(m_hh) : sel10
# 1D(m_aa) : sel9
# 1D(m_bb) : sel8 (skip this)
# 2D(m_hh,m_aa) : sel9/10 (is the same)
# 2D(m_aa,m_bb) : sel8

def parseOptions():

    usage = ('usage: %prog [options] datasetList\n'+ '%prog -h for help')
    parser = optparse.OptionParser(usage)
    parser.add_option('-t', '--tipo', dest='tipo', type='string', default="hmaa_mhh", help='')
    parser.add_option('-u', '--unfold', dest='unfold', type='int', default=0, help='unfold (1) or not (0)')
    parser.add_option('-p', '--non-parametric', action="store_false", dest='parametric', default=True, help='use morphing instead of parametric')
    parser.add_option('-k', '--constant-lambda', action="store_true", dest='constlambda', default=False, help='use constant lambda for mhh shape')
    #parser.add_option('-s', '--stop', dest='stop', type='int', default=1, help='stop to see the plot')
    global opt, args
    (opt, args) = parser.parse_args()

parseOptions()
global opt, args

#bins2D
# 50 = 5*5*2
# 75 = 5*5*3
#sel8: #10-15 OK < 10-10 OK < 5-10 KO ~ 10-5 OK < 10-3 OK
#10-3 = 5*25 = 125 bins
#sel9 (single points) : 5-3 = 10*25 = 250 bins
print "tipo = "+opt.tipo
tipo = opt.tipo # hmaa_mhh, sel9

#tipo = "hmaa_mbb" # hmaa_mhh, sel8
#tipo = "hh_m" #sel10
#tipo = "haa_m" #sel9
if opt.unfold == 0 :
	unfold = False
else:
	unfold = True

rebin1 = 5
rebin2 = 3
selection = "sel9"
dim = 2
folder = "hhbbaa"

if tipo == "hmaa_mhh" :
	selection = "sel9"
	dim = 2
	rebin1 = 2#10
	rebin2 = 2#5

elif tipo == "hmaa_mbb" :
	selection = "sel8"
	dim = 2
	rebin1 = 2
	rebin2 = 2

elif tipo == "hh_m" :
	selection = "sel10"
	dim =1 

elif tipo == "haa_m" :
	selection = "sel9"
	dim = 1

elif tipo == "boosted" :
	tipo = "hh_m"
	selection = "sel10"
	dim =1 
	folder = "hh_boosted"
#klambda = 1.5
processes = ["HH","jgjj","ggjj","ttH","data_obs"]
#lambdas = [0.5,0.9,0.95,1.0,1.03,1.05,1.1,1.5]
#lambdas = [0.5,0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.1,1.5]
#lambdas = [0.9,0.95,0.96,0.98,1.00,1.02,1.04,1.05,1.1]
#lambdas = [0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.01,1.02,1.03,1.04,1.05,1.1]
#lambdas = [0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.02,1.03,1.05,1.1]
lambdas = [1.00]

if opt.tipo == "boosted" : 
	processes = ["HH","QCD","data_obs"]
	#lambdas = [1.0,0.5,0.9,0.95,1.05,1.1,1.5]

#if opt.tipo == "hh_m" :
#	x = RooRealVar("x","x",240,1500) #mhh
#	x.setBins(50)
#else:	
x = RooRealVar("x","x",115,135) #maa
x.setBins(50)
if tipo == "hmaa_mbb" :
	y = RooRealVar("y","y",80,140) #mbb
	y.setBins(50)		
elif opt.tipo == "boosted" :
	y = RooRealVar("y","y",220,2500) #mHH
	y.setBins(57)
elif tipo == "haa_m" :
	y = RooRealVar("y","y",115,135) #maa
	y.setBins(50)
else :
	y = RooRealVar("y","y",240,1500) #mHH
	y.setBins(75)
### 
if dim == 1 :
	varList = RooArgList(y)
	varSet = RooArgSet(y)
	unfold = False
else :
	varList = RooArgList(x,y)
	varSet = RooArgSet(x,y)
kl = RooRealVar("kl","kl",1.00,0.9,1.1)
klConst = RooRealVar("klConst","klConst",1.00)
klConst.setConstant(True)
smearPhoton = RooRealVar("smearPhoton","smearPhoton",1.00)
datasets = []

meanG = RooRealVar("meanG","mean of gaussian",125.00)#,124.8,125.2) 
sigmaG = RooFormulaVar("sigmaG","sigmaG","1.30292*@0",RooArgList(smearPhoton))#sigmaG= RooRealVar("sigmaG","width of gaussian",1.30292)#,1.12971-2.0/1000.0,1.12971+2.0/1000.0) 
meanG.setConstant()
smearPhoton.setConstant()
gauss = RooGaussian("gauss","gaussian PDF",x,meanG,sigmaG) 
#These values should be retuned for Boosted analysis
if not opt.constlambda :
	constL = RooFormulaVar("constL","0.0437283+@0*1.34435-@0*@0*0.695253",RooArgList(kl)) 
	meanL = RooFormulaVar("meanL","421.557+@0*25.7048",RooArgList(kl)) 
	sigmaL= RooFormulaVar("sigmaL","135.194-@0*151.369+@0*@0*77.4694",RooArgList(kl)) 
	expoC= RooFormulaVar("expoC","-0.00585114+@0*0.000626062",RooArgList(kl)) 
	changer= RooFormulaVar("changer","615.666+@0*77.17",RooArgList(kl)) 
else :
	constL = RooFormulaVar("constL","0.0437283+@0*1.34435-@0*@0*0.695253",RooArgList(klConst)) 
	meanL = RooFormulaVar("meanL","421.557+@0*25.7048",RooArgList(klConst)) 
	sigmaL= RooFormulaVar("sigmaL","135.194-@0*151.369+@0*@0*77.4694",RooArgList(klConst)) 
	expoC= RooFormulaVar("expoC","-0.00585114+@0*0.000626062",RooArgList(klConst)) 
	changer= RooFormulaVar("changer","615.666+@0*77.17",RooArgList(klConst)) 
landau = LandauExp("LandauExp","LandauExp",y,constL,meanL,sigmaL,expoC,changer)

for klambda in lambdas :
	rates = []
	histos = []
	inFile = TFile.Open("{1}/root_HH_kappa_l_{0:.2f}/shapes.root".format(klambda,folder))
	outFile = open("card{0:.2f}.txt".format(klambda),"w")
	#outWS = TFile.Open("hhbbaa/root_HH_kappa_l_{0:.2f}/ws.root","RECREATE")
	ws = RooWorkspace("w")

	allPdfs = []
	for iproc in processes :
		if "HH" in iproc and not "bb" in tipo and opt.parametric :
			#do stuff to generate rooprodpdf
			#// Declare variables x,mean,sigma with associated name, title, initial value and allowed range
			if tipo == "hmaa_mhh" : pdf = RooProdPdf("HH","HH",landau,gauss)
			elif tipo == "hh_m" : pdf = landau
			elif tipo == "haa_m" : pdf = gauss
			pdf.SetNameTitle("HH","HH")
			allPdfs.append(pdf) 
			if "boosted" in opt.tipo : rates.append(11639.5)
			else :rates.append(10211.10624)
			#wFunc = RooRealVar ("weight","event weight",1) 
			#tempdata = pdf.generate(RooArgSet(x,y),5009.4*1-15732*1+20938)
			#datasets.append(tempdata)
			#wFunc = RooRealVar ("weight","event weight",1) 
			#tempdata.addColumn(wFunc)
			#	RooDataSet (const char *name, const char *title, RooDataSet *data, const RooArgSet &vars, const char *cuts=0, const char *wgtVarName=0)
			#datasets.append(RooDataSet(tempdata.GetName(),tempdata.GetTitle(),tempdata,RooArgSet(x,y,wFunc),"True",wFunc.GetName()))
			#datasets.append()
		else :
			print "{2}_{0}_{1}".format(selection,tipo,iproc)
			htemp = inFile.Get("{2}_{0}_{1}".format(selection,tipo,iproc))
			print "BinningX,y",iproc, htemp.GetNbinsX(), htemp.GetNbinsY()
			if dim == 1 : htemp.Rebin(2)
			else : 
				htemp.RebinX(rebin1) #5
				htemp.RebinY(rebin2) #5
				print "Re-BinningX,y",iproc, htemp.GetNbinsX(), htemp.GetNbinsY()
			if unfold :
				h = TH1F(iproc,iproc,htemp.GetNbinsX()*htemp.GetNbinsY(),htemp.GetXaxis().GetXmin(),htemp.GetXaxis().GetXmax()*htemp.GetNbinsY())
				ibin=1
				for xbin in range(1,htemp.GetNbinsX()+1) :
					for ybin in range(1,htemp.GetNbinsY()+1) :
						h.SetBinContent(ibin,htemp.GetBinContent(xbin,ybin))
						ibin += 1
			else : h = htemp
			print "Binning",iproc, h.GetNbinsX()
			h.SetName(iproc)
			h.SetTitle(iproc)
			#if iproc == "HH" : 
	 		#print "scaling"
			print h.Integral(), 30000000.0*h.Integral()
	 		h.Scale(30000000.0)
	 		print h.Integral()
			#if tipo == "haa_m" : rates.append(h.Integral(h.FindBin(120),h.FindBin(130)))
			if opt.tipo == "hh_m" : rates.append(h.Integral(h.FindBin(240),h.FindBin(1500)))
			else : rates.append(h.Integral())
			#htoappend = h.Rebin(4*dim)
			for xbin in range(1,h.GetNbinsX()+1) :
	 			if h.GetBinContent(xbin)==0 : h.SetBinContent(xbin,0.001)	
			histos.append(h)
			#print "Normalizations", h.Integral(), h.Integral(h.FindBin(120),h.FindBin(130))
			rdh = RooDataHist(iproc+"rdh",iproc+"rdh",varList,h)
			#print "Normalizations", rdh.sumEntries(), h.Integral(), h.Integral(h.FindBin(120),h.FindBin(130))
			if not "obs" in iproc : 
				if "HH" in iproc and tipo == "hmaa_mbb" and opt.parametric :
					#qui fare la conditional rooprodpdf
					#if tipo == "hmbb_mhh" : pdf = RooProdPdf("HH","HH",landau,gauss) #questo non esiste perche non ha senso
					#elif tipo == "hbb_m" : pdf = RooHistPdf(iproc,iproc,varSet,rdh)
					#elif tipo == "hmaa_mbb":
					pdftemp = RooHistPdf(iproc+"temp",iproc+"temp",varSet,rdh)
					pdf = RooProdPdf("HH","HH",RooArgSet(gauss),RooFit.Conditional(RooArgSet(pdftemp),RooArgSet(y)) )
				else : pdf = RooHistPdf(iproc,iproc,varSet,rdh)
				pdf.Print()
				allPdfs.append(pdf)
				print "generating"
				datasets.append(pdf.generate(RooArgSet(x,y),h.Integral()))
				print "LEN ", len(allPdfs)
			else : 
				#print "DATAOBS",h.Integral()
				#wFunc = RooRealVar ("weight","event weight",1) 
				##datasets[0].addColumn(wFunc)
				#for i in range(0,4): print datasets[i].sumEntries()
				#for i in range(0,4): datasets[i].Print()
				#print "dataobs"
				#pdf = RooDataSet("data_obs","data_obs",RooArgSet(x,y,wFunc),"weight")
				#print pdf.sumEntries()
				#pdf.append(datasets[0])
				#print pdf.sumEntries()
				#pdf.append(datasets[1])
				#print pdf.sumEntries()
				#pdf.append(datasets[2])
				#print pdf.sumEntries()
				#pdf.append(datasets[3])
				#print pdf.sumEntries()
				#pdf.Print()
				pdf = rdh
				print "Normalizations", rdh.sumEntries(), h.Integral()
				pdf.SetNameTitle("data_obs","data_obs")
				pdf.SetName("data_obs")
				pdf.SetTitle("data_obs")
				#pdf = datasetFull
		getattr(ws,'import')(pdf,RooFit.RecycleConflictNodes())
		if opt.tipo == "boosted" :
			rfvSigRate_HH = RooFormulaVar("HH_norm","-0.4875*@0 + 1.4883",RooArgList(kl))
		else :
			rfvSigRate_HH = RooFormulaVar("HH_norm","1.6096-0.6081*@0",RooArgList(kl))
		getattr(ws,'import')(rfvSigRate_HH,RooFit.RecycleConflictNodes())
		#if iproc = "HH" : obs = inFile.Get("{2}_{0}_{1}".format(sel,tipo,iproc)).Clone("data_obs")
		#else : obs.Add(inFile.Get("{2}_{0}_{1}".format(sel,tipo,iproc)))
	#
	#obs.SetName("data_obs")
	#obs.SetTitle("data_obs")
	#ws.writeToFile("hhbbaa/root_HH_kappa_l_{0:.2f}/ws.root".format(klambda))
	outFile.write("imax 1\n")
	if opt.tipo == "boosted" :outFile.write("jmax 1\n")
	else: outFile.write("jmax 3\n")
	outFile.write("kmax *\n")
	outFile.write("----------------------\n")
	#outFile.write("shapes * * {1}/root_HH_kappa_l_{0:.2f}/ws.root $PROCESS \n".format(klambda,folder))
	outFile.write("shapes * * ws1.root w:$PROCESS \n".format(klambda,folder))
	outFile.write("----------------------\n")
	outFile.write("bin bin1\n")
	outFile.write("observation {0}\n".format(rates[len(rates)-1]))
	outFile.write("------------------------------\n")
	if opt.tipo == "boosted" :
		outFile.write("bin             bin1       bin1 \n")		
		outFile.write("process         HH        QCD\n")
		outFile.write("process         0          1 \n")
		outFile.write("rate            {0} {1}\n".format(rates[0],rates[1]))
		outFile.write("--------------------------------\n")
		#outFile.write("lumiSig     lnN    1.01       - \n")
		outFile.write("lumi     lnN    1.01 - \n")
		outFile.write("BkgScaler rateParam * QCD 1.0 \n")
		outFile.write("fakeScaler rateParam * * 0.7 \n")
	else : 
		outFile.write("bin             bin1       bin1 bin1       bin1\n")		
		outFile.write("process         HH        jgjj ggjj ttH\n")
		outFile.write("process         0          1 2 3\n")
		outFile.write("rate            {0} {1} {2} {3}\n".format(rates[0],rates[1],rates[2],rates[3]))
		outFile.write("--------------------------------\n")
		outFile.write("lumiSig     lnN    1.01       - - - \n")
		outFile.write("lumi     lnN    1.01 - - 1.01\n")
		outFile.write("BkgScaler rateParam * jgjj 1.0 \n")
		outFile.write("BkgScaler rateParam * ggjj 1.0 \n")
		outFile.write("BkgScaler rateParam * ttH 1.0 \n")
	#outFile.write("bgnorm   lnN    1.00       1.3\n")
	#name rateParam bin process initial_value
	outWS = TFile.Open("{1}/root_HH_kappa_l_{0:.2f}/ws.root".format(klambda,folder),"RECREATE")
	outWS.cd()
	for h in histos :
		h.Write()
	ws.writeToFile("ws1.root")