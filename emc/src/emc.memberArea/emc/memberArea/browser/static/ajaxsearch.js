/*!
 * Bootstrap v3.3.2 (http://getbootstrap.com)
 * Copyright 2011-2015 Twitter, Inc.
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 */
function closeEventMore() {
  $("#cata_more_div").hide(), $("#address_more_div").hide()
}
function innerMoreArea() {
  var a = $("#ajaxmorearea").attr("data-ajax-target"),
    b = {
      demo: 2
    };
  $.post(a, b, function(a) {
    try {
      $("#addressSearchMore1").html("");
      var b = a.provincelist;
      $(b).appendTo("#province_list_div"), $("#li_province_more").hide()
    } catch(c) {
      alert(c)
    }
  }, "json")
}
function closeSearchEventsDiv(a) {
  1 == a ? ($("#dateSearch").val("0"), $("#dateRangeSearchUl > .over").removeClass("over"), $("#dateRangeSearchUl").find("li[data-name='0']").addClass("over"), searchEvent()) : 2 == a ? ($("#addressSearch").val("0"), $("#addressSelectSearch li> .over").removeClass("over"), $("#addressSelectSearch").find("li span[data-name='0']").addClass("over"), searchEvent()) : 3 == a && ($("#categorySearch").val("0"), $("#categorySelectSearch li> .over").removeClass("over"), $("#categorySelectSearch").find("li span[data-name='0']").addClass("over"), searchEvent())
}
function searchEventParent() {
  searchEvent()
}
function showResultRemind(a, b, c, d) {
  var e = "";
  "" !== a || "0" == b && "0" == c && "0" == d ? "" === a || "0" == b && "0" == c && "0" == d || (e = createStringSearch(a, b, c, d)) : e = createStringSearch(a, b, c, d), "" === a && "0" == b && "0" == c && "0" == d && (e = "<li class='a'>已选择：</li><li id='show_site_result'></li><li class='info' id='searchresultinfor'>“<span id='keyworkshow'>所有</span>”的社会组织信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"), "" !== a && "0" == b && "0" == c && "0" == d && (e = "<li class='a'>已选择：</li><li id='show_site_result'></li><li class='info' id='searchresultinfor'>有关“<span id='keyworkshow'>" + a + "</span>”的社会组织信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"), $("#all_result_recordinfo").html(e)
}
function createStringSearch(a, b, c, d) {
  var e = "<li class='a'>已选择：</li><li id='show_site_result'>",
    f = "";
  switch(b) {
  case "1":
    f = "最近一周", e += "<div class='select'  onclick=\"closeSearchEventsDiv(1)\" >时间：<span id='search_site_desc' style='cursor: pointer;vertical-align: middle;'>" + f + " </span></div>";
    break;
  case "2":
    f = "最近一月", e += "<div class='select'  onclick=\"closeSearchEventsDiv(1)\" >时间：<span  style='cursor: pointer;vertical-align: middle;'>" + f + " </span></div>";
    break;
  case "3":
    f = "最近一年", e += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span  style='cursor: pointer;vertical-align: middle;'>" + f + " </span></div>";
    break;
  case "4":
    f = "30天内", e += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span style='cursor: pointer;vertical-align: middle;'>" + f + " </span></div>";
    break;
  case "5":
    f = "30天后", e += "<div class='select' onclick=\"closeSearchEventsDiv(1)\">时间：<span style='cursor: pointer;vertical-align: middle;'>" + f + " </span></div>"
  }
  var g = "";
  "0" == c ? g = "所有" : (g = $(document.getElementById("addressSelectSearch")).find("span[data-name='" + c + "'] a").html(), e += "<div class='select' onclick=\"closeSearchEventsDiv(2)\">公告类别：<span style='cursor: pointer;vertical-align: middle;' >" + g + " </span></div>");
  var h = "";
  return "0" == d ? h = "所有" : (h = $(document.getElementById("categorySelectSearch")).find("span[data-name='" + d + "'] a").html(), e += "<div class='select' onclick=\"closeSearchEventsDiv(3)\">分类：<span style='cursor: pointer;vertical-align: middle;' >" + h + " </span></div>"), e += "" === a ? "</li><li class='info' id='searchresultinfor'>的信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>" : "</li><li class='info' id='searchresultinfor'>中有关“<span>" + a + "</span>”的信息有“<span id='searchresult_count'>" + totalCountSearchEvent + "</span>”条！</li>"
}
if("undefined" == typeof jQuery) throw new Error("Bootstrap's JavaScript requires jQuery"); + function(a) {
  "use strict";
  var b = a.fn.jquery.split(" ")[0].split(".");
  if(b[0] < 2 && b[1] < 9 || 1 == b[0] && 9 == b[1] && b[2] < 1) throw new Error("Bootstrap's JavaScript requires jQuery version 1.9.1 or higher")
}(jQuery), $.extend({
  getUrlVars: function() {
    for(var a, b = [], c = window.location.href.slice(window.location.href.indexOf("?") + 1).split("&"), d = 0; d < c.length; d++) a = c[d].split("="), b.push(a[0]), b[a[0]] = a[1];
    return b
  },
  getUrlVar: function(a) {
    return $.getUrlVars()[a]
  }
});
var searchEvent = function(a, b, c) {
  var d;
  d = void 0 !== c && "" !== c ? c : $("#searchKeyword").val();
  var e = $("#dateSearch").val(),
    f = $("#addressSearch").val(),
    g = $("#categorySearch").val(),
    h = $("#solrSortColumn").val(),
    i = $("#solrSortDirection").val(),
    j = {
      datetype: e,
      province: f,
      type: g
    };
  if(j.sortcolumn = h, j.sortdirection = i, j.searchabletext = void 0 === d || null === d || "" === d ? "" : d, void 0 !== a && "" !== a) {
    var k = a > 0 ? (a - 1) * b : 0;
    j.start = k, j.size = b
  } else j.start = 0, j.size = 10;
  var l = $("#ajaxsearch").attr("data-ajax-target");
  $.post(l, j, function(a) {
    try {
      showSearchEventResult(a, !0, d), showResultRemind(d, e, f, g)
    } catch(b) {
      alert(b)
    }
  }, "json")
}, totalCountSearchEvent = 0,
  showSearchEventResult = function(a) {
    var b = "",
      c = parseInt(a.size, 10),
      d = parseInt(a.start, 10),
      e = parseInt(a.total, 10);
    totalCountSearchEvent = e;
    var f = d + c > e ? e - d : c;
    f > 0 ? (generatePageLink(d, c, e), b += a.searchresult) : (document.getElementById("bottomPageId").innerHTML = "", b += '<tr class="div_tip">', b += '<td class="alert alert-block span12" colspan="7">警告！：没有搜索到您要找的信息。</td></tr>'), $("#searchResultDiv").html(b)
  }, generatePageLink = function(a, b, c) {
    var d = $("#bottomPageId"),
      e = Math.floor(c / b) + (c % b === 0 ? 0 : 1);
    0 === e && (e = 1);
    var f = Math.floor(a / b) + 1,
      g = $("#fastPageList");
    g.html("");
    var h = "",
      i = "",
      j = $("#searchtext").val();
    (void 0 === j || null == j || "" === j) && (j = ""), 1 >= f ? (i += "<li class='previous'><a href='javascript:void(0)'><span aria-hidden='true'>&larr;</span> 前一页</a></li>", h += "<li class='disabled'><a href='javascript:void(0)' >首页</a></li>", h += "<li class='disabled'><a aria-label='Previous' href='javascript:void(0)' ><span aria-hidden='true'>&laquo;</span></a></li>") : (i += "<li class='previous'><a href='javascript:searchEvent(" + (f - 1) + ",10)'><span aria-hidden='true'>&larr;</span> 前一页</a></li>", h += "<li><a href=javascript:searchEvent(1,10) >首页</a></li><li><a page_over num active href=javascript:searchEvent(" + (f - 1) + ",10) ><span aria-hidden='true'>&laquo;</span></a></li>"), i += "<li><span>" + f + "/" + e + "</span></li>";
    var k = 1,
      l = 3;
    1 == f ? (k = 1, l = f + 2, l >= e && (l = e)) : f == e ? (k = e - 2, 0 >= k && (k = 1), l = e) : (k = f - 1, l = f + 1);
    for(var m = k; l >= m; m++) h += f == m ? "<li class='active'><a href='#'>" + m + "</a></li>" : "<li><a href=javascript:searchEvent(" + m + ",10) class='page num'>" + m + "</a></li>";
    f == e || 2 > e ? (i += "<li class='next'><a href='javascript:void(0)'><span aria-hidden='true'>&rarr;</span> 下一页</a></li>", h += "<li class='disabled'><a href='javascript:void(0)' ><span aria-hidden='true'>&raquo;</span></a></li>", h += "<li class='disabled'><a href='javascript:void(0)' >末页</a></li>") : (i += "<li class='next'><a href='javascript:searchEvent(" + (f + 1) + ",10)'><span aria-hidden='true'>&rarr;</span> 下一页</a></li>", h += "<li><a href=javascript:searchEvent(" + (f + 1) + ",10)><span aria-hidden='true'>&raquo;</span></a><li><a href=javascript:searchEvent(" + e + ",10) >末页</a></li>"), d.html(h), g.html(i)
  };
$(document).ready(function() {
  var a = $.getUrlVar("orgname");
  if(void 0 === a || null == a || "" === a) searchEvent();
  else {
    var b = decodeURIComponent(a);
    $("#searchKeyword").val(b), searchEvent()
  }
  $("#dateRangeSearchUl").on("click", "li", function() {
    return "title" == $(this).attr("class") || ($("#dateRangeSearchUl > .over").removeClass("over"), $(this).addClass("over"), $("#dateSearch").attr("value", $(this).attr("data-name")), searchEvent()), !1
  }), $("#addressSelectSearch li").on("click", "span", function() {
    return "title" == $(this).attr("class") || "more" == $(this).attr("class") || ($("#addressSelectSearch li> .over").removeClass("over"), $(this).addClass("over"), $("#addressSearch").attr("value", $(this).attr("data-name")), searchEvent()), !1
  }), $("#categorySelectSearch li").on("click", "span", function() {
    return "title" == $(this).attr("class") || "more" == $(this).attr("class") || ($("#categorySelectSearch li> .over").removeClass("over"), $(this).addClass("over"), $("#categorySearch").attr("value", $(this).attr("data-name")), searchEvent()), !1
  }), $("#eventListSort").on("click", ".glyphicon", function() {
    return $("#solrSortColumn").attr("value", $(this).attr("data-name")), "glyphicon glyphicon-arrow-up" == $(this).attr("class") ? ($(this).attr("class", "glyphicon glyphicon-arrow-down"), $(this).parent().attr("class", "text-success"), $("#solrSortDirection").attr("value", "ascending")) : ($(this).attr("class", "glyphicon glyphicon-arrow-up"), $("#solrSortDirection").attr("value", "reverse")), searchEvent(), !1
  }), $("#eventListSort").on("click", "a", function() {
    return $("#eventListSort > .over").removeClass("over"), $("#eventListSort a").attr("style", ""), $(this).attr("style", "font-weight:bold;color:#279006;"), !1
  }), $("#search").on("click", "button", function() {
    return searchEventParent(), !1
  })
});