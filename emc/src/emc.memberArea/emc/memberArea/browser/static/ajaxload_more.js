require([
  'jquery',
  'bootstrap-tooltip'
], function($,tp) {
  'use strict';
$(document).ready(function(){
$('[data-toggle="tooltip"]').tooltip();
var start=0;	
$("#ajaxmore-link").on("click","#ajaxmore",function() {        
       var action = $("#ajaxdisplay").attr('data-ajax-target');
	   start++;
       $.post(action, 
           {formstart:start},
           function(data) {
        	   	var outhtml = data['outhtml'];
        	   	$(outhtml).appendTo('#tablecontent');
        	   	var pending = data['pending'];
        	   	$("#pending").text(pending);
        	   	var ifmore = data['ifmore'];
        	   	if (ifmore==1){
			   			$('#ajaxmore-link').remove();
        	   										}
            									},
           'json');        
       return false;
    });
 });
});