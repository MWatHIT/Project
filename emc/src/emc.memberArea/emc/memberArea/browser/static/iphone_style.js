require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){
	$('#tablecontent').on('click','.iphone-style', function(){
		var id = $(this).attr('rel');
		var checkboxID = '#' + id;
		var action = $(this).parent().attr('data-target');
		var state = $(checkboxID).attr('data-state');
		var states = {'id': id,'state': state};
		if ($(checkboxID)[0].checked == true) {	
			$(this).animate({backgroundPosition: '0% 100%'},500);
			$(checkboxID)[0].checked = false;
			$(this).removeClass('on').addClass('off');			
			$.post(action, states, function(result){
				if (result) {
					$(checkboxID).attr('data-state','processed');
					var old = $('#todo').html();
					var newnum = (Number(old) - 1).toString();
					$('#todo').html(newnum);					    					
				}
				else {return false;}
			}, 'json');
		}else {
			$(this).animate({backgroundPosition: '100% 0%'},500);
			$(checkboxID)[0].checked = true;
			$(this).removeClass('off').addClass('on');			
			$.post(action, states, function(result){
				if (result) {
					$(checkboxID).attr('data-state','unprocessed');
					var old = $('#todo').html();
					var newnum = (Number(old) + 1).toString();
					$('#todo').html(newnum); 								
				}
			else {return false;}
			}, 'json');
		}
	});
	});
	});