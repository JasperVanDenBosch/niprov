var files = [{"added": "2015-10-20T20:50:33.996245", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans1", "transient": true, "parents": ["gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt"], "location": "gram:/p/child1.txt", "path": "/p/child1.txt", "id": "Vspqnf", "subject": "Jane Doe"}, {"added": "2015-10-20T20:49:03.777477", "hash": "f9ccd1b4312d9ebd3daf727054815276", "dimensions": [32, 2080], "created": "2015-03-09T20:19:19.367602", "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transient": false, "location": "gram:/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "path": "/home/jasper/Projects/niprov/testdata/eeg/stub.cnt", "size": 492581, "id": "VR55dC", "subject": "Jane Doe"}, {"added": "2015-10-20T20:51:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child2.txt", "path": "/p/b/child2.txt", "id": "toGp6R", "subject": "Jane Doe"}, {"added": "2015-10-20T20:52:00.178131", "script": null, "acquired": "2015-03-09T13:07:03.000000", "hostname": "gram", "transformation": "trans2", "transient": true, "parents": ["gram:/p/child1.txt"], "location": "gram:/p/b/child3.txt", "path": "/p/b/child3.txt", "id": "J7yUxi", "subject": "Jane Doe"}];


QUnit.test( "filesToHierarchy returns object ", function( assert ) {
    var root = filesToHierarchy([]);
    assert.deepEqual( root, {path:'root',children:[]} );
});

QUnit.test( "filesToHierarchy root has raw files as children ", function( assert ) {
    files = [{'location':'a'},{'location':'b','parents':['a']},
            {'location':'c'},{'location':'d','parents':['c']}]
    var root = filesToHierarchy(files);
    assert.equal( root.children[0].location, 'a' );
    assert.equal( root.children[1].location, 'c' );
});

QUnit.test( "filesToHierarchy recursively finds children ", function( assert ) {
    files = [{'location':'a'},
            {'location':'b','parents':['a']},{'location':'c','parents':['a']},
            {'location':'d','parents':['b']},{'location':'e','parents':['b']}]
    var root = filesToHierarchy(files);
    assert.equal( root.children[0].location, 'a' );
    assert.equal( root.children[0].children[0].location, 'b' );
    assert.equal( root.children[0].children[1].location, 'c' );
    assert.equal( root.children[0].children[0].children[0].location, 'd' );
    assert.equal( root.children[0].children[0].children[1].location, 'e' );
});
QUnit.test( "filesToHierarchy only adds child to one parent ", function( assert ) {
    files = [{'location':'a'},{'location':'b'},
            {'location':'c','parents':['a','b']}]
    var root = filesToHierarchy(files);
    // a has child c
    assert.equal( root.children[0].children[0].location, 'c' ); 
    if ( root.children[1].hasOwnProperty('children') ) {
        //b does not have child c
        assert.equal( root.children[1].children.length, 0, 
            "second parent B should not have any children" ); 
    }
});
QUnit.test( "Translate function returns translate string", function( assert ) {
    assert.equal( translate(12,34), 'translate(12,34)' );
});

QUnit.test( "Shortname makes filename readable", function( assert ) {
    var shortpath = '/home/johndoe/sometextfile.txt'
    assert.equal( shortname(shortpath), 'sometextfile.txt' );
    var longpath = '/p/one_two_12_three_four_34_five_six_56_seven_eight_78.ext'
    assert.equal( shortname(longpath), 'one_two...ght_78.ext' );
});



