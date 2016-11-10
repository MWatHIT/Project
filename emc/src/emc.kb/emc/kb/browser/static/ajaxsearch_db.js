/*jshint sub:true*/
// base lib
function searchEventParent() {
    searchEvent();
}
// read url query string
$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});

var searchEvent = function(jumpPage, rows, initKeyword) { 
    var keyword;
    if (initKeyword !== undefined && initKeyword !== "") {
        keyword = initKeyword;
    } else {
        keyword = $("#searchKeyword").val();
    }	  
    var sortColumn = $("#solrSortColumn").val();    
    var sortDirection = $("#solrSortDirection").val();        
    var data = {};
    if (keyword === undefined || keyword === null || keyword === "") {
           data['searchabletext'] = "";
    } else {
           data['searchabletext'] = keyword;
    }    
    data['sortcolumn'] = sortColumn;
    data['sortdirection'] = sortDirection;      

    if (jumpPage !== undefined && jumpPage !== "") 
    {   var start = jumpPage > 0 ? (jumpPage - 1) * rows : 0;
        data['start'] = start;
        data['size'] = rows;
    } else {
        data['start'] = 0;
        data['size'] =10;
    }        
       var action = $("#ajaxsearch").attr('data-ajax-target');
       $.post(action, 
           data,
           function(resp) {
                       try {
                			showSearchEventResult(resp, true, keyword);
            				}
                       catch(e){alert(e);}
                       	   },
            'json');             

};
var totalCountSearchEvent = 0;
var showSearchEventResult = function(D, u, C) {
//function showSearchEventResult(D, u, C) {
//D json response
// u true
// c keyword
//size batch size
//start batch start
//total return result total

    var a = "";
    var h = "";
    var o = parseInt(D['size'],10);
    var l = parseInt(D['start'],10);
    var p = parseInt(D['total'],10);
    totalCountSearchEvent = p;
    var e = (l + o) > p ? (p - l) : o;
    if (e > 0) {
        generatePageLink(l, o, p); 
       a +=  D['searchresult']; 
    } else {
     $("#bottomPageId").html("");
        a += '<tr class="div_tip">';
        a += '<td class="alert alert-block span12" colspan="7">警告！：没有搜索到您要找的信息。</td></tr>';
    		}
$("#searchResultDiv").html(a);
};


var generatePageLink = function(c, n, a) {
    // c: start n:size  a: total
	  var f = $("#bottomPageId");
    // k pages number
	  var k = Math.floor(a / n) + (a % n === 0 ? 0 : 1);
    if (k === 0) {
        k = 1;
    }
    // l current page number
    var l = Math.floor(c / n) + 1;
    var j = $("#fastPageList");
    j.html("");
    // e fast link
    // d pagenation link 
    var d = "";
    var e = "";
    var m = $("#searchtext").val();
    if (m === undefined || m == null || m === "") {
        m = "";
    }
    if (l <= 1) {
        e += "<li class='previous'><a href='javascript:void(0)'>" +
        		"<span aria-hidden='true'>&larr;</span>前一页</a></li>";
        d += "<li class='disabled'><a href='javascript:void(0)'>首页</a></li>";
        d += "<li class='disabled'><a aria-label='Previous' href='javascript:void(0)'>" +
        		"<span aria-hidden='true'>&laquo;</span></a></li>";
    } else {
        e += "<li class='previous'><a href='javascript:searchEvent(" +
        (l - 1) + ",10)'><span aria-hidden='true'>&larr;</span>前一页</a></li>";
        d += "<li><a href=javascript:searchEvent(1,10)>首页</a></li>" +
        		"<li><a page_over num active href=javascript:searchEvent(" + (l - 1) + ",10) >" +
        		"<span aria-hidden='true'>&laquo;</span></a></li>";
    }
    e += "<li><span>" + l + "/" + k + "</span></li>";
    var b = 1;
    var h = 3;
    if (l == 1) {
        b = 1;
        h = l + 2;
        if (h >= k) {
            h = k;
        }
    } else {
        if (l == k) {
            b = k - 2;
            if (b <= 0) {
                b = 1;
            }
            h = k;
        } else {
            b = l - 1;
            h = l + 1;
        }
    }
    for (var g = b; g <= h; g++) {
        if (l == g) {
            d += "<li class='active'><a href='#'>" + g + "</a></li>";
        } else {
            d += "<li><a href=javascript:searchEvent(" + g + ",10) class='page num'>" + g + "</a></li>";
        }
    }
    if (l == k || k < 2) {
        e += "<li class='next'><a href='javascript:void(0)'><span aria-hidden='true'>&rarr;</span> 下一页</a></li>";
        d += "<li class='disabled'><a href='javascript:void(0)' >" +
        		"<span aria-hidden='true'>&raquo;</span></a></li>";
        d += "<li class='disabled'><a href='javascript:void(0)' >末页</a></li>";
    } else {
        e += "<li class='next'><a href='javascript:searchEvent(" + (l + 1) + ",10)'><span aria-hidden='true'>&rarr;</span> 下一页</a></li>";
        d += "<li><a href=javascript:searchEvent(" + (l + 1) + ",10)><span aria-hidden='true'>&raquo;</span></a>" +
        		"<li><a href=javascript:searchEvent(" + (k) + ",10) >末页</a></li>";
    }
   f.html(d);
   j.html(e);
};

$(document).ready(function(){
// read query string
// Getting URL var by its nam
    var byName = $.getUrlVar('orgname');
    if (byName === undefined || byName == null || byName === "") {
               searchEvent();
    } else {
               var byName2 = decodeURIComponent(byName);
               $("#searchKeyword").val(byName2);    
               searchEvent();
    }
   $("#search").on("click","button",function(){ searchEvent();});
   
   $("#eventListSort").on("click","a",function() {             
                $("#solrSortColumn").attr("value", $(this).attr("data-name"));
                //a reverse,will be ascending
                if ($(this).attr("class") == "a") {
                    $(this).attr("class", "b");
                    $(this).find("span.glyphicon").addClass("glyphicon-arrow-down").removeClass("glyphicon-arrow-up");
                    $("#solrSortDirection").attr("value", "ascending");
                } else {
                    $(this).attr("class", "a");
                    $(this).find("span.glyphicon").addClass("glyphicon-arrow-up").removeClass("glyphicon-arrow-down");
                    $("#solrSortDirection").attr("value", "reverse");
                }
                searchEvent();
       return false; 
        });                 
});
