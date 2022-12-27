$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var weight_received = [];

    //receive details from server
    socket.on('weight', function(msg) {
        $('#weight').html(msg.data);
    });

});
