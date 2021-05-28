
var pagelist = null;

function parseJSON(obj) {
  $('#result').html(getResultHTMLText(obj));
  pagelist = obj.meta;
  onSearchReady();
}

function onTimeout() {
  console.log('timeout');
}

function query(s, q) {
    if (q) {
        $('#loadingMessage').show();
        url = "load.py?q="+encodeURIComponent(q);
        if (s)
            url += "&s="+s;
        $.ajax({
          url: url,
          dataType: 'json',
          error: onTimeout,
          success: parseJSON,
          timeout: 20000
        });
    }
    else {
        $('#loadingMessage').hide();
    }
}

function onSearch() {
    var q = $('#input_q').val();
    var s = $('#select_engine').val();
    window.location.href = 'search.html?q=' + q + '&s=' + s;
}

function onPlayVideo() {
    if (pagelist) {
        saveCookie('pagelist', pagelist);
    }
}

function onSearchReady() {
    $( "a[meta='playVideo']" ).click(onPlayVideo);
    $('#loadingMessage').hide();
}

function onDocumentReady() {
    var s = GetURLParameter("s") || 'youtube';
    var q = GetURLParameter("q");
    if (q) {
        q = decodeURIComponent(q);
        $('#input_q').val(q);
    }
    $('#select_engine').val(s);
    query(s, q);
}
