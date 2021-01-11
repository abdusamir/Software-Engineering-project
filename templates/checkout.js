$(document).ready(function(){
    $('#a').click(function(){
        if($(this).prop("checked") == true){
          $("#result").show();
          $('.c').not(this).prop('checked', false);
          
        }
        else if($(this).prop("checked") == false){
            $("#result").hide();
          $("#a").not(this).prop('checked', false);
        }
    });

});
  $(document).ready(function(){
    $('#b').click(function(){
        if($(this).prop("checked") == true){
          $('.c').not(this).prop('checked', false);
          $("#result").hide();
        }
        
    });

});