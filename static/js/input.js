(function(){
  $("#submitsimulation").click(function(){
    var formdata = {'tamil':'englsh'};
    $.ajax({
        type: "POST",
        url: "simulation", //process to mail
        data: formdata,
        success: function(msg){
            alert("Sucess");
        },
        error: function(){
            alert("failure");
        }
    });
    alert('Tamil Submited');
  });
}());
