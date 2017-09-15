#!/usr/bin/python -tt
  #     25    1    1    2    0    0  0.35960409498E+02 -0.53973850759E+02 -0.95711389391E+03  0.96741838598E+03  0.12500000000E+03 0.  0.

import sys
import urllib2
import ROOT
from ROOT import * #TFile,TDirectory,TH2F,TString,TCanvas, RooFit

secondPart=False
startedEvents = False
pt1=[]
pt2=[]
pb1=[]
pb2=[]
ph1 = []
h1 = TLorentzVector()
h2 = TLorentzVector()
t1 = TLorentzVector()
t2 = TLorentzVector()
b1 = TLorentzVector()
b2 = TLorentzVector()
nTot =0
nTotPt =0
nTotEta =0
nTotEta4 =0
nTotEtaPt = 0
nTotEta4Pt = 0
nBarrelPt = 0
nBarrel = 0

for line in open("run_09/dec_events.lhe","r"):
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
        if len(pb1)>2:
            pb2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
            b1=TLorentzVector(pb1[0],pb1[1],pb1[2],pb1[3])
            b2=TLorentzVector(pb2[0],pb2[1],pb2[2],pb2[3])
            #histoDRbb.Fill(b1.DeltaR(b2))
        else: pb1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
                
    elif words[0] == "15" or words[0] == "-15":
        if len(pt1)>2:
            pt2 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]
            t1=TLorentzVector(pt1[0],pt1[1],pt1[2],pt1[3])
            t2=TLorentzVector(pt2[0],pt2[1],pt2[2],pt2[3])
        else : pt1 = [float(words[6]),float(words[7]),float(words[8]),float(words[9])]

    if (len(pb1)>2 and len(pb2)>2 and len(pt1)>2 and len(pt2)>2):
        #print "found Event"
        nTot = nTot + 1
        if b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 :
            nTotPt = nTotPt +1
        else :
            #print "discarded",  b1.Pt(),  b2.Pt(),  t1.Pt(),  t2.Pt()
            pt1=[]
            pt2=[]
            pb1=[]
            pb2=[]
            continue
        if abs(t1.Eta()<0.9) and abs(t2.Eta()<0.9) and abs(b1.Eta()<0.9) and abs(b2.Eta()<0.9) :
            #print "found passed event"
            nBarrel = nBarrel + 1         
            if b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 :
                nBarrelPt = nBarrelPt +1
        if abs(t1.Eta()<2.3) and abs(t2.Eta()<2.3) and abs(b1.Eta()<2.3) and abs(b2.Eta()<2.3) :
            #print "found passed event"
            nTotEta = nTotEta + 1         
            if b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 :
                nTotEtaPt = nTotEtaPt +1
        if abs(t1.Eta()<4) and abs(t2.Eta()<4) and abs(b1.Eta()<4) and abs(b2.Eta()<4) :
            #print "found passed event"
            nTotEta4 = nTotEta4 + 1         
            if b1.Pt()>20 and b2.Pt()>20 and t1.Pt()>20 and t2.Pt()>20 :
                nTotEta4Pt = nTotEta4Pt +1
        pt1=[]
        pt2=[]
        pb1=[]
        pb2=[]
print "all", nTot,"in acc", nTotEta, "in barrel", nBarrel, "fino a 4", nTotEta4
print "asking pt"
print "all", nTotPt,"in acc", nTotEtaPt, "in barrel", nBarrelPt,  "fino a 4", nTotEta4Pt



