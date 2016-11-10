require([
  'jquery','table-sort','bootstrap-tabs','bootstrap-tooltip'
], function($,tst,tabs,tp) {
  'use strict';
$(document).ready(function(){ 
	$(".nav-tabs a").mouseover(function (e) {
		  e.preventDefault();
		  $(this).tab('show');
		});
	$(".nav-tabs").on("click","a",function (e) {
		  e.preventDefault();
		  var url = $(this).attr("data-js-target");
		  window.location.href = url;
		  return false;
		});
	$('#favcontent').on('click','.unfavorite', function(){
		  var uid = $(this).attr('rel');
		  var action = $("#favcontent").attr('data-ajax-target');
			var states = {'uid': uid};
			$(this).removeClass('off').addClass('on');			
			$.post(action, states, function(result){
			var res = result["result"];
				if (res == 1) {
				$("#favcontent td.on").parent().hide();
				return false;
				}
				else {return false;}
			}, 'json');
		
		});
	$('[data-toggle="tooltip"]').tooltip();			

	});
});