import niprov.adding
provdict = {'mydict':{'a':1234567,'bbbbbbb':'Hello. I was wondering..',
            'innerdict':{'key1':88.77, 'key2':'bla'}}}
rawbold = niprov.adding.add('testdata/parrec/T2.PAR', 
    provenance=provdict)



