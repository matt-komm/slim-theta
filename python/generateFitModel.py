from ModelClasses import *
from optparse import OptionParser
import math
import sys
import os
import logging
import copy
import random
import re
import ROOT

ROOT.gROOT.SetStyle("Plain")
ROOT.gStyle.SetOptStat(0)

sampleDict = {
    "tChannel":
    {
        "processes":[
            "ST_t-channel_4f_leptonDecays_13TeV-amcatnlo-pythia8_TuneCUETP8M1",
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kRed),
        "title":"t-channel",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)"
    },

    "tWChannel":
    {
        "processes":[
            "ST_tW_top_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1",
            "ST_tW_antitop_5f_inclusiveDecays_13TeV-powheg-pythia8_TuneCUETP8M1"
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kOrange),
        "title":"tW-channel",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)"
    },

    "TTJets":
    {
        "processes":[
            "TT_TuneCUETP8M1_13TeV-powheg-pythia8_ext"
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kOrange-3),
        "title":"t#bar{t}",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)"
    },
    
    "WJetsAMC":
    {
        "processes":[
            "WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kGreen-2),
        "title":"W+jets",
        "addtitle":"(aMC@NLO)",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)*(1+0.8*(Reconstructed_1__nSelectedJet==2)*(Reconstructed_1__nSelectedBJet==1))"
    },
    
    "WJetsMG":
    {
        "processes":[
            "WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8"
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kGreen-2),
        "title":"W+jets",
        "addtitle":"(MadGraph)",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)*(1+0.8*(Reconstructed_1__nSelectedJet==2)*(Reconstructed_1__nSelectedBJet==1))"
    },
    
    
    "DY":
    {
        "processes":[
            "DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8"
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kBlue-1),
        "title":"Drell-Yan",
        #"addtitle":"(#times 1.8)",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)*(1+0.8*(Reconstructed_1__nSelectedJet==2)*(Reconstructed_1__nSelectedBJet==1))"
    },

    "QCD":
    {
        "processes":[
            "QCD_Pt-20toInf_MuEnrichedPt15_TuneCUETP8M1_13TeV_pythia8",
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kGray),
        "title":"QCD (MC)",# #lower[-0.06]{#scale[0.85]{#times#frac{1}{5}}}",
        "weight":"((Generated_1__genweight<0)*(-1)+(Generated_1__genweight>0)*1)"
    },
    
    "data1":
    {
        "processes":[
            "SingleMuon_Run2015D-05Oct2015-v1",
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kBlack),
        "title":"Data",
        "weight":"((Reconstructed_1__HLT_IsoMu20_v2==1)+(Reconstructed_1__HLT_IsoMu20_v3==1))"
    },
    
    "data2":
    {
        "processes":[
            "SingleMuon_Run2015D-PromptReco-v4",
        ],
        "color":ROOT.gROOT.GetColor(ROOT.kBlack),
        "title":"Data",
        "weight":"(Reconstructed_1__HLT_IsoMu20_v3==1)"
    }
}

rootFilesMC=[]
rootFilesData=[]

basedirMC = os.path.join(os.getcwd(),"evaluate25ns")
matchMC = re.compile("mc[0-9]+.root")
basedirData = os.path.join(os.getcwd(),"evaluate25nsData")
matchData = re.compile("data[0-9]+.root")

for f in os.listdir(basedirMC):
    if matchMC.match(f):
        rootFilesMC.append(os.path.join(basedirMC,f))

for f in os.listdir(basedirData):
    if matchData.match(f):
        rootFilesData.append(os.path.join(basedirData,f))
        
print "found MC=",len(rootFilesMC)," and data=",len(rootFilesData)," files"




uncertainties = {
    "other":{"type":"gauss","config":{"mean": "1.0", "width":"0.5", "range":"(0.0,\"inf\")"}},
    "topbg":{"type":"gauss","config":{"mean": "1.0", "width":"2.0", "range":"(0.0,\"inf\")"}},
    "tChan":{"type":"gauss","config":{"mean": "1.0", "width":"100.0", "range":"(0.0,\"inf\")"}},
    "qcd":{"type":"gauss","config":{"mean": "1.0", "width":"2.0", "range":"(0.0,\"inf\")"}}
}

observables = {
    "2j1t": {
        #"weight":"1",
        "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)*(njets==2)*(ntags==1)*(bdt_qcd>-0.15)"
    },
    "3j2t": {
        #"weight":"1",
        "weight":"(n_signal_mu==1)*(n_signal_ele==0)*(n_veto_mu==0)*(n_veto_ele==0)*(hlt_mu==1)*(ljet_dr>0.3)*(bjet_dr>0.3)*(njets==3)*(ntags==2)*(bdt_qcd>-0.15)"
    },
}

globalMCWeight="(Reconstructed_1__HLT_IsoMu20_v1==1)*(Reconstructed_1__PU69000_weight)"

components={
    "other":
    {
        "sets":["DY"],
        "uncertainties":["other"],
        "weight":globalMCWeight,
        "color":ROOT.kGreen+1
    },
    "topbg":
    {
        "sets":["tWChannel","TTJets"],
        "uncertainties":["topbg"],
        "weight":globalMCWeight,
        "color":ROOT.kOrange
    },
    "tChan":
    {
        "sets":["tChannel"],
        "uncertainties":["tChan"],
        "weight":globalMCWeight,
        "color":ROOT.kMagenta
    },
    "QCD":
    {
        "sets":["QCD"],
        "uncertainties":["qcd"],
        "weight":globalMCWeight,
        "color":ROOT.kGray+1
    }
}

data = {
    "data":
    {
        "sets":["data1","data2"],
        "weight":"1"
    }
}


binning=20
ranges=[-1,1]


model=Model(modelName, {"bb_uncertainties":"true"})

for uncertainty in uncertainties.keys():
    uncertaintyDict[uncertainty]["dist"]=Distribution(uncertainty, uncertaintyDict[uncertainty]["type"], uncertaintyDict[uncertainty]["config"])
    file.write(uncertaintyDict[uncertainty]["dist"].toConfigString())
        
for observableName in observables.keys():
    observable = Observable(observableName, binning, ranges)
    observableWeight = observables[observableName]["weight"]
    
    for componentName in components.keys():
        componentWeight = components[componentName]["weight"]
        componentUncertainties = components[componentName]["uncertainties"]
        
        for componentSetName in components[componentName]["sets"]:
            for processName in sampleDict[setName]["processes"]:
                processWeight = sampleDict[setName]["weight"]
                
                for i,f in enumerate(rootFilesMC):
                    rootFile = ROOT.TFile(f)
                    tree = rootFile.Get(processName)
                    if (tree):
                        component=ObservableComponent(observableName+"__"+componentName+"__"+componentSetName+"__"+processName+"__"+str(i))
                        coeff=CoefficientMultiplyFunction()
                        for uncertaintyName in componentUncertainties:
                            coeff.addDistribution(uncertainties[uncertaintyName],uncertainties[uncertaintyName].getParameterName())
                        component.setCoefficientFunction(coeff)
                        observable.addComponent(component)
                    rootFile.Close()
                
            

    model.addObservable(obs)
    #break

    '''
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
        

    
    
        
    
   
    file.write(model.toConfigString())
    _writeFile(file,model,modelName,dicePoisson=dicePoisson,mcUncertainty=mcUncertainty)
    file.close()
    '''
                    
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
    
    

