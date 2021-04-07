from CRABClient.UserUtilities import config
config = config()

config.section_('General')
config.General.requestName = 'Monopole_SpinHalf_M-1000_DY_13TeV_v1'
config.General.workArea = 'linshih_crab'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ntuple_1000.py'
config.JobType.pyCfgParams = []
config.JobType.maxMemoryMB = 2000
config.JobType.maxJobRuntimeMin = 2000

config.section_('Data')
config.Data.inputDataset = '/Monopole_SpinHalf_M-1000_DY_13TeV_TuneCUETP8M1/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v2/GEN-SIM-RECO'
config.Data.inputDBS = 'global'
#config.Data.splitting = 'LumiBased'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
#config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/Legacy_2017/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt'
config.Data.outLFNDirBase = '/store/user/lshih/Monopole'
#config.Data.publication = True
#config.Data.outputDatasetTag = 'DiphoVtxUL2017_DoubleMuon_Run2017D-09Aug2019_UL2017-v1'

config.section_('Site')
config.Site.storageSite = 'T2_TW_NCHC'
