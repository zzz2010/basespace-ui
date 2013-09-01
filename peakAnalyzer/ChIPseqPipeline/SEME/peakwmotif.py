<html><head><title>SEME Result</title>
<?#  <link rel="stylesheet" type="text/css" href="./resources/css/ext-all.css" />?>
</head>
<body>
<?function mainfunction(){
	 $rootdir="/home/chipseq/public_html/";
	 $rooturl="http://biogpu.ddns.comp.nus.edu.sg/~chipseq/";
	$runDir=$_REQUEST['rundir'];
	$hashvalue="SEME_clust.pwm";
	$resultLink="$rooturl/$runDir";
	?>

<a href=<? echo "$resultLink/