#!/usr/bin/python -tt
  #     25    1    1    2    0    0  0.35960409498E+02 -0.53973850759E+02 -0.95711389391E+03  0.96741838598E+03  0.12500000000E+03 0.  0.

import sys
import urllib2
import ROOT
from ROOT import * #TFile,TDirectory,TH2F,TString,TCanvas, RooFit

#300K events runs
#names = ["-15","-4","0","1","2.46","4","10","20"]
#runlist=["28","07","13","09","10","11","12","29"]

#"Official" plot
#names = ["-15","0","1","2.46","4","20"]
#runlist=["28","13","09","10","11","29"]
#outName="defaultRuns"

#"Positive Runs" plot
#names = ["0","2.46","4","20"]
#runlist=["13","10","11","29"]
#outName="positiveRuns"

#"Positive2 Runs" plot
#names = ["0","2.46","1","20"]
#runlist=["13","10","09","29"]
#outName="positive2Runs"

#"Anomalous Runs" plot
#names = ["1","1,y_{t}=2.3","1, c2=3"]#,"1,y_{t}=2.3,c2=3"]
#runlist=["09","30","tthh02"]#,"34"]
#outName="AnomalousRuns"

#names = ["1"]#,"1,y_{t}=2.3,c2=3"]
#runlist=["09"]#,"34"]
#outName="test"

#Temporary
#names = ["-4","0","1","2.46","4","20"]
#runlist=["07","13","09","10","11","29"]
#outName="tempRuns"

#names = ["-4","1","2.46","20"]
#runlist=["07","09","10","29"]
names = ["1"]
runlist = ["09"]
outName="tempRuns2all_eta"
colors = [kBlack,kGreen+2,kBlue,kYellow+1]
styles = [1,1,3]#,2,3,4,9,10]

#colors = [kBlack,kRed+1,kGreen+2,kBlue,kMagenta,kYellow+1]
#styles = [1,1,1,3]#,2,3,4,9,10]
fills = [3003]
run2D=0
fillVar=1 #0=mass, 1=Pt

#names=["-15"]
#runlist=["28"]
#Scan next to 2.46 to check interf effect
#names = ["0","0.5","1","1.5","2","2.46","3","3.5","4","noBox"]
#runlist=["13","18","09","19","20","10","21","22","11","24"]
printout=False
idPart = "25"
applyAccCuts=False
plotALL=True#False: solo hhMass (mass o pt)
only2D=True

gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)


def fillHHMass(histo, filename):
    secondPart=False
    startedEvents = False
    p1 = [1,2,3,4]
    #out = open("decayLHE.dat","w")
    for line in open(filename,"r"):
        #if printout : print >>out, line
        #if not startedEvents:
        #    if line.find("<event>")>=0:
        #        startedEvents=True
        #if not startedEvents: continue
        words = line.split()
        if len(words)<10 : continue
        if words[0] != idPart : continue #and words[0] != ("-"+idPart): continue
        #print len(words)
        #for i in range(len(words)):print words[i]
        
        #h=TLorentzVector(float(words[6]),float(words[7]),float(words[8]),float(words[9]))
        #if abs(h.M()-125)>0.0001: print "error mass ",h.M()
        if secondPart:
            #print words[0]
            h1=TLorentzVector(float(words[6]),float(words[7]),float(words[8]),float(words[9])) 
            h2=TLorentzVector(p1[0],p1[1],p1[2],p1[3])
            if fillVar == 0 : histo.Fill((h1+h2).M())
            elif fillVar == 1 :
                histo.Fill(h1.Pt())
                histo.Fill(h2.Pt())
            #print (h1+h2).Pt()
            #print (h1+h2).M()
            #print h1.Px()," ",h1.Py()," ",h1.Pz()," ",h1.Py()
            #print h2.Px()," ",h2.Py()," ",h2.Pz()," ",h2.Pt()
            #print (h1+h2).Px()," ",(h1+h2).Py()," ",(h1+h2).Pz()," ",(h1+h2).Pt()
            secondPart = False
        else :
            p1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
            secondPart = True    


def fillAll(histoHHMass, histPzlow,histPzhigh, histoTheta,histoDRbb, histoDRtt, histoMinDR,filename):
    secondPart=False
    startedEvents = False
    ph1 = []
    pt1=[]
    pt2=[]
    pb1=[]
    pb2=[]
    h1 = TLorentzVector()
    h2 = TLorentzVector()
    t1 = TLorentzVector()
    t2 = TLorentzVector()
    b1 = TLorentzVector()
    b2 = TLorentzVector()
    nBefore = 0 
    nAfter = 0
    nAfterAcc = 0 
    for line in open(filename,"r"):
        if not startedEvents:
            if line.find("<event>")>=0:
                startedEvents=True
        if not startedEvents: continue
        words = line.split()
        if len(words)<10 : continue
        #if words[0] != idPart and words[0] != ("-"+idPart): continue
        #invece che salater, dovrei leggere per ognuna e fillare le cose che mi servono a seconda dell'idPart
        fillH=False
        if words[0] == "25" or words[0] == "-25":
            if len(ph1)>2:
                h1=TLorentzVector(float(words[6]),float(words[7]),float(words[8]),float(words[9])) 
                h2=TLorentzVector(ph1[0],ph1[1],ph1[2],ph1[3])
                #histoHHMass.Fill((h1+h2).M())
                fillH=True
                #ph1.clear()
                ph1 = []
            else :ph1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                
        elif words[0] == "5" or words[0] == "-5":
            if not applyAccCuts and not plotALL : continue
            if len(pb1)>2:
                pb2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                b1=TLorentzVector(pb1[0],pb1[1],pb1[2],pb1[3])
                b2=TLorentzVector(pb2[0],pb2[1],pb2[2],pb2[3])
                #histoDRbb.Fill(b1.DeltaR(b2))
            else: pb1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                
        elif words[0] == "15" or words[0] == "-15":
            if not applyAccCuts and not plotALL : continue
            if len(pt1)>2:
                pt2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                t1=TLorentzVector(pt1[0],pt1[1],pt1[2],pt1[3])
                t2=TLorentzVector(pt2[0],pt2[1],pt2[2],pt2[3])
                #histoDRtt.Fill(t1.DeltaR(t2))
            else: pt1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]

        if (len(pb1)>2 and len(pb2)>2 and len(pt1)>2 and len(pt2)>2) or (not plotALL and fillH and not applyAccCuts) :
            nBefore = nBefore +1 
            if abs(t1.Eta()<0.8) and abs(t2.Eta()<0.8) and abs(b1.Eta()<0.8) and abs(b2.Eta()<0.8) :
                nAfter = nAfter+1
            passCuts = True
            if applyAccCuts :
                if not ( abs(b1.Eta()<2.5) and abs(b2.Eta()<2.5) and abs(t1.Eta()<2.5) and abs(t2.Eta()<2.5) and b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20):
                    passCuts=False
                else : nAfterAcc = nAfterAcc + 1
            #if abs(b1.Eta()<2.5) and abs(b2.Eta()<2.5) and abs(t1.Eta()<2.5) and abs(t2.Eta()<2.5) and b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 and applyAccCuts:
            if passCuts:
                h = [b1,b2,t1,t2]
                if plotALL:
                    mindr=10000
                    for i in range(1,len(h)):
                        if h[0].DeltaR(h[i])<mindr:mindr=h[0].DeltaR(h[i])
                    for i in range(2,len(h)):
                        if h[1].DeltaR(h[i])<mindr:mindr=h[1].DeltaR(h[i])
                    if h[2].DeltaR(h[3])<mindr:mindr=h[2].DeltaR(h[3])
                    histoMinDR.Fill(mindr)
                    histoDRbb.Fill(b1.DeltaR(b2))
                    histoDRtt.Fill(t1.DeltaR(t2))
                if fillVar == 0 : histoHHMass.Fill((h1+h2).M())
                elif fillVar == 1 :
                    histoHHMass.Fill(h1.Pt())
                    histoHHMass.Fill(h2.Pt())
                if h1.Pz()>h2.Pz() :
                    histPzlow.Fill(h2.Pz())
                    histPzhigh.Fill(h1.Pz())
                else:
                    histPzlow.Fill(h1.Pz())
                    histPzhigh.Fill(h2.Pz())
                histoTheta.Fill((h1.Angle(h2.Vect())))
            pt1=[]
            pt2=[]
            pb1=[]
            pb2=[]
    print "Candidates ", nBefore, "in Barrel", nAfter, "in barrel + acc", nAfterAcc


def fillAlland2D(histoHHMass, histPzlow,histPzhigh,histoTheta,histoDRbb, histoDRtt, histoMinDR,histo2D,filename):
    secondPart=False
    startedEvents = False
    ph1 = []
    pt1=[]
    pt2=[]
    pb1=[]
    pb2=[]
    h1 = TLorentzVector()
    h2 = TLorentzVector()
    t1 = TLorentzVector()
    t2 = TLorentzVector()
    b1 = TLorentzVector()
    b2 = TLorentzVector()
    for line in open(filename,"r"):
        if not startedEvents:
            if line.find("<event>")>=0:
                startedEvents=True
        if not startedEvents: continue
        words = line.split()
        if len(words)<10 : continue
        #if words[0] != idPart and words[0] != ("-"+idPart): continue
        #invece che salater, dovrei leggere per ognuna e fillare le cose che mi servono a seconda dell'idPart
        fillH=False
        if words[0] == "25" or words[0] == "-25":
            if len(ph1)>2:
                h1=TLorentzVector(float(words[6]),float(words[7]),float(words[8]),float(words[9])) 
                h2=TLorentzVector(ph1[0],ph1[1],ph1[2],ph1[3])
                #histoHHMass.Fill((h1+h2).M())
                fillH=True
                #ph1.clear()
                ph1 = []
            else :ph1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                
        elif words[0] == "5" or words[0] == "-5":
            if not applyAccCuts and not plotALL : continue
            if len(pb1)>2:
                pb2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                b1=TLorentzVector(pb1[0],pb1[1],pb1[2],pb1[3])
                b2=TLorentzVector(pb2[0],pb2[1],pb2[2],pb2[3])
                #histoDRbb.Fill(b1.DeltaR(b2))
            else: pb1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                
        elif words[0] == "15" or words[0] == "-15":
            if not applyAccCuts and not plotALL : continue
            if len(pt1)>2:
                pt2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                t1=TLorentzVector(pt1[0],pt1[1],pt1[2],pt1[3])
                t2=TLorentzVector(pt2[0],pt2[1],pt2[2],pt2[3])
                #histoDRtt.Fill(t1.DeltaR(t2))
            else: pt1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]

        if (len(pb1)>2 and len(pb2)>2 and len(pt1)>2 and len(pt2)>2) or (not plotALL and fillH and not applyAccCuts) :
            passCuts = True
            h = [b1,b2,t1,t2]
            if applyAccCuts :
                if not ( abs(b1.Eta()<2.5) and abs(b2.Eta()<2.5) and abs(t1.Eta()<2.5) and abs(t2.Eta()<2.5) and b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20):
                    passCuts=False
            #if abs(b1.Eta()<2.5) and abs(b2.Eta()<2.5) and abs(t1.Eta()<2.5) and abs(t2.Eta()<2.5) and b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 and applyAccCuts:
            if passCuts:
                if plotALL:
                    mindr=10000
                    for i in range(1,len(h)):
                        if h[0].DeltaR(h[i])<mindr:mindr=h[0].DeltaR(h[i])
                    for i in range(2,len(h)):
                        if h[1].DeltaR(h[i])<mindr:mindr=h[1].DeltaR(h[i])
                    if h[2].DeltaR(h[3])<mindr:mindr=h[2].DeltaR(h[3])
                    histoMinDR.Fill(mindr)
                    histoDRbb.Fill(b1.DeltaR(b2))
                    histoDRtt.Fill(t1.DeltaR(t2))
                if fillVar == 0 : histoHHMass.Fill((h1+h2).M())
                elif fillVar == 1 :
                    histoHHMass.Fill(h1.Pt())
                    histoHHMass.Fill(h2.Pt())
                #if abs(h1.M()-(b1+b2).M()<0.0001): #h1->bb, h2->tt
                    #histo2D.Fill((h1+h2).M()/h1.Pt(),b1.DeltaR(b2))
                    #histo2D.Fill((h1+h2).M()/h2.Pt(),t1.DeltaR(t2))
                    #histo2D.Fill(h1.Pt(),b1.DeltaR(b2))
                    #histo2D.Fill(h2.Pt(),t1.DeltaR(t2))
                #else:
                    #histo2D.Fill((h1+h2).M()/h1.Pt(),t1.DeltaR(t2))
                    #histo2D.Fill((h1+h2).M()/h2.Pt(),b1.DeltaR(b2))
                    #histo2D.Fill(h1.Pt(),t1.DeltaR(t2))
                    #histo2D.Fill(h2.Pt(),b1.DeltaR(b2))
                #histo2D.Fill(1./h1.Pt(),mindr)
                #histo2D.Fill(1./h2.Pt(),mindr)
                histo2D.Fill(h1.M(),h2.M())
                #histo2D.Fill(1./h2.Pt(),mindr)
                if h1.Pz()>h2.Pz() :
                    histPzlow.Fill(h2.Pz())
                    histPzhigh.Fill(h1.Pz())
                else:
                    histPzlow.Fill(h1.Pz())
                    histPzhigh.Fill(h2.Pz())
                histoTheta.Fill((h1+h2).Theta())
            pt1=[]
            pt2=[]
            pb1=[]
            pb2=[]



nBins=200    
histlist = []
histlistbb = []
histlisttt = []
histlistDR = []
#hist2D = TH2F("minDeltaR vs M/pt "+names[run2D],"minDeltaR vs M/pt "+"#lambda="+names[run2D],100,0,0.05,200,0,3.5)#1000 for pt, 5 for Dr
hist2D = TH2F("minDeltaR vs M/pt "+names[run2D],"minDeltaR vs M/pt "+"#lambda="+names[run2D],100,110,800,100,110,800)#1000 for pt, 5 for Dr
histPzlow = []
histPzhigh = []
histTheta = []

if len(colors)<len(names):
    for k in range(len(colors),len(names)): colors.append(kBlue+k)
if len(styles)<len(names):
    for k in range(len(styles),len(names)): styles.append(1)
if len(fills)<len(names):
    for k in range(len(fills),len(names)): fills.append(0)
for i in range(len(runlist)):
    print "running lambda=",names[i]
    if fillVar == 0:
        appendLeg = "hh mass "
        start=250
        end = 600
    elif fillVar == 1 :
        appendLeg = "h p_{t} "
        start=0
        end=700
    histlist.append(TH1F(appendLeg+names[i],appendLeg+"#lambda="+names[i],nBins,start,end))
    histPzlow.append(TH1F("Pz_{min} "+names[i],"Pz_{min} #lambda="+names[i],nBins+100,-2000,1000))
    histPzhigh.append(TH1F("Pz_{max} "+names[i],"Pz_{max} #lambda="+names[i],nBins+100,-1000,2000))
    histTheta.append(TH1F("h_{#theta} "+names[i],"h_{#theta} #lambda="+names[i],nBins,0,TMath.Pi()+0.06))
    histlistbb.append(TH1F("DeltaR bb "+names[i],"DeltaR bb #lambda="+names[i],200,0,5))
    histlisttt.append(TH1F("DeltaR tt "+names[i],"DeltaR tt #lambda="+names[i],200,0,5))
    histlistDR.append(TH1F("min DR "+names[i],"minDR #lambda="+names[i],150,0,4))
    
    if plotALL or applyAccCuts:
        if run2D == i : fillAlland2D(histlist[i],histPzlow[i],histPzhigh[i],histTheta[i],histlistbb[i],histlisttt[i],histlistDR[i],hist2D,"run_"+runlist[i]+"/dec_events.lhe")
        elif not only2D:  fillAll(histlist[i],histPzlow[i],histPzhigh[i],histTheta[i],histlistbb[i],histlisttt[i],histlistDR[i],"run_"+runlist[i]+"/dec_events.lhe")
    else : fillHHMass(histlist[i],"run_"+runlist[i]+"/dec_events.lhe")
    print "nentries lambda ",names[i]," = ",histlist[i].GetEntries()
    histlist[i].SetLineColor(colors[i])
    histlistbb[i].SetLineColor(colors[i])
    histlisttt[i].SetLineColor(colors[i])
    histlistDR[i].SetLineColor(colors[i])
    histlist[i].SetLineStyle(styles[i])
    histlistbb[i].SetLineStyle(styles[i])
    histlisttt[i].SetLineStyle(styles[i])
    histlistDR[i].SetLineStyle(styles[i])
    histlist[i].SetFillStyle(fills[i])
    histlistbb[i].SetFillStyle(fills[i])
    histlisttt[i].SetFillStyle(fills[i])
    histlistDR[i].SetFillStyle(fills[i])
    #histlist[i].SetLineWidth(1)
    
    histPzlow[i].SetLineColor(colors[i])
    #histPzlow[i].SetLineStyle(3)
    histPzhigh[i].SetLineColor(colors[i])
    histTheta[i].SetLineStyle(styles[i])
    histTheta[i].SetLineColor(colors[i])
    #histlistbb[i].SetLineWidth(1.5)
    #histlisttt[i].SetLineWidth(1.5)
    #histlistDR[i].SetLineWidth(1.5)
    
#histo  = TH1F("mass hh ","mass hh #lambda=1",100,200,800)
#histo2 = TH1F("mass hh2","mass hh #lambda=2.46",100,200,800)
#histo3 = TH1F("mass hh3","mass hh #lambda=4",100,200,800)
#fillHHMass(histo,"run_02/unweighted_events.lhe")
#fillHHMass(histo2,"run_03/unweighted_events.lhe")
#fillHHMass(histo3,"run_04/events.lhe")
#histo2.SetLineColor(2)
#histo3.SetLineColor(kBlack)


gStyle.SetOptStat(0)
if fillVar == 0 : outName+="_M"
elif fillVar == 1 : outName+="_Pt"
if plotALL and not only2D: outName += "_all"
if plotALL and only2D: outName += "_minDR"
if applyAccCuts : outName += "_wcuts"
    
if not only2D:
    c = TCanvas("c","c")
    if plotALL:
        c.Divide(2,2)
    c.cd(1)
    #histo3.DrawNormalized()
    #histo2.DrawNormalized("SAME")
    #histo.DrawNormalized("SAME")
    #histlist[4].DrawNormalized()
    maximum=-1
    for i in range(len(runlist)):
        print "integral ",histlist[i].Integral()," nentries: ",histlist[i].GetEntries()
        maxi=histlist[i].GetMaximum()/histlist[i].Integral()
        if maxi>maximum:maximum=maxi
    print maximum
    for i in range(len(runlist)):
        #histlist[i].GetYaxis().SetRangeUser(0.0001,maximum+0.005)
        temph = histlist[i].DrawNormalized("SAME")
        temph.GetYaxis().SetRangeUser(0.000001,maximum+0.005)
        temph.GetYaxis().SetTitle("a. u.")
        if fillVar == 0 : temph.GetXaxis().SetTitle("hh Mass")
        else : temph.GetXaxis().SetTitle("p_{t}(h)")
        #histlist[i].GetYaxis().SetRangeUser(0.000001,maximum+0.005)
    legend=c.cd(1).BuildLegend()
    legend.SetFillStyle(0)
    legend.SetLineColor(0)
    if plotALL:
        c.cd(2)
        for i in range(len(runlist)):
            histlisttt[i].DrawNormalized("SAME")
        c.cd(3)
        for i in range(len(runlist)):
            histlistbb[i].DrawNormalized("SAME")
        c.cd(4)
        for i in range(len(runlist)):
            histlistDR[i].DrawNormalized("SAME")
#c.SaveAs("c.root")
    c.SaveAs(outName+".root")
    c.SaveAs(outName+".pdf")

    if plotALL:
        cpz=TCanvas("cpzlow","cpzlow")
        cpz.cd()
        maximum=-1
        for i in range(len(runlist)):
            maxi=histPzlow[i].GetMaximum()/histPzlow[i].Integral()
            if maxi>maximum:maximum=maxi
                
        for i in range(len(runlist)):
            temph = histPzlow[i].DrawNormalized("SAME")
            temph.GetYaxis().SetRangeUser(0.000001,maximum+0.005)
            temph.GetXaxis().SetTitle("P_{z}")
        leg=cpz.BuildLegend()
        leg.SetLineColor(0)
        leg.SetFillStyle(0)
        cpz.SaveAs(outName+"_pzlow.root")
        cpz.SaveAs(outName+"_pzlow.pdf")
    
        cpzh=TCanvas("cpzh","cpzh")
        cpzh.cd()
        maximum=-1
        for i in range(len(runlist)):
            maxi=histPzhigh[i].GetMaximum()/histPzhigh[i].Integral()
            if maxi>maximum:maximum=maxi
        
        for i in range(len(runlist)):
            temph2 = histPzhigh[i].DrawNormalized("SAME")
            temph2.GetYaxis().SetRangeUser(0.000001,maximum+0.005)
            temph2.GetXaxis().SetTitle("P_{z}")
        legh=cpzh.BuildLegend()
        legh.SetLineColor(0)
        legh.SetFillStyle(0)
        cpzh.SaveAs(outName+"_pzhigh.root")
        cpzh.SaveAs(outName+"_pzhigh.pdf")

        cth=TCanvas("cth","cth")
        cth.cd()
        maximum=-1
        for i in range(len(runlist)):
            maxi=histTheta[i].GetMaximum()/histTheta[i].Integral()
            if maxi>maximum:maximum=maxi
        
        for i in range(len(runlist)):
            temph2 = histTheta[i].DrawNormalized("SAME")
            temph2.GetYaxis().SetRangeUser(0.000001,maximum+0.005)
            temph2.GetXaxis().SetTitle("h_{#theta}")
        legt=cth.BuildLegend()
        legt.SetLineColor(0)
        legt.SetFillStyle(0)
        cth.SaveAs(outName+"_theta.root")
        cth.SaveAs(outName+"_theta.pdf")


c2D=TCanvas("c2d","c2d")
c2D.cd()
hist2D.Draw("COLZ")
#hist2D.GetXaxis().SetTitle("M_{hh}/p_{t}(h)")
hist2D.GetXaxis().SetTitle("p^{-1}_{t}(h)")
hist2D.GetYaxis().SetTitle("min #Delta R (final products)")
c2D.SaveAs(outName+"_scatter_pt.root")
c2D.SaveAs(outName+"_scatter_pt.pdf")


    
