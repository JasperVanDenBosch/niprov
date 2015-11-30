
// from http://stackoverflow.com/a/18650828/708221
function formatBytes(bytes,decimals) {
   if(bytes == 0) return '0 Byte';
   var k = 1000;
   var dm = decimals + 1 || 3;
   var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
   var i = Math.floor(Math.log(bytes) / Math.log(k));
   return (bytes / Math.pow(k, i)).toPrecision(dm) + ' ' + sizes[i];
}

function makeFieldsHumanReadable() {
    //this could be a general function for filesize, datetime, etc
    $('.filesize').each(function() {
        //should add class that notes that this element has been converted .addClass()
        $( this ).text(function (i, txt) {
            return formatBytes(parseInt(txt),2);
        });
    });
    $('.datetime').each(function() {
        //should add class that notes that this element has been converted .addClass()
        $( this ).text(function (i, txt) {
            return moment(txt).format('MMMM Do YYYY, h:mm a');
        });
    });
}

makeFieldsHumanReadable();

