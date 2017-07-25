using namespace RooFit;
void plotfromWS(){
  gSystem->Load("$CMSSW_BASE/lib/slc5_amd64_gcc472/libHiggsAnalysisCombinedLimit.so");
  TFile *f = TFile::Open("cards_03_05_Unblind_093_2D/HCG/220/hzz4l_2e2muS_8TeV.input.root");
  TFile *fK = TFile::Open("cards_093_AlternativeKBKG/HCG/220/hzz4l_2e2muS_8TeV.input.root");
  //TFile *f = TFile::Open("cards_03_05_Unblind_093_2D/HCG/220/hzz4l_allS_8TeV.root");
  //TFile *fK = TFile::Open("cards_093_AlternativeKBKG/HCG/220/hzz4l_allS_8TeV.root");
  RooWorkspace *wK =(RooWorkspace*)fK->Get("w");
  RooWorkspace *w =(RooWorkspace*)f->Get("w");
  //RooAbsPdf* s = w->pdf("ggzz");
  //RooAbsPdf* sK = wK->pdf("ggzz");
  RooSimultaneous* s = w->pdf("model_s");
  RooSimultaneous* sK = wK->pdf("model_s");

  RooRealVar *m4l = w->var("CMS_zz4l_widthMass");
  RooCategory *cat = w->cat("CMS_channel");
  RooArgSet *set = w->set("ModelConfig_Observables");
  RooAbsData *data_obs= w->data("data_obs");

  m4l->setBins(25000);
  m4l->setRange(220,800);
  RooPlot* plot = m4l->frame();
  //  RooAbsData* projData = new RooDataHist("projDataWMixH","projDataWMixH",*set,data_obs);
  RooPlot *plots = s->plotOn(plot,Name("kone"),FillStyle(0),RooFit::ProjWData(*cat,set));
  RooPlot *plotsk= sK->plotOn(plot,LineColor(kRed+1),Name("knew"),FillStyle(0),RooFit::ProjWData(*cat,set));
  TCanvas *c1 =  new TCanvas();
  plot->Draw();
  TLegend *leg = new TLegend(0.5,0.5,0.8,0.8);
  leg->SetFillStyle(0);
  leg->SetLineColor(0);
  leg->AddEntry("kone","ggZZ, 2e2#mu, K=1","l");
  leg->AddEntry("knew","ggZZ, 2e2#mu, K=1/2.8","l");
  leg->Draw();
  c1->SetLogy();
}
