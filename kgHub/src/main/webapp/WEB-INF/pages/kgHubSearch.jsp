<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" href="<%=request.getContextPath() %>/static/bootstrap-3.3.7/css/bootstrap.min.css">
<title>KgHub搜索</title>
<style type="text/css">
.result_seg h4{
	color: #4177D4;font-weight: bold;
}

.result_seg ul{
	list-style: none;
	padding: 0 0;
}
.result_seg ul li{
	padding: 8px 2px;
	word-wrap: break-word;
	word-break: normal;
}
.result_seg ul li:hover{
	background-color: #ccc;
}
</style>
</head>
<body>
<div class="container">
	<br/><br/><br/>
	<div class="row">
	  	<div class="col-lg-12">
	    	<div class="input-group">
	      	<input type="text" class="form-control" id="keyword" placeholder="Search for...">
	      	<span class="input-group-btn">
	        	<button class="btn btn-default" type="button" id="search">Go!</button>
	      	</span>
	    	</div>
	  	</div>
	</div>
	<div class="row">
		<div class="col-lg-12">
		<br/>
		<h3>查询结果</h3>
		<div id="result" class="col-lg-12">
		</div>
		</div>
	</div>
</div>
<script src="<%=request.getContextPath() %>/static/js/jquery-1.11.1.min.js"></script>
<script src="<%=request.getContextPath() %>/static/bootstrap-3.3.7/js/bootstrap.min.js"></script>
<script type="text/javascript">
var root = "<%=request.getContextPath() %>";
$("#search").click(function(){
	var keyword  = $.trim($("#keyword").val());
	if(keyword){
		getSearchResult(keyword);
	}
});

function getSearchResult(keyword) {
	$.ajax({
				type : "POST",
				url : root + "/searchGraph",
				data : JSON.stringify({text:keyword}),
				success : function(data) {
					$("#result").empty();
					if(data.state==3000){
						for(var graphID in data.result){
							var rtl = "" ;
							var ell = "";
							var el = ""; 
							var tresult = ""; 
							var sresult = ""; 
							var sub_rtl = ""; 
							var sub_ell = ""; 
							var sub_el = "";
							var sub_result = data.result[graphID].result;
							if(data.result[graphID].state==4000){
								if(sub_result.RTL && sub_result.RTL.length){
									for(var i=0;i<sub_result.RTL.length;i++){
										rtl = rtl + "<li>"+JSON.stringify(sub_result.RTL[i])+"</li>";
									}
								}else{
									rtl = "<li>空</li>";
								}
								if(sub_result.ELL && sub_result.ELL.length){
									for(var i=0;i<sub_result.ELL.length;i++){
										ell = ell + "<li>"+JSON.stringify(sub_result.ELL[i])+"</li>"
									}
								}else{
									ell = "<li>空</li>";
								}
								if(sub_result.EL && sub_result.EL.length){
									for(var i=0;i<sub_result.EL.length;i++){
										el = el + "<li>"+JSON.stringify(sub_result.EL[i])+"</li>";
									}
								}else{
									el = "<li>空</li>";
								}
								if(sub_result.TResult && sub_result.TResult.length){
									for(var i=0;i<sub_result.TResult.length;i++){
										tresult = tresult + "<li>结点</li>";
										for(var j=0;j<sub_result.TResult[i].nodes.length;j++){
											tresult = tresult + "<li>"+JSON.stringify(sub_result.TResult[i].nodes[j])+"</li>";
										}
										tresult = tresult + "<li>边</li>"
										for(var m=0;m<sub_result.TResult[i].edges.length;m++){
											tresult = tresult + "<li>"+JSON.stringify(sub_result.TResult[i].edges[m])+"</li>";
										}
									}
								}else{
									tresult = "<li>空</li>";
								}
								if(sub_result.SResult && sub_result.SResult.length){
									for(var i=0;i<sub_result.SResult.length;i++){
										sresult = sresult + "<li>"+JSON.stringify(sub_result.SResult[i])+"</li>";
									}
								}else{
									sresult = "<li>空</li>";
								}
								if(sub_result.sub_RTL && sub_result.sub_RTL.length){
									for(var i=0;i<sub_result.sub_RTL.length;i++){
										sub_rtl = sub_rtl + "<li>"+JSON.stringify(sub_result.sub_RTL[i])+"</li>";
									}
								}else{
									sub_rtl = "<li>空</li>";
								}
								if(sub_result.sub_ELL && sub_result.sub_ELL.length){
									for(var i=0;i<sub_result.sub_ELL.length;i++){
										sub_ell = sub_ell + "<li>"+JSON.stringify(sub_result.sub_ELL[i])+"</li>";
									}
								}else{
									sub_ell = "<li>空</li>";
								}
								if(sub_result.sub_EL && sub_result.sub_EL.length){
									for(var i=0;i<sub_result.sub_EL.length;i++){
										sub_el = sub_el + "<li>"+JSON.stringify(sub_result.sub_EL[i])+"</li>"
									}
								}else{
									sub_el = "<li>空</li>";
								}
							}
							var temp = '<div class="result_seg col-lg-12"><h4>'+graphID+'(score:'+sub_result.weight+')</h4>'+
							'<div class="col-lg-12"><label>RTL</label><ul class="col-lg-12">'+rtl+'</ul></div>'+
							'<div class="col-lg-12"><label>ELL</label><ul class="col-lg-12">'+ell+'</ul></div>'+
							'<div class="col-lg-12"><label>EL</label><ul class="col-lg-12">'+el+'</ul></div>'+
							'<div class="col-lg-12"><label>TResult</label><ul class="col-lg-12">'+tresult+'</ul></div>'+
							'<div class="col-lg-12"><label>SResult</label><ul class="col-lg-12">'+sresult+'</ul></div>'+
							'<div class="col-lg-12"><label>sub_RTL</label><ul class="col-lg-12">'+sub_rtl+'</ul></div>'+
							'<div class="col-lg-12"><label>sub_ELL</label><ul class="col-lg-12">'+sub_ell+'</ul></div>'+
							'<div class="col-lg-12"><label>sub_EL</label><ul class="col-lg-12">'+sub_el+'</ul></div>'+
							'</div>';
							$("#result").append(temp);
						}
					}
				},
				datatype : "json"
			});
}
</script>
</body>
</html>