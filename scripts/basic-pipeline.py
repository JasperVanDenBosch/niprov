from niprov import ProvenanceContext
provenance = ProvenanceContext()
rawimg = provenance.add('testdata/eeg/stub.cnt')
g1c1 = provenance.log('g1c1','action', str(rawimg.location), transient=True) #new, transformation, parents
g1c2 = provenance.log('g1c2','action', str(rawimg.location), transient=True) #new, transformation, parents
g2c1 = provenance.log('g2c1','action', str(g1c1.location), transient=True) #new, transformation, parents
g2c2 = provenance.log('g2c2','action', str(g1c1.location), transient=True) #new, transformation, parents
g2c3 = provenance.log('g2c3','action', [str(g1c2.location), str(rawimg.location)], transient=True) 
g3c1 = provenance.log('g3c1','action', str(g2c3.location), transient=True) #new, transformation, parents
g3c2 = provenance.log('g3c2','action', str(g2c3.location), transient=True) #new, transformation, parents

