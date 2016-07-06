from niprov import ProvenanceContext
provenance = ProvenanceContext()
(rawstru, s) = provenance.add('testdata/dicom/T1.dcm')
(rawbold, s) = provenance.add('testdata/parrec/T2_.PAR')
(rawevnt, s) = provenance.add('events.log', transient=True)

(stru, s) = provenance.log('struct.nii','reconstruction', str(rawstru.location), transient=True)
(run1, s) = provenance.log('run1.nii','reconstruction', str(rawbold.location), transient=True)
(dsgn, s) = provenance.log('design.mat','parse events', str(rawevnt.location), transient=True)

(moco, s) = provenance.log('run1_moco.nii','motion correction', str(run1.location), transient=True)

(corg, s) = provenance.log('run1_coreg.nii','coregistration', [str(moco.location), str(stru.location)], transient=True)

(stat, s) = provenance.log('run1_tstat.nii','statistics', [str(corg.location), str(dsgn.location)], transient=True)


