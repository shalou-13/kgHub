<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link rel="stylesheet" href="<%=request.getContextPath() %>/static/bootstrap-3.3.7/css/bootstrap.min.css">
<title>KgHub搜索</title>
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
			<div>
				<label>RTL</label>
				<ul id="RTL"></ul>
			</div>
			<div>
				<label>ELL</label>
				<ul id="ELL"></ul>
			</div>
			<div>
				<label>EL</label>
				<ul id="EL"></ul>
			</div>
			<div>
				<label>TResult</label>
				<ul id="TResult"></ul>
			</div>
			<div>
				<label>SResult</label>
				<ul id="SResult"></ul>
			</div>
			<div>
				<label>sub_RTLL</label>
				<ul id="sub_RTL"></ul>
			</div>
			<div>
				<label>sub_ELL</label>
				<ul id="sub_ELL"></ul>
			</div>
			<div>
				<label>sub_EL</label>
				<ul id="sub_EL"></ul>
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
					$("ul").empty();
					if(data.state==4000){
						if(data.result.RTL && data.result.RTL.length){
							for(var i=0;i<data.result.RTL.length;i++){
								$("#RTL").append("<li>"+JSON.stringify(data.result.RTL[i])+"</li>");
							}
								
						}else{
							$("#RTL").append("<li>空</li>");
						}
						if(data.result.ELL && data.result.ELL.length){
							for(var i=0;i<data.result.ELL.length;i++){
								$("#ELL").append("<li>"+JSON.stringify(data.result.ELL[i])+"</li>");
							}
								
						}else{
							$("#ELL").append("<li>空</li>");
						}
						if(data.result.EL && data.result.EL.length){
							for(var i=0;i<data.result.EL.length;i++){
								$("#EL").append("<li>"+JSON.stringify(data.result.EL[i])+"</li>");
							}
								
						}else{
							$("#EL").append("<li>空</li>");
						}
						if(data.result.TResult && data.result.TResult.length){
							for(var i=0;i<data.result.TResult.length;i++){
								$("#TResult").append("<li>结点</li>");
								for(var j=0;j<data.result.TResult[i].nodes.length;j++){
									$("#TResult").append("<li>"+JSON.stringify(data.result.TResult[i].nodes[j])+"</li>");
								}
								$("#TResult").append("<li>边</li>");
								for(var m=0;m<data.result.TResult[i].edges.length;m++){
									$("#TResult").append("<li>"+JSON.stringify(data.result.TResult[i].edges[m])+"</li>");
								}
							}
						}else{
							$("#TResult").append("<li>空</li>");
						}
						if(data.result.SResult && data.result.SResult.length){
							for(var i=0;i<data.result.SResult.length;i++){
								$("#SResult").append("<li>"+JSON.stringify(data.result.SResult[i])+"</li>");
							}
						}else{
							$("#SResult").append("<li>空</li>");
						}
						if(data.result.sub_RTL && data.result.sub_RTL.length){
							for(var i=0;i<data.result.sub_RTL.length;i++){
								$("#sub_RTL").append("<li>"+JSON.stringify(data.result.sub_RTL[i])+"</li>");
							}
								
						}else{
							$("#sub_RTL").append("<li>空</li>");
						}
						if(data.result.sub_ELL && data.result.sub_ELL.length){
							for(var i=0;i<data.result.sub_ELL.length;i++){
								$("#sub_ELL").append("<li>"+JSON.stringify(data.result.sub_ELL[i])+"</li>");
							}
								
						}else{
							$("#sub_ELL").append("<li>空</li>");
						}
						if(data.result.sub_EL && data.result.sub_EL.length){
							for(var i=0;i<data.result.sub_EL.length;i++){
								$("#sub_EL").append("<li>"+JSON.stringify(data.result.sub_EL[i])+"</li>");
							}
								
						}else{
							$("#sub_EL").append("<li>空</li>");
						}
					}
				},
				datatype : "json"
			});
}
</script>
</body>
</html>