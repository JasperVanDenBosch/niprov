from niprov import ProvenanceContext
provenance = ProvenanceContext()
rawstru = provenance.add('testdata/dicom/T1.dcm')
rawbold = provenance.add('testdata/parrec/T2_.PAR')
rawevnt = provenance.add('events.log', transient=True)

stru = provenance.log('struct.nii','reconstruction', str(rawstru.location), transient=True)
run1 = provenance.log('run1.nii','reconstruction', str(rawbold.location), transient=True)
dsgn = provenance.log('design.mat','parse events', str(rawevnt.location), transient=True)

moco = provenance.log('run1_moco.nii','motion correction', str(run1.location), transient=True)

corg = provenance.log('run1_coreg.nii','coregistration', [str(moco.location), str(stru.location)], transient=True)

stat = provenance.log('run1_tstat.nii','statistics', [str(corg.location), str(dsgn.location)], transient=True)


