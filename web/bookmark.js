
function loadgist(gistid, filename) {
    $.ajax({
        url: 'https://api.github.com/gists/'+gistid,
        type: 'GET',
        dataType: 'jsonp',
        cache: true,
        jsonpCallback: 'myCallback',
        timeout: 1000
    }).success( function(gistdata) {
        var content = gistdata.data.files[filename].content;
        parseJSON(JSON.parse(content));
    }).error( function(e) {
        console.log(e);
    });
}

function genTemplateTable(channel, links) {
    var length4 = (links.length + 3) & ~3;
    var colspan = length4 / 4;
    var text = '';

    text += '<table>';
    text += '<tr><th colspan='+colspan+'>'+channel+'</th></tr>';
    for (var i=0; i<4; i++) {
        text += '<tr>';
        for (var j=0; j<colspan; j++) {
            var idx = i + j * 4;
            if (idx < links.length) {
                if (links[idx].link.startsWith('http')) {
                    text += '<td><a href="list.html?p='+links[idx].link+'">'+links[idx].title+'</a></td>';
                } else {
                    text += '<td><a href="'+links[idx].link+'">'+links[idx].title+'</a></td>';
                }
            } else {
                text += '<td></td>';
            }
        }
        text += '</tr>';
    }
    text += '</table>';

    return text;
}

function genCustomTable() {
    var text = '';
    var youtubeID = localStorage.getItem('youtubeID');

    if (youtubeID && youtubeID.length > 0) {
        links = [
            {'title' : 'videos', 'link' : 'https://www.youtube.com/user/'+youtubeID+'/videos'},
            {'title' : 'playlists', 'link' : 'https://www.youtube.com/user/'+youtubeID+'/playlists'},
            {'title' : 'channels', 'link': 'https://www.youtube.com/user/'+youtubeID+'/channels'}
        ];
        text += genTemplateTable(youtubeID, links);
    }

    return text;
}


function parseJSON(obj) {
    var text = '';

    text += genCustomTable();

    for (var i=0; i<obj.channels.length; i++) {
        var channel = obj.channels[i];
        text += genTemplateTable(channel.channel, channel.links);
    }

    $('#result').html(text);
    $('#loadingMessage').hide();
}

function onTimeout () {
    console.log('timeout');
}

function onDocumentReady() {
    var jsonURL = 'null';

    var bookmark = localStorage.getItem('bookmark');
    if (bookmark && bookmark.length > 0) {
        jsonURL = bookmark;
    }

    $.ajax({
        url: 'load.py?j='+jsonURL,
        dataType: 'json',
        error: onTimeout,
        success: parseJSON,
        timeout: 2000
    });
}

