from ROOT import *
import optparse

#scanr_${tipo}_resg_${resolution}_effg_85_fake_${fakerate}_btag_${btag}_bkg_${bkg}_syst_1HHttH

#define function for parsing options
def parseOptions():

    usage = ('usage: %prog [options] datasetList\n'+ '%prog -h for help')
    parser = optparse.OptionParser(usage)
    #parser.add_option('-v', '--var', dest='var', type='string', default="kl", help='variable (kl, r)')
    #parser.add_option('-w', '--which', dest='what', type='int', default=3, help='which plot 1D/2D and vars')
    parser.add_option('-s', '--stop', dest='stop', type='int', default=1, help='stop at the end to see the plot')
    parser.add_option('-u', '--first', dest='fileuno', type='string', default="scankl_hmaa_mhh_resg_1.3_effg_95_fake_1_btag_1_bkg_1_syst_1HHttH")
    parser.add_option('-d', '--second', dest='filedue', type='string', default="")
    parser.add_option('-t', '--third', dest='filetre', type='string', default="")
    parser.add_option('-q', '--quattro', dest='filequattro', type='string', default="")

#    parser.add_option('-n', '--nuis', dest='nuis', type='int', default=1, help='use nuisances')
#    parser.add_option('-p', '--suffixoptions', dest='options', type='string', default="_", help='options used to run (p,k)')
    global opt, args
    (opt, args) = parser.parse_args()

def goodName(which,number):
	if which == "syst" :
		if number == "noSyst" : return "Stat. Only"
		elif "1HHttH" in number : return "#delta S/S = #delta ttH/ttH = 1%"
		elif "2HHttH" in number : return "#delta S/S = #delta ttH/ttH = 2%"
		elif "1HH" in number : return "#delta S/S = 1%"
	elif which == "bkg" : return "All Bkg #times "+number
	elif which == "btag" :
		if number == "1" : return "85% b-tag eff."
		else : return "75% b-tag eff."
	elif which == "fake" : return "Fake rate #times "+number
	elif which == "effg" : return number+"% Photon eff."
	elif which == "resg" : return "Photon #sigma="+number+" GeV"

def badName(which,number):
	if which == "syst" : return number
	elif which == "bkg" : return "bkgx"+number
	elif which == "btag" : 
		if number == "1" : return "btag085"
		else : return "btag075"
	elif which == "fake" : return "fakex"+number
	elif which == "effg" : return "effg0"+number
	elif which == "resg" : return "resg"+number


parseOptions()
global opt, args
if "scankl" in opt.fileuno : variable = "kl"
else : variable="r"

allVars = []
files = []
allVars.append(opt.fileuno.split("_"))
files.append(TFile.Open("higgsCombine"+opt.fileuno+".MultiDimFit.mH120.root"))
if len(opt.filedue.split("_"))>2 :
	allVars.append(opt.filedue.split("_"))
	files.append(TFile.Open("higgsCombine"+opt.filedue+".MultiDimFit.mH120.root"))
	if len(opt.filetre.split("_"))>2 :
		allVars.append(opt.filetre.split("_"))
		files.append(TFile.Open("higgsCombine"+opt.filetre+".MultiDimFit.mH120.root"))
		if len(opt.filequattro.split("_"))>2 :
			allVars.append(opt.filequattro.split("_"))
			files.append(TFile.Open("higgsCombine"+opt.filequattro+".MultiDimFit.mH120.root"))

leg = []
out = [] 
if len(allVars) > 1:
	wordsD = allVars[1]
	wordsU = allVars[0]
	for icheck in range(len(allVars[0])) :
		if wordsD[icheck] != wordsU[icheck]:
			leg.append(goodName(wordsD[icheck-1],wordsU[icheck]))
			leg.append(goodName(wordsD[icheck-1],wordsD[icheck]))
			out.append(badName(wordsD[icheck-1],wordsU[icheck]))
			out.append(badName(wordsD[icheck-1],wordsD[icheck]))
			if len(allVars)>2 : 
				leg.append(goodName(wordsD[icheck-1],allVars[2][icheck]))
				out.append(badName(wordsD[icheck-1],allVars[2][icheck]))
				if len(allVars)>3 : 
					leg.append(goodName(wordsD[icheck-1],allVars[3][icheck]))
					out.append(badName(wordsD[icheck-1],allVars[3][icheck]))
else:
	leg.append("Stat. Only")
	out.append("StatOnly")


trees = []
for il in range(len(files)):
	trees.append(files[il].Get("limit"))	

graphs = []

for i in range(len(trees)) : 
	graphs.append(TGraph(0))
	graphs[i].SetFillStyle(0)
	graphs[i].SetName(leg[i])
	ipoint =0
	for event in trees[i] :
		if event.deltaNLL > 6 : continue
		if variable == "kl" :
#			if whichplot is not 4 and ( event.kl<0.9 or event.kl>1.1 ): continue
#			if whichplot == 4 :
#				if event.kl<0.95 and event.kl>0.9 : continue
#				if event.kl<1.15 and event.kl>1.02 : continue
			graphs[i].SetPoint(ipoint,event.kl, 2*event.deltaNLL)
		else :
#			if event.r<0.9 or event.r>1.1 : continue
			graphs[i].SetPoint(ipoint,event.r, 2*event.deltaNLL)
		ipoint+=1
	graphs[i].Sort()
	graphs[i].SetTitle("")
	if variable == "r" : graphs[i].GetXaxis().SetTitle("r = #sigma_{obs}/#sigma_{SM}")
	else : graphs[i].GetXaxis().SetTitle("k_{#lambda} = #lambda_{obs}/#lambda_{SM}")
	graphs[i].GetYaxis().SetTitle("-2#Delta NLL")
	graphs[i].SetLineWidth(3)

c = TCanvas("c","c",600,600)
c.SetTicks(1,1)
c.SetLeftMargin(0.14)
c.SetRightMargin(0.08)
graphs[0].SetLineColor(kBlue)
if len(opt.filedue.split("_"))>2 :graphs[1].SetLineColor(kRed+2)
if len(opt.filetre.split("_"))>2 :graphs[2].SetLineColor(kGreen+3)
if len(opt.filequattro.split("_"))>2 :graphs[3].SetLineColor(kPink+2)

graphs[0].GetXaxis().SetTitleOffset(1.1)
##graphs[0].GetYaxis().SetTitleOffset(1.6)
#graphs[0].GetXaxis().SetLabelOffset(0.02)
#graphs[0].GetYaxis().SetLabelOffset(0.02)
#graphs[0].GetXaxis().SetTitleSize(0.06)
#graphs[0].GetYaxis().SetTitleSize(0.06)
#graphs[0].GetXaxis().SetLabelSize(0.06)
#graphs[0].GetYaxis().SetLabelSize(0.06)
##graphs[0].GetXaxis().SetNdivisions(505);
##graphs[0].GetYaxis().SetNdivisions(505);
##graphs[0].SetTitle("") '''
#graphs[0].GetYaxis().SetTitleOffset(1.75)
#graphs[0].GetXaxis().SetTitleOffset(1.40)
#if opt.nuis > 0 and opt.nuis < 5 and whichplot < 4 :
#	graphs[1].SetName("#delta S/S = 1%")
#	graphs[2].SetName("#delta S/S = #delta ttH/ttH = 1%")
#	graphs[1].Draw("AL")
#	graphs[2].Draw("LSAME")
#elif opt.nuis > 5 :
#	graphs[3].SetLineColor(kRed+2)
#	graphs[3].SetName("All bkg x 2")
#	graphs[4].SetLineColor(kGreen+2)
#	#graphs[4].SetLineStyle(3)
#	graphs[4].SetName("All bkg x 0.5")
#	graphs[4].Draw("AL")
#	graphs[3].Draw("LSAME")

graphs[0].Draw("AL")
if len(opt.filedue.split("_"))>2 :graphs[1].Draw("LSAME")
if len(opt.filetre.split("_"))>2 :graphs[2].Draw("LSAME")
if len(opt.filequattro.split("_"))>2 :graphs[3].Draw("LSAME")
leg = c.BuildLegend()
leg.SetLineColor(0)
leg.SetFillColor(0)

xmin = graphs[0].GetXaxis().GetXmin()
xmax = graphs[0].GetXaxis().GetXmax()
line = TLine(xmin,1,xmax,1)
line.SetLineColor(kBlack)
line.SetLineStyle(3)
line.SetLineWidth(3)
line.Draw("SAME")

#Text = TLatex()
#Text.SetNDC() 
#Text.SetTextAlign(31);
#Text.SetTextSize(0.04) 
#leftText = "FCC-hh Simulation (Delphes)"
#re = "#sqrt{{s}} = 100 TeV, L = {:.0f} ab^{{-1}}".format(30)
#text = '#it{' + leftText +'}'
#
#Text.DrawLatex(0.90, 0.92, text) 
#rightText = re.split(",")#, rightText)
#text = '#bf{#it{' + rightText[0] +'}}'
#
#Text.SetTextAlign(12);
#Text.SetNDC(True) 
#Text.SetTextSize(0.04) 
#Text.DrawLatex(0.18, 0.83, text)
#
#text = '#bf{#it{' + rightText[1] +'}}'
#Text.DrawLatex(0.18, 0.78, text)


Text = TPaveText(0.58, 0.88,0.93,0.95,'brNDC')
#Text.SetNDC() 
Text.SetTextAlign(31);
Text.SetTextSize(0.04) 
leftText = "FCC-hh Simulation (Delphes)"
re = "#sqrt{{s}} = 100 TeV, L = {:.0f} ab^{{-1}}".format(30)
text = '#it{' + leftText +'}'
#Text.DrawLatex(0.90, 0.92, text) 
Text.AddText(text)
Text.SetFillStyle(0)
Text.SetLineStyle(0)
Text.SetBorderSize(0)
Text.Draw()

Text2 = TPaveText(0.18, 0.71,0.4,0.85,'brNDC')
rightText = re.split(",")#, rightText)
text = '#bf{#it{' + rightText[0] +'}}'
Text2.SetTextAlign(12);
#Text.SetNDC(True) 
Text2.SetTextSize(0.04) 
Text2.AddText(text)
text = '#bf{#it{' + rightText[1] +'}}'
Text2.AddText(text)
#Text2.SetFillStyle(0)
Text2.SetFillColor(kWhite)
Text2.SetLineStyle(0)
Text2.SetBorderSize(0)
Text2.Draw()

#Text.DrawLatex(0.18, 0.78, rightText[1])
c.RedrawAxis()
#c.Update()
c.GetFrame().SetBorderSize( 12 )
c.Modified()
c.Update()

#c.SaveAs(titles[whichplot]+appString+variable+opt.options+".pdf")
#c.SaveAs(titles[whichplot]+appString+variable+opt.options+".root")
outString = "plot"
for legs in out : outString += legs
c.SaveAs(outString+".pdf")
c.SaveAs(outString+".root")

if opt.stop > 0 :raw_input()
