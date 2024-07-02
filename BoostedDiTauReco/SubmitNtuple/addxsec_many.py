import os, sys, math
import ROOT
import argparse

parser = argparse.ArgumentParser(description="Normalize by cross-section. e.g. python3 -v v6 -f studySVFit --histo MuTau_OS_dRcut_lowMt_Mass --all")
parser.add_argument("-v", "--version", type=str, help="Version for doHadd")
parser.add_argument("-f", "--filename", type=str, help="filename from condor output")
parser.add_argument("-a", "--all", action="store_true", help="go through all samples")
parser.add_argument("--tcp", action="store_true", help="go through tcp samples only")
parser.add_argument("--bkg", action="store_true", help="go through background samples only")
parser.add_argument("-r", "--region", type=str, help="regions to plot")
parser.add_argument("--histo", type=str, nargs="+")
parser.add_argument("--alpmodel", type=str)
args = parser.parse_args(args=None if sys.argv[1:] else ['--help'])

pi = math.pi

c_t = 1
m_t = 1.77686 #Tau Mass
fa = 1000 #dimensional param
m_a = [10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65]
Br = {
    'M1':{'10':6.7, '15':4.01, '20':3.4, '25':2.9, '30':2.5, '35':2.2, '40':1.9, '45':1.7, '50':1.5, '55':1.3, '60':1.2, '65':1.05},
    'M2':{'10':9.7, '15':5.8, '20':4.8, '25':4.1, '30':3.6, '35':3.1, '40':2.7, '45':2.4, '50':2.1, '55':1.9, '60':1.7, '65':1.5},
    'M3':{'10':5.7, '15':3.4, '20':2.9, '25':2.6, '30':2.2, '35':1.98, '40':1.8, '45':1.6, '50':1.4, '55':1.2, '60':1.1, '65':1.01},
    'M4':{'10':6.2, '15':3.6, '20':2.6, '25':2.03, '30':1.6, '35':1.3, '40':1.1, '45':0.9, '50':0.79, '55':0.7, '60':0.6, '65':0.53},
    'M5':{'10':3.0, '15':1.8, '20':1.5, '25':1.28, '30':1.1, '35':0.96, '40':0.84, '45':0.74, '50':0.66, '55':0.6, '60':0.52, '65':0.47},
    'M6':{'10':3.0, '15':1.8, '20':1.5, '25':1.28, '30':1.1, '35':0.96, '40':0.84, '45':0.74, '50':0.66, '55':0.6, '60':0.52, '65':0.47},
    'M7':{'10':9.7, '15':5.8, '20':4.9, '25':4.1, '30':3.6, '35':3.1, '40':2.7, '45':2.4, '50':2.1, '55':1.9, '60':1.7, '65':1.5},
    'M8':{'10':0.88, '15':0.53, '20':0.5, '25':0.49, '30':0.48, '35':0.5, '40':0.46, '45':0.4, '50':0.43, '55':0.41, '60':0.4, '65':0.4},
    'M9':{'10':1.9, '15':1.1, '20':0.74, '25':0.54, '30':0.42, '35':0.33, '40':0.27, '45':0.2, '50':0.19, '55':0.17, '60':0.14, '65':0.13},
    'M10':{'10':1.8, '15':1.05, '20':0.73, '25':0.53, '30':0.41, '35':0.33, '40':0.27, '45':0.2, '50':0.19, '55':0.17, '60':0.14, '65':0.13},
    'M11':{'10':2.1, '15':1.2, '20':1.1, '25':1.02, '30':0.94, '35':0.86, '40':0.79, '45':0.7, '50':0.66, '55':0.6, '60':0.55, '65':0.51},
    'M12':{'10':2.9, '15':1.7, '20':1.5, '25':1.4, '30':1.3, '35':1.1, '40':1.0, '45':0.9, '50':0.85, '55':0.8, '60':0.70, '65':0.6}
}


xsec_M = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

xsec_M_unscaled = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

for mass in m_a:
    Gamma_tt = ((c_t**2*mass/(8*pi))*m_t**2*math.sqrt(1-4*m_t**2/mass**2))/fa**2
    xsec_g_TCP = 1/Gamma_tt #cross section of gg fusion to tcp
    for model in Br.keys():
        xsec_M_list = xsec_g_TCP * Br[model][str(mass)]
        xsec_M_unscaled[model][str(mass)] = xsec_g_TCP
        xsec_M[model][str(mass)] = xsec_M_list

TCP_xsec = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}

TCP_xsec_unscaled = {
    'M1':{},
    'M2':{},
    'M3':{},
    'M4':{},
    'M5':{},
    'M6':{},
    'M7':{},
    'M8':{},
    'M9':{},
    'M10':{},
    'M11':{},
    'M12':{}
}


norm = {
    '10': 2.890e-06+5.616e-08,
    '15': 4.301e-06+8.291e-08,
    '20': 5.867e-06+1.179e-07,
    '25': 6.925e-06+1.351e-07,
    '30': 8.060e-06+1.628e-07,
    '35': 9.147e-06+1.971e-07,
    '40': 1.004e-05+2.301e-07,
    '45': 1.097e-05+2.358e-07,
    '50': 1.176e-05+2.691e-07,
    '55': 1.220e-05+2.746e-07,
    '60': 1.272e-05+3.032e-07,
    '65': 1.343e-05+3.453e-07
}

for model in Br.keys():
    for mass in range(10,70,5):
        TCP_xsec[model][str(mass)] = xsec_M[model][str(mass)] * norm[str(mass)]
        TCP_xsec_unscaled[model][str(mass)] = xsec_M_unscaled[model][str(mass)] * norm[str(mass)]


model = args.alpmodel

#----------------------------------

xsecs={
     'ALP_Ntuple_m_10_htj_100to400':{'':xsec_M[model]['10'] * 2.890e-06},
     'ALP_Ntuple_m_10_htj_400toInf':{'':xsec_M[model]['10'] * 5.616e-08},
     'ALP_Ntuple_m_15_htj_100to400':{'':xsec_M[model]['15'] * 4.301e-06},
     'ALP_Ntuple_m_15_htj_400toInf':{'':xsec_M[model]['15'] * 8.291e-08},
     'ALP_Ntuple_m_20_htj_100to400':{'':xsec_M[model]['20'] * 5.867e-06},
     'ALP_Ntuple_m_20_htj_400toInf':{'':xsec_M[model]['20'] * 1.179e-07},
     'ALP_Ntuple_m_25_htj_100to400':{'':xsec_M[model]['25'] * 6.925e-06},
     'ALP_Ntuple_m_25_htj_400toInf':{'':xsec_M[model]['25'] * 1.351e-07},
     'ALP_Ntuple_m_30_htj_100to400':{'':xsec_M[model]['30'] * 8.060e-06},
     'ALP_Ntuple_m_30_htj_400toInf':{'':xsec_M[model]['30'] * 1.628e-07},
     'ALP_Ntuple_m_35_htj_100to400':{'':xsec_M[model]['35'] * 9.147e-06},
     'ALP_Ntuple_m_35_htj_400toInf':{'':xsec_M[model]['35'] * 1.971e-07},
     'ALP_Ntuple_m_40_htj_100to400':{'':xsec_M[model]['40'] * 1.004e-05},
     'ALP_Ntuple_m_40_htj_400toInf':{'':xsec_M[model]['40'] * 2.301e-07},
     'ALP_Ntuple_m_45_htj_100to400':{'':xsec_M[model]['45'] * 1.097e-05},
     'ALP_Ntuple_m_45_htj_400toInf':{'':xsec_M[model]['45'] * 2.358e-07},
     'ALP_Ntuple_m_50_htj_100to400':{'':xsec_M[model]['50'] * 1.176e-05},
     'ALP_Ntuple_m_50_htj_400toInf':{'':xsec_M[model]['50'] * 2.691e-07},
     'ALP_Ntuple_m_55_htj_100to400':{'':xsec_M[model]['55'] * 1.220e-05},
     'ALP_Ntuple_m_55_htj_400toInf':{'':xsec_M[model]['55'] * 2.746e-07},
     'ALP_Ntuple_m_60_htj_100to400':{'':xsec_M[model]['60'] * 1.272e-05},
     'ALP_Ntuple_m_60_htj_400toInf':{'':xsec_M[model]['60'] * 3.032e-07},
     'ALP_Ntuple_m_65_htj_100to400':{'':xsec_M[model]['65'] * 1.343e-05},
     'ALP_Ntuple_m_65_htj_400toInf':{'':xsec_M[model]['65'] * 3.453e-07},        
     'DYJetsToLL':{
         'M-50_HT-70to100':140.0,
         'M-50_HT-100to200':139.2, 
         'M-50_HT-200to400':38.4, 
         'M-50_HT-400to600':5.174,
         'M-50_HT-600to800':1.258, 
         'M-50_HT-800to1200':0.5598, 
         'M-50_HT-1200to2500':0.1305, 
         'M-50_HT-2500toInf':0.002997},
     'DYJetsToLL_M-4to50':{
         'HT-70to100':321.2,
         'HT-100to200':190.6,
         'HT-200to400':42.27,
         'HT-400to600':4.05,
         'HT-600toInf':1.216},
     'TT':{
         'TTTo2L2Nu_TuneCP5':88.2497},
         # 'TTToSemiLeptonic_TuneCP5':365.30899,
         # 'TTToHadronic_TuneCP5':377.9517},
     'ST':{
         's-channel':3.549,
         # 't-channel_antitop':26.2278,
         # 't-channel_top':44.07048,
         't_antitop':71.75,
         't_top':119.7,
         'tW_antitop':32.51,
         'tW_top':32.45},
     'Diboson':{
         'WW':76.25,
         'WZ':27.55,
         'ZZ':12.23},
      'WJetsToLNu_flat':{
          'TuneCP5':52940.0},
      'WJetsToLNu':{
          'HT-70To100':1264.0,
          'HT-100To200':1343.0,
          'HT-200To400':359.6,
          'HT-400To600':48.85,
          'HT-600To800':12.05,
          'HT-800To1200':5.501,
          'HT-1200To2500':1.329},
      'QCD':{
          'HT50to100':185300000.0,
          'HT100to200':23590000.0,
          'HT200to300':1551000.0,
          'HT300to500':323400.0,
          'HT500to700':30140.0,
          'HT700to1000':6344.0,
          'HT1000to1500':1092.0,
          'HT1500to2000':99.76,
          'HT2000toInf':20.35},
     'Y':{
         'pth400':0.0504*0.01*0.00945495019497735,
         'pth100':47.980*0.01*0.00945495019497735}
}

     # 'DYJetsToLL':{
     #     'M-50_HT-70to100':146.5,
     #     'M-50_HT-100to200':160.7, 
     #     'M-50_HT-200to400':48.63, 
     #     'M-50_HT-400to600':6.993,
     #     'M-50_HT-600to800':1.761, 
     #     'M-50_HT-800to1200':0.8021, 
     #     'M-50_HT-1200to2500':0.1937, 
     #     'M-50_HT-2500toInf':0.003514},
#      'DYJetsToLL_M-4to50':{
#          'HT-70to100':321.2,
# #         'HT-70to100':145.5,
#          'HT-100to200':204.0,
#          'HT-200to400':54.39,
#          'HT-400to600':5.697,
#          'HT-600toInf':1.85},

xsecsQCD = {
    'HT-50to100':{'':185300000.0},
    'HT-100to200':{'':23590000.0},
    'HT-200to300':{'':1551000.0},
    'HT-300to500':{'':323400.0},
    'HT-500to700':{'':30140.0},
    'HT-700to1000':{'':6344.0},
    'HT-1000to1500':{'':1092.0},
    'HT-1500to2000':{'':99.76},
    'HT-2000toInf':{'':20.35}
}


if args.filename :
    fileName = args.filename


def weightBackgroundHists(hists, files, version, study, var, Sample):
    for sample in Sample:
        h = None
        for mass in list(xsecs[sample]):
            if gen==True:
                filename="h_Gen_"+sample+"_"+mass+"_"+version+".root"
            else:
                filename = "h_"+fileName+"_"+sample+"_"+mass+"_"+version+".root"
            histname=var 
            print(filename, histname)
            fil=ROOT.TFile(filename, 'r')
            if fil.IsZombie(): continue
            files+=[fil]
            hist=fil.Get(histname) 
            nEvt=fil.Get("NEvents").GetBinContent(2)
            xsec=xsecs[sample][mass]
            if list(xsecs[sample]).index(mass)==0:  
                h = hist.Clone(sample+"_"+histname)                                                 
                h.Scale((xsec/nEvt)*L)
                hists[sample] = h                    
            else: 
                hist.Scale((xsec/nEvt)*L)
                hists[sample].Add(hist)

            # if h == None:
            #     try:
            #         h = hist.Clone(sample+"_"+histname)                                                                      
            #         h.Scale((xsec/nEvt)*L)                                                                           
            #         hists[sample] = h
            #     except ReferenceError:
            #         continue
            # else:                                                                                                                          
            #     hist.Scale((xsec/nEvt)*L)                                                                                                  
            #     hists[sample].Add(hist)             



hists = {}
files = []

#L = 41530.0 #2017
#L = 36700.0
#L = 36700.0 #2016
L = 59740.0 #2018
#L = 7100.0 #2018Eras
#L = 137600.0 #Full RunII
#L = 1
#-------------

gen = False
scaling = 'xsection' #'xsection' else: 'unity'

if args.version :
    version = args.version
    iteration = args.version
    study = args.filename

#-------------

#Sample = ['TTJets']

signal_sample = []
signal_mass= []

if args.tcp :
    signal_sample = ['ALP_Ntuple_m_30_htj_100to400','ALP_Ntuple_m_30_htj_400toInf', 'ALP_Ntuple_m_20_htj_100to400', 'ALP_Ntuple_m_20_htj_400toInf', 'ALP_Ntuple_m_50_htj_100to400', 'ALP_Ntuple_m_50_htj_400toInf','ALP_Ntuple_m_65_htj_100to400','ALP_Ntuple_m_65_htj_400toInf']
    signal_mass = [x.split("_")[0]+'_'+x.split("_")[1]+'_'+x.split("_")[2]+'_'+x.split("_")[3] for x in signal_sample]
    signal_mass = list(set(signal_mass))
    Sample = signal_sample
#    Sample = ['ALP_Ntuple_m_30_htj_100to400','ALP_Ntuple_m_30_htj_400toInf']
if args.all :
    signal_sample = ['ALP_Ntuple_m_15_htj_100to400', 'ALP_Ntuple_m_15_htj_400toInf','ALP_Ntuple_m_20_htj_100to400', 'ALP_Ntuple_m_20_htj_400toInf','ALP_Ntuple_m_25_htj_100to400', 'ALP_Ntuple_m_25_htj_400toInf','ALP_Ntuple_m_30_htj_100to400','ALP_Ntuple_m_30_htj_400toInf','ALP_Ntuple_m_35_htj_100to400', 'ALP_Ntuple_m_35_htj_400toInf','ALP_Ntuple_m_40_htj_100to400', 'ALP_Ntuple_m_40_htj_400toInf','ALP_Ntuple_m_45_htj_100to400', 'ALP_Ntuple_m_45_htj_400toInf', 'ALP_Ntuple_m_60_htj_100to400', 'ALP_Ntuple_m_60_htj_400toInf','ALP_Ntuple_m_55_htj_100to400', 'ALP_Ntuple_m_55_htj_400toInf','ALP_Ntuple_m_50_htj_100to400', 'ALP_Ntuple_m_50_htj_400toInf']
    # # signal_sample = ['ALP_Ntuple_m_30_htj_100to400','ALP_Ntuple_m_30_htj_400toInf', 'ALP_Ntuple_m_20_htj_100to400', 'ALP_Ntuple_m_20_htj_400toInf', 'ALP_Ntuple_m_50_htj_100to400', 'ALP_Ntuple_m_50_htj_400toInf']
    # signal_sample = ['ALP_Ntuple_m_15_htj_100to400','ALP_Ntuple_m_15_htj_400toInf']
    signal_mass = [x.split("_")[0]+'_'+x.split("_")[1]+'_'+x.split("_")[2]+'_'+x.split("_")[3] for x in signal_sample]
    signal_mass = list(set(signal_mass))
    # bkg_sample = ['Ntuple_DYJetsToLL','Ntuple_DYJetsToLL_M-4to50','Ntuple_WJetsToLNu','Ntuple_Diboson','Ntuple_TT']
    bkg_sample = ['DYJetsToLL','DYJetsToLL_M-4to50','WJetsToLNu','Diboson','ST','TT']
    Sample = signal_sample+bkg_sample
if args.bkg :
    # Sample = ['DYJetsToLL','DYJetsToLL_M-4to50','QCD','WJetsToLNu','Diboson','ST','TT']
    Sample = ['TT','ST','Diboson']


#VARIABLE = ['Mass', 'Lepton1Pt', 'Lepton2Pt', 'JetPt', 'MetPt', 'Mt','Nj','dRl','dRj', 'dPhil', 'dPhi','Count']
#VARIABLE = ['Lepton1Pt', 'Lepton2Pt', 'LeadingJetPt', 'Count', 'HT','dRl','dRj','Mass','MetPt']
#VARIABLE = ['Lepton1Pt', 'Lepton2Pt', 'LeadingJetPt', 'Mass','dRl','dRj']
VARIABLE = ['Lepton1Pt', 'Lepton2Pt','dRl', 'MetPt']

REGION = []

histlist = []

#for region in REGION:
if args.region is not None:
    for variable in VARIABLE:
        histlist.append(args.region+"_"+variable)

if args.histo is not None:
    histlist = args.histo

for var in histlist:
    weightBackgroundHists(hists, files, version, study, var, Sample)

    if scaling == 'xsection':
         # out = ROOT.TFile("h_"+var+"_"+study+"_"+iteration+"_"+model+".root",'recreate')
         out = ROOT.TFile("h_"+var+"_"+study+"_"+iteration+".root",'recreate')
         print(out)
    else: 
         out = ROOT.TFile("h_"+study+"_"+var+"_"+version+"_unity.root",'recreate')

    out.cd()

    print(hists)

    for name in Sample:
        if name=='DYJetsToLL':
            hists[name].SetFillColor(ROOT.kRed-6)
        elif name=='DYJetsToLL_M-4to50':
            hists[name].SetFillColor(ROOT.kRed-9)
        elif name=='TTJets':
            hists[name].SetFillColor(ROOT.kOrange-4)
        elif name=='TTTo2L2Nu':
            hists[name].SetFillColor(ROOT.kOrange-4)
        elif name=='TTToSemiLeptonic':
            hists[name].SetFillColor(ROOT.kOrange-5)
        elif name=='TTToHadronic':
            hists[name].SetFillColor(ROOT.kOrange-6)
        elif name=='ST':
            hists[name].SetFillColor(ROOT.kMagenta-9)
        elif name == 'Diboson':
            hists[name].SetFillColor(ROOT.kAzure+7)
        elif name == 'QCD':
            hists[name].SetFillColor(ROOT.kGray)
        elif name=='WJetsToLNu':
            hists[name].SetFillColor(ROOT.kGreen-6)

        if name not in signal_sample:
            # hists[name].SetName("ETau_hBJetPt")
            # hists[name].Write("ETau_hBJetPt", ROOT.TObject.kWriteDelete)
            hists[name].Write()
            print(hists[name].GetName())
            print(name)

    for sig in signal_mass:
        print(sig)
        tmp = {}
        for key in hists.keys():
            if sig in key:
                if '100to400' in key:
                    tmp[sig] = hists[key]
                if '400toInf' in key:
                    tmp[sig].Add(hists[key])
                    print(sig+"_"+var)
                    tmp[sig].SetName(sig+"_"+var)
                    tmp[sig].Write(sig+"_"+var, ROOT.TObject.kWriteDelete)
                    # tmp[sig].SetName(sig+"_ETau_SR_2017_OS_Boost_Mass")
                    # tmp[sig].Write(sig+"_ETau_SR_2017_OS_Boost_Mass", ROOT.TObject.kWriteDelete)
                    

    out.Close()

print(VARIABLE)
print("Histlist")
print(*histlist, sep=", ")
print("Regions")
print(*REGION, sep=", ")
