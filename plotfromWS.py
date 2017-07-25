#! /usr/bin/env python
import sys
import os
import re
import math
from scipy.special import erf
from ROOT import *
import ROOT

gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");

f = TFile.Open("hzz4l_allS_8TeV.root")
w =f.Get("w");
w.Print()
s = w.pdf("model_s");
b = w.pdf("model_b");
data = w.data("data_obs")
#data = w.data("qqzz_TempDataHist_3_8")
#data.append(w.data("ZX_FullDataHist_3_8"))
#data.append(w.data("ZX_FullDataHist_Up_3_8"))
#data.append(w.data("ZX_FullDataHist_Down_3_8"))
#data.append(w.data("qqzz_TempDataHist_1_8"))
#data.append(w.data("ZX_FullDataHist_1_8"))
#data.append(w.data("ZX_FullDataHist_Up_1_8"))
#data.append(w.data("ZX_FullDataHist_Down_1_8"))
#data.append(w.data("qqzz_TempDataHist_2_8"))
#data.append(w.data("ZX_FullDataHist_2_8"))
#data.append(w.data("ZX_FullDataHist_Up_2_8"))
#data.append(w.data("ZX_FullDataHist_Down_2_8"))

#norms = w.formula("ggzz_norm")
m4l = w.var("CMS_zz4l_widthMass");
#m4l.setBins(69);
#m4l.setRange(220,1600);
plot = m4l.frame();
dataset = w.set("ModelConfig_Observables")
bkgRate = 76.8200+ 1.3800+46.1900+ 0.5500+31.6400 +1.7800
sigRate = 14.3100+0.8762+8.6004+0.5069+5.9969+0.3732
s.plotOn(plot,RooFit.Name("kone"),RooFit.FillStyle(0),RooFit.ProjWData(dataset,data));
b.plotOn(plot,RooFit.Name("kbkg"),RooFit.FillStyle(0),RooFit.ProjWData(dataset,data),RooFit.LineColor(kRed+1),RooFit.Normalization(bkgRate))
s.Print()
pdflist = ROOT.RooArgList()
pdflist.add(b.getPdf("ch1"))
pdflist.add(b.getPdf("ch2"))
pdflist.add(b.getPdf("ch3"))
pdflist.add(s.getPdf("ch1"))
pdflist.add(s.getPdf("ch2"))
pdflist.add(s.getPdf("ch3"))

coeflist= ROOT.RooArgList()
coeflist.add(ROOT.RooRealVar("a","a",(76.8200+ 1.3800)/(sigRate+bkgRate)))
coeflist.add(ROOT.RooRealVar("b","b",(46.1900+ 0.5500)/(sigRate+bkgRate))          )    
coeflist.add(ROOT.RooRealVar("c","c",(31.6400+ 1.7800)/(sigRate+bkgRate)))
coeflist.add(ROOT.RooRealVar("d","d",(14.3100+0.8762)/(sigRate+bkgRate)))
coeflist.add(ROOT.RooRealVar("e","e",(8.6004+0.5069)/(sigRate+bkgRate)))
coeflist.add(ROOT.RooRealVar("f","f",(5.9969+0.3732)/(sigRate+bkgRate)))

print coeflist.getSize(), pdflist.getSize()
hs=s.createHistogram("hone",m4l,RooFit.ProjWData(dataset,data))
hb=b.createHistogram("hbkg",m4l,RooFit.ProjWData(dataset,data))
#hplusb = hs.Clone("hsplusb")
#hplusb.Add(hb)
#coeff = s.evaluate()/(s.evaluate()+bkgRate)


#splusb = RooAddPdf("SplusB","SplusB",pdflist,coeflist)#mettere ratio S/B
#splusb.plotOn(plot,RooFit.Name("kbkg"),RooFit.FillStyle(0),RooFit.ProjWData(dataset,data),RooFit.LineColor(kGreen+1),RooFit.Normalization(bkgRate+sigRate))

data.plotOn(plot)
plot.Draw()
#hplusb.Draw("SAME")
hs.Draw("SAME")
hb.Scale(bkgRate)
hb.Draw("SAME")
hsum=hs.Clone("hH")
hsum.Add(hb)
hsum.Draw("SAME")
