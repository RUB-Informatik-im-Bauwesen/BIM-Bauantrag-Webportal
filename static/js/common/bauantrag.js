var baseURI=window.location.protocol+"//"+window.location.host;

function bauantrag_delete(element){
    var p = $(element).parent().parent().children().get(0);
    var id = p.innerHTML;
    $.ajax({
        url: baseURI+'/bauantrag/'+id,
        type: 'DELETE',
        success: function(result) {
            location.reload();
        }
    });
}

function bauantrag_open(element) {
    var p = $(element).parent().parent().children().get(0);
    var id = p.innerHTML;
    window.location.href =  baseURI+'/bauantrag/open/'+id;
}

function bauantrag_download(element) {
    var p = $(element).parent().parent().children().get(0);
    var id = p.innerHTML;
    window.location.href =  baseURI+'/bauantrag/download/'+id;
}