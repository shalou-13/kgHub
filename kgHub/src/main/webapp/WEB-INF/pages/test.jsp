<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>接口测试</title>
</head>
<body>
<div id="result"></div>
<script src="<%=request.getContextPath() %>/static/js/jquery-1.11.1.min.js"></script>
<script type="text/javascript">
var root = "<%=request.getContextPath() %>";
getTestResult();
function getTestResult() {
	$.ajax({
				type : "POST",
				url : root + "/getInstituteInfoByID",
				data : JSON.stringify({id:"0371F5EFDE6243F0B459505A3C81054C"}),
				success : function(data) {
					$("#result").html(data.result.instName);
				},
				datatype : "json"
			});
}
</script>
</body>
</html>