#!/usr/bin/env python
import coffea
import numpy as np
import awkward as ak
from coffea import hist, processor
from topcoffea.modules.objects import isTightElec
from coffea.analysis_tools import PackedSelection
class AnalysisProcessor(processor.ProcessorABC):
    def __init__(self):

        # Create the histograms
        # In general, histograms depend on 'sample', 'channel' (final state) and 'cut' (level of selection)
        self._accumulator = processor.dict_accumulator({
            "events": hist.Hist(
                  "Events",
                  hist.Cat("sample", "A"),
                  hist.Bin("pdgID", "B", 1200, -600, 600 )),
            "electrons": hist.Hist(
                  "Electrons",
                  hist.Cat("sample", "A"),
                  hist.Bin("pt", "B", 600, 0, 600)),
            "jets": hist.Hist(
                  "Jets P_T",
                  hist.Cat("sample","A"),
                  hist.Bin("jets","Events", 90, 0, 1000)),
        })


    @property
    def accumulator(self):
        return self._accumulator

    @property
    def columns(self):
        return self._columns

    def process(self, events):
        dataset = events.metadata['dataset'] 

        particles = events.GenPart.pdgId
        values = ak.flatten(particles)

        e = events.Electron
        e['isTight'] = isTightElec(e.pt, e.eta, e.dxy, e.dz, e.miniPFRelIso_all, e.sip3d, e.mvaTTH, e.mvaFall17V2Iso, e.lostHits, e.convVeto, e.tightCharge, e.sieie, e.hoe, e.eInvMinusPInv, minpt=30)
        e = e[e.isTight]
        #ak.num==1
        elec = ak.flatten(e.pt)

        j = events.XConeJet.pt
        j = j[(abs(e.pt)>=55) & (abs(e.eta)<=2.5)]
        jet = ak.flatten(j)
        
        

#        

        # fill Histos
        hout = self.accumulator.identity()
        hout['events'].fill(
            sample=dataset,
            pdgID=values,
        )
        hout['electrons'].fill(
            sample = dataset,
            pt = elec,
        )
        hout['jets'].fill(
            sample = dataset,
            jets = jet,
        )
        return hout

    def postprocess(self, accumulator):
        return accumulator


