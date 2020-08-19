var baseURI=window.location.protocol+"//"+window.location.host;

var xbau_uploader = new plupload.Uploader({
  browse_button: 'xbau_uploader', // this can be an id of a DOM element or the DOM element itself
  url: baseURI+'/antragsteller/upload'
});

xbau_uploader.init();

xbau_uploader.bind('FilesAdded', function(up, files) {
     xbau_uploader.start();
});

xbau_uploader.bind('FileUploaded', function(up, file, response){
     location.reload()
});