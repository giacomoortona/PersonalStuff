from ROOT import *
import os,re, optparse
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
    parser.add_option('-u', '--unfold', dest='unfold', type='int', default=1, help='unfold (1) or not (0)')
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
print "tipo = "+opt.tipo

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
	rebin1 = 10
	rebin2 = 5

elif tipo == "hmaa_mbb" :
	selection = "sel8"
	dim = 2
	rebin1 = 10
	rebin2 = 5

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
lambdas = [0.9,0.95,0.96,0.97,0.98,0.99,1.00,1.02,1.03,1.05,1.1]

if opt.tipo == "boosted" : 
	processes = ["HH","QCD","data_obs"]
	lambdas = [1.0,0.5,0.9,0.95,1.05,1.1,1.5]

x = RooRealVar("x","x",120,130)
x.setBins(50)
if tipo == "hmaa_mbb" :
	y = RooRealVar("y","y",80,140)
	y.setBins(50)	
else :
	y = RooRealVar("y","y",240,1500)
	y.setBins(75)
### 
if dim == 1 :
	varList = RooArgList(y)
	varSet = RooArgSet(y)
	unfold = False
else :
	varList = RooArgList(x,y)
	varSet = RooArgSet(x,y)
	
for klambda in lambdas :
	rates = []
	histos = []
	inFile = TFile.Open("{1}/root_HH_kappa_l_{0:.2f}/shapes.root".format(klambda,folder))
	outFile = open("card{0:.2f}.txt".format(klambda),"w")
	#outWS = TFile.Open("hhbbaa/root_HH_kappa_l_{0:.2f}/ws.root","RECREATE")
	ws = RooWorkspace("w")

	for iproc in processes :
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
		rates.append(h.Integral())
		#htoappend = h.Rebin(4*dim)
		for xbin in range(1,h.GetNbinsX()+1) :
 			if h.GetBinContent(xbin)==0 : h.SetBinContent(xbin,0.001)	
		histos.append(h)
		rdh = RooDataHist(iproc+"rdh",iproc+"rdh",varList,h)
		if not "obs" in iproc : pdf = RooHistPdf(iproc,iproc,varSet,rdh)
		else : 
			pdf = rdh
			pdf.SetNameTitle("data_obs","data_obs")
			pdf.SetName("data_obs")
			pdf.SetTitle("data_obs")
		getattr(ws,'import')(pdf,RooFit.RecycleConflictNodes())
		#if iproc = "HH" : obs = inFile.Get("{2}_{0}_{1}".format(sel,tipo,iproc)).Clone("data_obs")
		#else : obs.Add(inFile.Get("{2}_{0}_{1}".format(sel,tipo,iproc)))
	#
	#obs.SetName("data_obs")
	#obs.SetTitle("data_obs")
	#ws.writeToFile("hhbbaa/root_HH_kappa_l_{0:.2f}/ws.root".format(klambda))
	outFile.write("imax 1\n")
	outFile.write("jmax 3\n")
	outFile.write("kmax 1\n")
	outFile.write("----------------------\n")
	outFile.write("shapes * * {1}/root_HH_kappa_l_{0:.2f}/ws.root $PROCESS \n".format(klambda,folder))
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
		outFile.write("lumiSig     lnN    1.01       - \n")
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
	ws.Write()


