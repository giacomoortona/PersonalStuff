from ROOT import *

colors68 = [kRed-7,kYellow,kOrange-3]
colors95 = [kBlue,kGreen,kYellow-8]
offset = 0.04

def doboxes(canvas,colors,mover=0,nboxes=3):
	canvas.cd()
	startX = 0.3
	Y = 0.2+mover
	box=[]
	for i in range(nboxes):
		print i
		string = ""
		box.append(TBox(startX+offset*i,Y,startX+offset*(i+1),Y+offset))
		box[i].SetFillColor(colors[i])
		#if i>0 : string = "SAME"
		#box.Draw(string)
	return box

def doboxes95(canvas,nboxes=3):
	return doboxes(canvas,colors95,offset*2,nboxes)

def doboxes68(canvas,nboxes=3):
	return doboxes(canvas,colors68,0,nboxes)



c = TCanvas("c","c")
box68 = doboxes68(c)
box95 = doboxes95(c)
string = ""
for i in range(len(box68)):
	if i>0 : string = "SAME"
	box68[i].Draw(string)
	box95[i].Draw("SAME")

text68 = TPaveText(box68[len(box68)-1].GetX2(),box68[0].GetY1(),box68[len(box68)-1].GetX2()+0.2,box68[0].GetY2(),"NDC")
text68.AddText("68% expected limit")
text68.SetFillColor(0)
text68.Draw("SAME")

text95 = TPaveText(box95[len(box95)-1].GetX2(),box95[0].GetY1(),box95[len(box95)-1].GetX2()+0.2,box95[0].GetY2(),"NDC")
text95.AddText("95% expected limit")
text95.SetFillColor(0)
text95.Draw("SAME")


hobs = TH1F("hobs","hobs",100,0,1)
hobs.SetMarkerStyle(20)
hexp = TH1F("hexp","hexp",100,0,1)
hexp.SetMarkerStyle(24)
leg = TLegend(box68[0].GetX1()-0.2,box68[0].GetY1()-0.0126,box95[0].GetX1(),box95[0].GetY2()+0.0126)
leg.SetFillColor(0)
leg.SetLineStyle(0)
leg.SetLineColor(0)
leg.AddEntry(hobs,"Observed","p")
leg.AddEntry(hexp,"Expected","p")
leg.Draw("SAME")


c.Update()
c.SaveAs("c.pdf")
raw_input("Press enter to continue...")
