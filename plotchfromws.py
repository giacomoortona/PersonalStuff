#! /usr/bin/env python
import sys
import os
import re
import math
from scipy.special import erf
from ROOT import *
import ROOT

gSystem.Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so")

logy = False
xstart = 220
xend = 500

names= ["2e2mu","4e","4mu","all"]
pdfs = []
pdfsK = []
pdfsK2=[]
norms = []
normsK = []
normsK2=[]
m4lVar = RooRealVar()
for i in range(len(names)) :
    if i <3:
        f = TFile.Open("cards_03_05_Unblind_093_2D/HCG/220/hzz4l_{0}S_8TeV.input.root".format(names[i]))
        fK = TFile.Open("cards_093_AlternativeKBKG/HCG/220/hzz4l_{0}S_8TeV.input.root".format(names[i]))
        fK2 = TFile.Open("cards_093_AlternativeKBKG_28/HCG/220/hzz4l_{0}S_8TeV.input.root".format(names[i]))
        #f = TFile.Open("cards_03_05_Unblind_093_2D/HCG/220/hzz4l_allS_8TeV.input.root")
        #fK = TFile.Open("cards_093_AlternativeKBKG/HCG/220/hzz4l_allS_8TeV.input.root")
        wK =fK.Get("w")
        wK2 =fK2.Get("w")
        w =f.Get("w")
        s = w.pdf("ggzz")
        sK = wK.pdf("ggzz")
        sK2 = wK2.pdf("ggzz")
        s.SetNameTitle("ggzz{0}".format(names[i]),"ggzz{0}".format(names[i]))
        sK.SetNameTitle("ggzz{0}k".format(names[i]),"ggzz{0}k".format(names[i]))
        sK2.SetNameTitle("ggzz{0}k2".format(names[i]),"ggzz{0}k2".format(names[i]))
        print "norm before: ", w.function("ggzz_norm").getVal(), "norm after: ", wK.function("ggzz_norm").getVal()
        
        v = w.pdf("vbf_offshell")
        vK = wK.pdf("vbf_offshell")
        pdfs.append(s)
        pdfsK.append(sK)
        pdfsK2.append(sK2)
        norms.append(w.function("ggzz_norm").getVal())
        normsK.append(wK.function("ggzz_norm").getVal())
        normsK2.append(wK2.function("ggzz_norm").getVal())
        print norms[i],"  ",normsK[i]
        #s = w.pdf("model_s")
        #sK = wK.pdf("model_s")
        
        #cat = w.cat("CMS_channel")
        #set = w.set("ModelConfig_Observables")
        #data_obs= w.data("data_obs")
        #projData = RooDataHist("projDataWMixH","projDataWMixH",set,data_obs)
        m4l = w.var("CMS_zz4l_widthMass")
        #m4lVar = m4l
    else:
        a = RooRealVar("a","a",norms[0]/(norms[0]+norms[1]+norms[2]))
        b = RooRealVar("b","b",norms[1]/(norms[0]+norms[1]+norms[2]))
        c = RooRealVar("c","c",norms[2]/(norms[0]+norms[1]+norms[2]))
        aK = RooRealVar("aK","aK",normsK[0]/(normsK[0]+normsK[1]+normsK[2]))
        bK = RooRealVar("bK","bK",normsK[1]/(normsK[0]+normsK[1]+normsK[2]))
        cK = RooRealVar("cK","cK",normsK[2]/(normsK[0]+normsK[1]+normsK[2]))
        aK2 = RooRealVar("aK2","aK2",normsK2[0]/(normsK2[0]+normsK2[1]+normsK2[2]))
        bK2 = RooRealVar("bK2","bK2",normsK2[1]/(normsK2[0]+normsK2[1]+normsK2[2]))
        cK2 = RooRealVar("cK2","cK2",normsK2[2]/(normsK2[0]+normsK2[1]+normsK2[2]))
        a.setConstant(True)
        b.setConstant(True)
        c.setConstant(True)
        aK.setConstant(True)
        bK.setConstant(True)
        cK.setConstant(True)
        aK2.setConstant(True)
        bK2.setConstant(True)
        cK2.setConstant(True)                                                
        #print aK.getVal(), " ",bK.getVal(), " ",cK.getVal()
        #print a.getVal(), " ",b.getVal(), " ",c.getVal()
        s = RooAddPdf("all","all",ROOT.RooArgList(pdfs[0],pdfs[1],pdfs[2]),ROOT.RooArgList(a,b,c))
        sK = RooAddPdf("allK","allK",ROOT.RooArgList(pdfsK[0],pdfsK[1],pdfsK[2]),ROOT.RooArgList(aK,bK,cK))
        sK2 = RooAddPdf("allK2","allK2",ROOT.RooArgList(pdfsK2[0],pdfsK2[1],pdfsK2[2]),ROOT.RooArgList(aK2,bK2,cK2))
        #m4l = m4lVar
        #m4l = RooRealVar("CMS_zz4l_widthMass","CMS_zz4l_widthMass",220,1200)

    m4l.setBins(25000)
    if i == 0 : m4l.setRange(xstart,min(800,xend))
    else : m4l.setRange(xstart,min(1200,xend))
    plot = m4l.frame()
    #plots = s.plotOn(plot,RooFit.Name("kone"),RooFit.FillStyle(0),RooFit.ProjWData(set,data_obs))
    #plotsk= sK.plotOn(plot,RooFit.LineColor(kRed+1),RooFit.Name("knew"),RooFit.FillStyle(0),RooFit.ProjWData(set,data_obs))
    s.plotOn(plot,RooFit.Name("kone"),RooFit.FillStyle(0))
    sK.plotOn(plot,RooFit.LineColor(kRed+1),RooFit.Name("knew"),RooFit.FillStyle(0))
    sK2.plotOn(plot,RooFit.LineColor(kGreen+1),RooFit.Name("k28"),RooFit.FillStyle(0))
    #if i==3 :
    #    pdfs[0].plotOn(plot,RooFit.Name("kone1"),RooFit.FillStyle(0),RooFit.LineColor(kGreen+1))
    #    pdfs[1].plotOn(plot,RooFit.Name("kone2"),RooFit.FillStyle(0),RooFit.LineColor(kGreen+2))
    #    pdfs[2].plotOn(plot,RooFit.Name("kone3"),RooFit.FillStyle(0),RooFit.LineColor(kGreen+3))
    #v.plotOn(plot,RooFit.Name("koneVBF"),RooFit.FillStyle(0),RooFit.LineStyle(2))
    #vK.plotOn(plot,RooFit.LineColor(kRed+1),RooFit.Name("knewVBF"),RooFit.FillStyle(0),RooFit.LineStyle(2))
    c2 =  TCanvas()
    plot.Draw()
    if xend > 700 : plot.SetAxisRange(0.00001,0.5,"Y")
    leg =  TLegend(0.5,0.65,0.8,0.85)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.AddEntry("kone","ggZZ, {0}, K=1".format(names[i]),"l")
    leg.AddEntry("knew","ggZZ, {0}, K=1/2.8".format(names[i]),"l")
    leg.AddEntry("k28","ggZZ, {0}, K=2.8".format(names[i]),"l")
    #leg.AddEntry("koneVBF","VBF, {0}, K=1".format(names[i]),"l")
    #leg.AddEntry("knewVBF","VBF, {0}, K=1/2.8".format(names[i]),"l")
    leg.Draw()
    if logy : c2.SetLogy()
    c2.SaveAs("03_09_ggZZKfact_{0}_up500.pdf".format(names[i]))
    c2.SaveAs("03_09_ggZZKfact_{0}_up500.png".format(names[i]))
    c2.SaveAs("03_09_ggZZKfact_{0}_up500.eps".format(names[i]))
    c2.SaveAs("03_09_ggZZKfact_{0}_up500.gif".format(names[i]))
    c2.SaveAs("03_09_ggZZKfact_{0}_up500.root".format(names[i]))
    if i == 3:
        hone = s.createHistogram("hone",m4l,RooFit.Binning(69,xstart,xend))
        hnew = sK.createHistogram("hnew",m4l,RooFit.Binning(69,xstart,xend))
        h28 = sK2.createHistogram("h28",m4l,RooFit.Binning(69,xstart,xstart))
        full=0
        fullK=0
        fullK2=0
        for ib in range (1,70):
            full+=hone.GetBinContent(ib)
            fullK+=hnew.GetBinContent(ib)
            fullK2+=h28.GetBinContent(ib)
        print full,"  ",fullK
        c4 = TCanvas()
        hone.Draw()
        hnew.Draw("SAME")
        h28.Draw("SAME")
        c5 = TCanvas()
        hone.DrawNormalized()
        hnew.DrawNormalized("SAME")
        h28.DrawNormalized("SAME")    
        


