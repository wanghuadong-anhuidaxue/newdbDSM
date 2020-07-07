<%@ page language="java" contentType="text/html; charset=utf-8"
    pageEncoding="utf-8"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">

<html>

	<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<meta name=”viewport” content=”width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no” />
		<title>dbDSM</title>
		<link rel="stylesheet" href="./css/global.css" />
		<link rel="stylesheet" href="./css/all.css" />
		<link rel="stylesheet" href="./layui/layui.js">
		<link rel="stylesheet" href="./layui/css/layui.css">
		<link rel="stylesheet" type="text/css" href="./css/bootstrap.min.css" />

		
		<script src="js/jquery-1.12.4.js"></script>
		<script src="js/jquery.dataTables.min.js"></script>
		<script src="js/dataTables.buttons.min.js"></script>
		<script src="js/jszip.min.js"></script>
		<script src="js/buttons.html5.min.js"></script>
		<script type="text/javascript" language="javascript" src="js/dataTables.bootstrap.js"></script>
		<style>
			.bbtn {
				float: left;
				margin-left: 5px;
			}
			
			.pagination {
				float: right;
				margin: 0 5px;
			}
			
			#example {
				margin-bottom: 2px;
			}
			
			.dataTables_info {
				float: right;
				height: 35px;
				text-align: center;
				margin: 0 5px;
			}
			
			.dataTables_length {
				float: left;
				height: 35px;
				margin: 0 5px;
			}
		</style>
		<style>
			.bbtn {
				float: left;
				margin-left: 5px;
			}
			
			.pagination {
				float: right;
				margin: 0 5px;
			}
			
			#example {
				margin-bottom: 2px;
			}
			
			.dataTables_info {
				float: right;
				height: 35px;
				text-align: center;
				margin: 0 5px;
			}
			
			.dataTables_length {
				float: left;
				height: 35px;
				margin: 0 5px;
			}
		</style>

		<link rel="stylesheet" href="layui/css/layui.css" />
		<link rel="stylesheet" href="css/home.css" />
	</head>

	<body>
		<div class="layui-container" style="min-width:1140px;">
			<div class="layui-row" id="header">
				<!--头-->
				<div class="layui-col-xs12 layui-col-sm12 layui-col-md12 layui-col-lg12" id="banner">
				</div>
				<!--这里是banner-->
				<div class="layui-col-xs12 layui-col-sm12 layui-col-md12 layui-col-lg12" id="bar">
					<!--这里是导航栏-->
					<ul class="layui-nav" lay-filter="" id="navbar">
						<li class="layui-nav-item">
							<a href="index.jsp">Home</a>
						</li>
						<li class="layui-nav-item layui-this">
							<a href="search.jsp">Search</a>
						</li>
						<li class="layui-nav-item">
							<a href="download.jsp">Download</a>
						</li>
						<li class="layui-nav-item">
							<a href="about.jsp">About</a>
						</li>
						<li class="layui-nav-item">
							<a href="submit.jsp">Submit</a>
						</li>
						<li class="layui-nav-item">
							<a href="contact.jsp">Contact us</a>
						</li>
					</ul>
				</div>
				<!--导航栏到这-->
			</div>
			<!--头到这-->
		<fieldset class="layui-elem-field layui-field-title" style="margin-top: 50px;">
			<legend><i><b>Search Result:</b></i>&nbsp;
			    <%=(request.getParameter("Disease")==null||request.getParameter("Disease")==""?"":("<i><b>Disease</b></i>: "+request.getParameter("Disease").replace("((l))", ", ")+";&nbsp;"))%>
				<%=(request.getParameter("Gene")==null||request.getParameter("Gene")==""?"":("<i><b>Gene</b></i>:"+request.getParameter("Gene").replace("((l))", ", ")+";&nbsp;"))%>
				<%=(request.getParameter("Protein")==null||request.getParameter("Protein")==""?"":("<i><b>Protein</b></i>: "+request.getParameter("Protein").replace("((l))", ", ")+";&nbsp;"))%>
				<%=(request.getParameter("DBDSMScore")==null||request.getParameter("DBDSMScore")==""?"":("<i><b>DBDSMScore</b></i>: "+request.getParameter("DBDSMScore").replace("((l))", ", ")+";"))%>
				<%=(request.getParameter("searchBy")==null||request.getParameter("searchBy")==""?"":(request.getParameter("searchBy"))+"&nbsp;like:")%>
				<%=(request.getParameter("userinput")==null||request.getParameter("userinput")==""?"":(request.getParameter("userinput")))%>
			</legend>
		</fieldset>
		<table id="example" class="table table-striped table-bordered" align="center" lay-filter="demoEvent" style="margin:0 0 0 0;">
			<thead>
				<tr role="row">
					<th required lay-verify="required" action="details20522.jsp" id="Disease" name="Disease">Disease</th>
					<th required lay-verify="required" action="details20522.jsp" id="Gene" name="Gene">Gene</th>
					<th>SNPID</th>
					<th>GRCh38_Position</th>
					<th>c.DNA</th>
					<th>Protein</th>
					<th>dbDSMscore</th>
					<th required lay-verify="required" action="details0522.jsp" id="DBDSMID" name="DBDSMID">dbDSM_AccNum</th>
				</tr>
			</thead>
			<tfoot>
			</tfoot>
		</table>
		<div class="layui-row" id="footer" align='center'>
				<hr class="layui-bg-black">
				<div class="link">
					Links:
					<a class="ow" href="http://bioinfo.ahu.edu.cn:8080/PrDSM/" target="_blank">PrDSM</a>
					<div style="display:inline;">|</div>
					<a class="ow" href="http://bioinfo.ahu.edu.cn:8080/IDSV/" target="_blank">IDSV</a>
					<!-- <div style="display:inline;">|</div>
					<a class="ow" href="http://bioinfo.ahu.edu.cn:8080/Melanoma/index.jsp" target="_blank">Melanoma</a> -->
				</div>
				<div class="copyright">
					Copyright©
					<a class="ow" href="http://en.ahu.edu.cn/" target="_blank">AnHui University</a> ©All Rights Reserved.
				</div>
				<div class="use">
					<!-- Website content is for educational and research purposes only and is not intended to be used for medical advice, diagnosis or treatment. -->
				</div>
			</div>
	</body>

	<script src="layui/layui.all.js"></script>

	<script>
		var t = $('#example').DataTable({
			ajax: {
				url: "details?Disease=" + <%="\""+(request.getParameter("Disease")==null?"":request.getParameter("Disease"))+"\""%> +
					"&Gene=" + <%="\""+(request.getParameter("Gene")==null?"":request.getParameter("Gene"))+"\""%> 
			},
			pageLength: 10,
			"stateSave": true,
			"scrollY": "550px", 
			"scrollCollapse": true,
			"ordering":true,
			columns: [{
				    "data": "Disease",
			    },
			          
				{
					"data": "Gene",
				},
				
				{
					"data": "SNPID"
				},
				{
					"data": "GRCh38_Position"
				},
				{
					"data": "cDNA"
				},
				{
					"data": "Protein"
				},
				{
					"data": "DBDSMScore",
				},
				{
					"data": "DBDSMID",
				},
	
			],
			"dom": '<"top"li>rt<"bottom"p><"clear">',
			"columnDefs": [{},
			  	{
					"render": function(data, type, row, meta) {
					    if ((row.Disease)==""){
						    return '<a style="color:black;">' + 'n/a'+ '</a>';
					    }
					    else{
					    	return '<a style="color:#5fb878;" href="details2.jsp?Disease=' + data + '">' + row.Disease + '</a>';
					    }
					
				    },
				    "targets": 0
			    },
				{
					"render": function(data, type, row, meta) {
						if ((row.Gene)==""){
							return '<a style="color:black;">' + 'n/a'+ '</a>';
						}
						else{
							return '<a style="color:#5fb878;" href="details2.jsp?Gene=' + data + '">' + row.Gene + '</a>';
						}
					},
					"targets": 1
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.SNPID)[0]=="*"){
							return '<a style="background-color:red;color:black;">' + (row.SNPID).substring(1) + '</a>';
						}
						else{
							if ((row.SNPID)==""){
								return '<a style="color:black;">' + 'n/a'+ '</a>';
							}
							else{
								return '<a style="color:black;">' + row.SNPID + '</a>';
							}
						}
						
					},
					"targets": 2
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.GRCh38_Position)==""){
							return '<a style="color:black;">' + 'n/a'+ '</a>';
						}
						else{
							return '<a style="color:black;">' + row.GRCh38_Position + '</a>';
						}
					},
					"targets": 3
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.cDNA)[0]=="*"){
							return '<a style="background-color:red;color:black;">' + (row.cDNA).substring(1) + '</a>';
						}
						else{
							if ((row.cDNA)==""){
								return '<a style="color:black;">' + 'n/a'+ '</a>';
							}
							else{
								return '<a style="color:black;">' + row.cDNA + '</a>';
							}
						}
						
					},
					"targets": 4
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.Protein)[0]=="*"){
							return '<a style="background-color:red;color:black;">' + (row.Protein).substring(1) + '</a>';
						}
						else{
							if ((row.Protein)==""){
								return '<a style="color:black;">' + 'n/a'+ '</a>';
							}
							else{
								return '<a style="color:black;">' + row.Protein + '</a>';
							}
						}
						
					},
					"targets": 5
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.DBDSMScore)==""){
							return '<a style="color:black;">' + 'n/a'+ '</a>';
						}
						else{
							return '<a style="color:black;">' + row.DBDSMScore + '</a>';
						}
					},
					"targets": 6
				},
				{
					"render": function(data, type, row, meta) {
						if ((row.DBDSMID)==""){
							return '<a style="color:black;">' + 'n/a'+ '</a>';
						}
						else{
							return '<a style="color:#5fb878;" href="details.jsp?DBDSMID=' + data + '">' + row.DBDSMID + '</a>';
						}
					},
					//指定是第三列
					"targets": -1
				},
				

			],

		});
		layui.use('element', function() {
			var element = layui.element;
		});
		layui.use('table', function() {
			var table = layui.table;
		});
	</script>

</html>