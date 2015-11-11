var files = [{"added": "2015-10-20T20:50:33.996245", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans1", "transient": true, "parents": ["gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt"], "location": "gram:/p/child1.txt", "path": "/p/child1.txt", "id": "Vspqnf", "subject": "Jane Doe"}, {"added": "2015-10-20T20:49:03.777477", "hash": "f9ccd1b4312d9ebd3daf727054815276", "dimensions": [32, 2080], "created": "2015-03-09T20:19:19.367602", "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transient": false, "location": "gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "path": "/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "size": 492581, "id": "VR55dC", "subject": "Jane Doe"}, {"added": "2015-10-20T20:51:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child2.txt", "path": "/p/b/child2.txt", "id": "toGp6R", "subject": "Jane Doe"}];


QUnit.test( "filesToHierarchy returns object ", function( assert ) {
    var root = filesToHierarchy([]);
    assert.deepEqual( root, {} );
});

QUnit.test( "filesToHierarchy root has raw files as children ", function( assert ) {
    files = [{'n':'a'},{'n':'b','parents':['a']},
            {'n':'c'},{'n':'d','parents':['c']}]
    var root = filesToHierarchy(files);
    assert.deepEqual( root, {'children':[{'n':'a'},{'n':'c'}]} );
});

QUnit.test( "Translate function returns translate string", function( assert ) {
    assert.equal( translate(12,34), 'translate(12,34)' );
});


