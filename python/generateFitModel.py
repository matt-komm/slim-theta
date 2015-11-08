


from ModelClasses import *
from optparse import OptionParser
import math
import sys
import os
import logging
import copy
import random

import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)

setDict = {
    "tChan":{
        "folders":["iso/nominal/T_t","iso/nominal/Tbar_t"],
        "weight":"1.0"
    },
    "DY":{
        "folders":["iso/nominal/DYJets"],
        "weight":"1.0"
    },
    "sChan":{
        "folders":["iso/nominal/T_s","iso/nominal/Tbar_s"],
        "weight":"1.0"
    },
    "tWChan":{
        "folders":["iso/nominal/T_tW","iso/nominal/Tbar_tW"],
        "weight":"1.0"
    },
    "tChanLeptons":{
        "folders":["iso/nominal/T_t_ToLeptons","iso/nominal/Tbar_t_ToLeptons"],
        "weight":"1.0"
    },
    "TTJetsDi":{
        "folders":["iso/nominal/TTJets_FullLept"],
        "weight":"(top_weight)"
    },
    "TTJetsSemi":{
        "folders":["iso/nominal/TTJets_SemiLept"],
        "weight":"(top_weight)"
    },
    "TTJetsFull":{
        "folders":["iso/nominal/TTJets_MassiveBinDECAY"],
        "weight":"(top_weight)"
    },
    "WJetsExclBF":{
        "folders":["iso/nominal/W1Jets_exclusive","iso/nominal/W2Jets_exclusive","iso/nominal/W3Jets_exclusive","iso/nominal/W4Jets_exclusive"],
        #"weight":"(fabs(ljet_id)==5 || fabs(bjet_id)==5 || fabs(sjet1_id)==5 || fabs(sjet2_id)==5)"
        "weight":"(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)"
    },
    "WJetsExclCF":{
        "folders":["iso/nominal/W1Jets_exclusive","iso/nominal/W2Jets_exclusive","iso/nominal/W3Jets_exclusive","iso/nominal/W4Jets_exclusive"],
        #"weight":"((fabs(ljet_id)!=5 && fabs(bjet_id)!=5 && fabs(sjet1_id)!=5 && fabs(sjet2_id)!=5) && (fabs(ljet_id)==4 || fabs(bjet_id)==4 || fabs(sjet1_id)==4 || fabs(sjet2_id)==4))"
        "weight":"((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))"
    },
    "WJetsExclLF":{
        "folders":["iso/nominal/W1Jets_exclusive","iso/nominal/W2Jets_exclusive","iso/nominal/W3Jets_exclusive","iso/nominal/W4Jets_exclusive"],
        #"weight":"(fabs(ljet_id)!=5 && fabs(bjet_id)!=5 && fabs(sjet1_id)!=5 && fabs(sjet2_id)!=5 && fabs(ljet_id)!=4 && fabs(bjet_id)!=4 && fabs(sjet1_id)!=4 && fabs(sjet2_id)!=4)"
        "weight":"(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)"
    },
    "DiBoson":{
        "folders":["iso/nominal/WW","iso/nominal/WZ","iso/nominal/ZZ"],
        "weight":"1.0"
    },
    
    
    
    
    "tChanAntiiso":{
        "folders":["antiiso/nominal/T_t","antiiso/nominal/Tbar_t"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "DYAntiiso":{
        "folders":["antiiso/nominal/DYJets"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "sChanAntiiso":{
        "folders":["antiiso/nominal/T_s","antiiso/nominal/Tbar_s"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "tWChanAntiiso":{
        "folders":["antiiso/nominal/T_tW","antiiso/nominal/Tbar_tW"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "tChanLeptonsAntiiso":{
        "folders":["antiiso/nominal/T_t_ToLeptons","antiiso/nominal/Tbar_t_ToLeptons"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "TTJetsDiAntiiso":{
        "folders":["antiiso/nominal/TTJets_FullLept"],
        "weight":"(-1.0)*(top_weight)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "TTJetsSemiAntiiso":{
        "folders":["antiiso/nominal/TTJets_SemiLept"],
        "weight":"(-1.0)*(top_weight)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "TTJetsFullAntiiso":{
        "folders":["antiiso/nominal/TTJets_MassiveBinDECAY"],
        "weight":"(-1.0)*(top_weight)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "WJetsExclBFAntiiso":{
        "folders":["antiiso/nominal/W1Jets_exclusive","antiiso/nominal/W2Jets_exclusive","antiiso/nominal/W3Jets_exclusive","antiiso/nominal/W4Jets_exclusive"],
        #"weight":"(fabs(ljet_id)==5 || fabs(bjet_id)==5 || fabs(sjet1_id)==5 || fabs(sjet2_id)==5)"
        "weight":"(-1.0)*(abs(ljet_id)==5 || abs(bjet_id)==5 || abs(sjet1_id)==5 || abs(sjet2_id)==5)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "WJetsExclCFAntiiso":{
        "folders":["antiiso/nominal/W1Jets_exclusive","antiiso/nominal/W2Jets_exclusive","antiiso/nominal/W3Jets_exclusive","antiiso/nominal/W4Jets_exclusive"],
        #"weight":"((fabs(ljet_id)!=5 && fabs(bjet_id)!=5 && fabs(sjet1_id)!=5 && fabs(sjet2_id)!=5) && (fabs(ljet_id)==4 || fabs(bjet_id)==4 || fabs(sjet1_id)==4 || fabs(sjet2_id)==4))"
        "weight":"(-1.0)*((abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5) && (abs(ljet_id)==4 || abs(bjet_id)==4 || abs(sjet1_id)==4 || abs(sjet2_id)==4))*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "WJetsExclLFAntiiso":{
        "folders":["antiiso/nominal/W1Jets_exclusive","antiiso/nominal/W2Jets_exclusive","antiiso/nominal/W3Jets_exclusive","antiiso/nominal/W4Jets_exclusive"],
        #"weight":"(fabs(ljet_id)!=5 && fabs(bjet_id)!=5 && fabs(sjet1_id)!=5 && fabs(sjet2_id)!=5 && fabs(ljet_id)!=4 && fabs(bjet_id)!=4 && fabs(sjet1_id)!=4 && fabs(sjet2_id)!=4)"
        "weight":"(-1.0)*(abs(ljet_id)!=5 && abs(bjet_id)!=5 && abs(sjet1_id)!=5 && abs(sjet2_id)!=5 && abs(ljet_id)!=4 && abs(bjet_id)!=4 && abs(sjet1_id)!=4 && abs(sjet2_id)!=4)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "DiBosonAntiiso":{
        "folders":["antiiso/nominal/WW","antiiso/nominal/WZ","antiiso/nominal/ZZ"],
        "weight":"(-1.0)*pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700"
    },
    "QCDMu":{
        "folders":["antiiso/data/SingleMu"],
        "weight":"1.0"
    },
    "QCDEle":{
        "folders":["antiiso/data/SingleEle"],
        "weight":"1.0"
    },
    
    
    
    "SingleMu":{
        "folders":["iso/data/SingleMu"],
        "weight":"1.0"
    },
    "SingleEle":{
        "folders":["iso/data/SingleEle"],
        "weight":"1.0"
    }
}

for sample in setDict.keys():
    setDict[sample]["files"]=[]
    setDict[sample]["weights"]=[]
    for folder in setDict[sample]["folders"]:
        path = os.path.join(os.getcwd(),"skimmed/Apr21/output/Apr21_btags",folder)
        
        for root, dirs, files in os.walk(path):
            for file in files:
                #print os.path.join(root,file)
                
                if file.endswith(".root"):
                    datafile=os.path.join(root,file)
                    weightfile=os.path.join(root,file+".added")
                    if os.path.exists(weightfile):
                        setDict[sample]["files"].append(datafile)
                        setDict[sample]["weights"].append(weightfile)
                    else:
                        print "weight file not found ",weightfile
    if len(setDict[sample]["files"])==len(setDict[sample]["weights"]):
        print "found ... ",sample,"...",len(setDict[sample]["files"])," files"
    else:
        print "ERROR"

def generateModel(modelName="fit",
                    prefix="",
                    dataDict={},
                    histSetDict={},
                    uncertaintyDict={},
                    binning=1,
                    ranges=[-1.0,1.0],
                    dicePoisson=True,
                    mcUncertainty=True):
    
    file=open(modelName+".cfg", "w")
    
    model=Model(modelName)
    if mcUncertainty:
        model=Model(modelName, {"bb_uncertainties":"true"})

    for uncertainty in uncertaintyDict.keys():
        uncertaintyDict[uncertainty]["dist"]=Distribution(uncertainty, uncertaintyDict[uncertainty]["type"], uncertaintyDict[uncertainty]["config"])
        file.write(uncertaintyDict[uncertainty]["dist"].toConfigString())
    
    
    varName = "bdt_sig_bg"
    
    
    
    dataStacks={}
    mcStacks={}
    
    for observable in dataDict.keys():
    
        dataStack = ROOT.THStack()
        dataStacks[observable]=dataStack
        histoadd = HistoAdd(observable+"__data")
        
        for component in dataDict[observable].keys():
            dataWeight=dataDict[observable][component]["weight"]
            
            componentHist = ROOT.TH1F(component+"__"+observable+"_data","",binning,ranges[0],ranges[1])
            componentHist.Sumw2()
            componentHist.SetLineColor(1)
            componentHist.SetLineWidth(2)
            componentHist.SetMarkerColor(1)
            componentHist.SetMarkerStyle(20)
            componentHist.SetMarkerSize(1.2)
            componentHist.SetDirectory(0)
            for setName in dataDict[observable][component]["sets"]:
                dataFiles = setDict[setName]["files"]
                weightFiles = setDict[setName]["weights"]
                for fileindex in range(len(dataFiles)):
                    datafile=dataFiles[fileindex]
                    weightfile=weightFiles[fileindex]
                    hist=RootProjectedHistogram(component+"__"+observable+"__"+setName+"__data__"+str(fileindex),{"use_errors":"true"})
                    hist.setFileName(datafile)
                    hist.addFriend(weightfile)
                    hist.setVariableString(varName)
                    hist.setWeightString(dataWeight)
                    hist.setTreeName("dataframe")
                    hist.setBinning(binning)
                    hist.setRange(ranges)
                    file.write(hist.toConfigString())
                    histoadd.addHisto(hist.getVarname())
                    
                   
                    
                    f = ROOT.TFile(datafile)
                    print observable,datafile
                    print dataWeight
                    tempHist = ROOT.TH1F(component+"__"+observable+"__"+setName+"__data__"+str(fileindex),"",binning,ranges[0],ranges[1])
                    tempHist.Sumw2()
                    tree = f.Get("dataframe")
                    tree.AddFriend("dataframe",weightfile)
                    tree.Project(tempHist.GetName(),varName,dataWeight)
                    tempHist.SetDirectory(0)
                    componentHist.Add(tempHist)
                    #break
            dataStack.Add(componentHist,"HIST PE")

                    
        file.write(histoadd.toConfigString())
        #break
        

    for observable in histSetDict.keys():
        mcStack = ROOT.THStack()
        mcStacks[observable]=mcStack
        
        obs=Observable(prefix+observable, binning, ranges)
        for component in histSetDict[observable].keys():
            compWeight = histSetDict[observable][component]["weight"]
            
            componentHist = ROOT.TH1F(component+"__"+observable+"_data","",binning,ranges[0],ranges[1])
            componentHist.SetLineColor(histSetDict[observable][component]["color"])
            componentHist.SetFillColor(histSetDict[observable][component]["color"])
            componentHist.SetFillStyle(1001)
            componentHist.SetDirectory(0)
            for setName in histSetDict[observable][component]["sets"]:
                files = setDict[setName]["files"]
                weights = setDict[setName]["weights"]
                setWeight =setDict[setName]["weight"]
                for fileindex in range(len(files)):
                    datafile=files[fileindex]
                    weightfile=weights[fileindex]
                    comp=ObservableComponent(component+"__"+observable+"__"+setName+"__"+str(fileindex))
                    coeff=CoefficientMultiplyFunction()
                    for uncertaintyName in histSetDict[observable][component]["uncertainties"]:
                        dist = uncertaintyDict[uncertaintyName]["dist"]
                        coeff.addDistribution(dist,dist.getParameterName())
                    comp.setCoefficientFunction(coeff)
                    
                    hist=RootProjectedHistogram(observable+"__"+component+"__"+setName+"__"+str(fileindex),{"use_errors":"true"})
                    hist.setFileName(datafile)
                    hist.addFriend(weightfile)
                    hist.setVariableString(varName)
                    hist.setWeightString(setWeight+"*"+compWeight)
                    hist.setTreeName("dataframe")
                    hist.setBinning(binning)
                    hist.setRange(ranges)
                    file.write(hist.toConfigString())
                    comp.setNominalHistogram(hist)
                
                    obs.addComponent(comp)
                    
                    
                    f = ROOT.TFile(datafile)
                    print observable,datafile
                    print setWeight+"*"+compWeight
                    tempHist = ROOT.TH1F(observable+"__"+component+"__"+setName+"__"+str(fileindex),"",binning,ranges[0],ranges[1])
                    tree = f.Get("dataframe")
                    tree.AddFriend("dataframe",weightfile)
                    tree.Project(tempHist.GetName(),varName,setWeight+"*"+compWeight)
                    tempHist.SetDirectory(0)
                    componentHist.Add(tempHist)
                #break
            for ibin in range(binning):
                componentHist.SetBinContent(ibin+1,max(0,componentHist.GetBinContent(ibin+1)))
            mcStack.Add(componentHist,"HIST")

            
        model.addObservable(obs)
        #break
    
        
    
   
    file.write(model.toConfigString())
    _writeFile(file,model,modelName,dicePoisson=dicePoisson,mcUncertainty=mcUncertainty)
    file.close()
    
    
    for observable in mcStacks.keys():
        cv = ROOT.TCanvas("cv_"+observable,"",800,600)
        ymax=max(mcStacks[observable].GetMaximum(),dataStacks[observable].GetMaximum())
        axis=ROOT.TH2F("axis"+observable,";BDT_{W,t #bar t};events",50,ranges[0],ranges[1],50,0,ymax*1.15)
        axis.Draw("AXIS")
        mcStacks[observable].Draw("Same")
        dataStacks[observable].Draw("Same")
        pave = ROOT.TPaveText(0.5,0.91,0.9,0.99,"NDC")
        pave.SetFillColor(ROOT.kWhite)
        pave.SetTextFont(42)
        pave.AddText(observable)
        pave.Draw("Same")
        axis.Draw("AXIS Same")
        cv.Print(observable+".pdf")
        cv.WaitPrimitive()
        
    
    
                    
                    
def _writeFile(file,model,modelName,dicePoisson=True,mcUncertainty=True,experiments=1): 

    file.write("\n")
    file.write("\n")
    
    file.write("myminimizer = {\n")

    file.write("type = \"newton_minimizer\";\n")
    file.write("//par_eps = 1e-6; // optional; default is 1e-4'\n")
    file.write("//maxit = 100000; // optional; default is 10,000'\n")
    file.write("//improve_cov = true; // optional; default is false'\n")
    file.write("//force_cov_positive = true; // optional, default is false'\n")
    file.write("//step_cov = 0.01; // optional; default is 0.1'\n")
    '''
    file.write("type = \"root_minuit\";\n")
    file.write("method = \"migrad\"; //optional. Default is 'migrad'\n")
    file.write("tolerance_factor = 0.1; //optional. Default is 1\n")
    file.write("max_iterations = 10000; // optional. Default as in ROOT::Minuit2\n")
    file.write("max_function_calls = 100000; //optional. Default as in ROOT::Minuit2\n")
    file.write("n_retries = 20; // optional; the default is 2\n")
    
    file.write("type = \"mcmc_minimizer\";\n")
    file.write("name = \"min0\";\n")
    file.write("iterations = 10000;\n")
    file.write("burn-in = 500; //optional. default is iterations / 10\n")
    file.write("stepsize_factor = 0.1; //optional, default is 1.0\n")
    '''
    file.write("};\n")
    
    file.write('pd = {\n')
    file.write('    name= "fit";\n')
    file.write('    type = "mle";\n')
    file.write('    parameters = ('+model.getParameterNames()+');\n')
    file.write('    minimizer = \"@myminimizer\";\n')
    file.write('    write_covariance = true;\n')
    file.write('};\n')
    
    file.write('main={\n')
    
    file.write('    data_source={\n')
    file.write('        type="histo_source";\n')
    file.write('        name="data";\n')
    
    file.write('        obs_2j1t="@histoadd_2j1t__data";\n')
    #file.write('        obs_2j0t="@histoadd_2j0t__data";\n')
    #file.write('        obs_3j1t="@histoadd_3j1t__data";\n')
    file.write('        obs_3j2t="@histoadd_3j2t__data";\n')
    file.write('    };\n')
    
    '''
    file.write('    data_source={\n')
    file.write('    type="model_source";\n')
    file.write('    model="@model_'+modelName+'";\n')
    file.write('    name="source";\n')
    if dicePoisson:
        file.write('    dice_poisson=true;\n')
    else:
        file.write('    dice_poisson=false;\n')
    if mcUncertainty:    
        file.write('    dice_template_uncertainties = true;\n')
    else:
        file.write('    dice_template_uncertainties = false;\n')
    file.write('    rnd_gen={\n')
    file.write('         seed=126;//default of-1 means: use current time.\n')
    file.write('      };\n')
    file.write('    };\n')
    '''
    
    
    file.write('    n-events='+str(experiments)+';\n')
    file.write('    model="@model_'+modelName+'";\n')
    file.write('    output_database={\n')
    file.write('        type="rootfile_database";\n')
    file.write('        filename="'+os.path.join(modelName+'.root')+'";\n')
    file.write('    };\n')
    file.write('    producers=("@pd"\n')
    file.write('    );\n')
    file.write('};\n')
    
    file.write('options = {\n')
    file.write('           plugin_files = ("$THETA_DIR/lib/root.so", "$THETA_DIR/lib/core-plugins.so");\n')
    file.write('};\n')
    
    

    

if __name__=="__main__":
    uncertaintyDict={
        "other":{"type":"gauss","config":{"mean": "1.0", "width":"0.5", "range":"(0.0,\"inf\")"}},
        "topbg":{"type":"gauss","config":{"mean": "1.0", "width":"2.0", "range":"(0.0,\"inf\")"}},
        "tChan":{"type":"gauss","config":{"mean": "1.0", "width":"100.0", "range":"(0.0,\"inf\")"}},
        "qcd":{"type":"gauss","config":{"mean": "1.0", "width":"2.0", "range":"(0.0,\"inf\")"}}
        
        #"other":{"type":"log_normal","config":{"mu": "0.0", "sigma":"2.0"}},
        #"topbg":{"type":"log_normal","config":{"mu": "0.0", "sigma":"2.0"}},
        #"tChan":{"type":"log_normal","config":{"mu": "0.0", "sigma":"2.0"}}
     
    }
    
    categories = {
        "2j1t": {
            #"weight":"1",
            "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)*(njets==2)*(ntags==1)*(bdt_qcd>-0.15)"
        },
        #"2j0t": {
        #    "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==2)*(ntags==0)*(bdt_qcd2>0.4)"
        #},
        #"3j1t": {
        #    "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(njets==3)*(ntags==1)*(bdt_qcd2>0.4)"
        #},
        "3j2t": {
            #"weight":"1",
            "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)*(njets==3)*(ntags==2)*(bdt_qcd>-0.15)"
        },
    }
    templateMCSetDict={
        "other":
        {
            "sets":["DY","DiBoson","WJetsExclLF","WJetsExclCF","WJetsExclBF"],
            "uncertainties":["other"],
            "weight":"pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700",
            "color":ROOT.kGreen+1
        },
        "topbg":
        {
            "sets":["sChan","tWChan","TTJetsSemi","TTJetsDi"],
            "uncertainties":["topbg"],
            "weight":"pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700",
            "color":ROOT.kOrange
        },
        "tChan":
        {
            "sets":["tChanLeptons"],
            "uncertainties":["tChan"],
            "weight":"pu_weight*b_weight*lepton_weight__id*lepton_weight__trigger*lepton_weight__iso*xsweight*19700",
            "color":ROOT.kMagenta
        },
        "QCD":
        {
            "sets":["QCDMu","DYAntiiso","DiBosonAntiiso","WJetsExclLFAntiiso","WJetsExclCFAntiiso","WJetsExclBFAntiiso","sChanAntiiso","tWChanAntiiso","TTJetsSemiAntiiso","TTJetsDiAntiiso","tChanLeptonsAntiiso"],
            "uncertainties":["qcd"],
            "weight":"1",
            "color":ROOT.kGray+1
        }
    }
    templateDATASetDict = {
        "data":
        {
            "sets":["SingleMu"],
            "weight":"1"
        }
    }

    dataSetDict={}
    histSetDict={}
    
    for category in categories.keys():
        dataSetDict[category]={}
        histSetDict[category]={}
        categoryWeight=categories[category]["weight"]
        for componentName in templateDATASetDict.keys():
            
            dataSetDict[category][componentName]=copy.copy(templateDATASetDict[componentName])
            dataSetDict[category][componentName]["weight"]+="*"+categoryWeight
            #print category,componentName
            #print dataSetDict[category][componentName]
            #print
        for componentName in templateMCSetDict.keys():
            histSetDict[category][componentName]=copy.copy(templateMCSetDict[componentName])
            histSetDict[category][componentName]["weight"]+="*"+categoryWeight
            #print category,componentName
            #print histSetDict[category][componentName]
            #print
       
     
    generateModel(modelName="fit",
                    prefix="",
                    dataDict=dataSetDict,
                    histSetDict=histSetDict,
                    uncertaintyDict=uncertaintyDict,
                    binning=30,
                    ranges=[-1.0,1.0],
                    dicePoisson=True,
                    mcUncertainty=True)
                
    
    
