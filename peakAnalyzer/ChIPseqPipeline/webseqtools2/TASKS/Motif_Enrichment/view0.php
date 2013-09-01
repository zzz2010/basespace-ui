<html><head><title>CentDist Result</title>
<?php
#  <link rel="stylesheet" type="text/css" href="./resources/css/ext-all.css" />?>
</head>
<body>
<?php
include_once('../../common.inc')?>

<?php

error_reporting(E_ALL);
// Function to calculate square of value - mean
function sd_square($x, $mean) { return pow($x - $mean,2); }

// Function to calculate standard deviation (uses sd_square)    
function sd($array) {
    
// square root of sum of squares devided by N-1
return sqrt(array_sum(array_map("sd_square", $array, array_fill(0,count($array), (array_sum($array) / count($array)) ) ) ) / (count($array)-1) );
}
?>

<?php
function mainfunction(){
	global $email;
	global $handle;
	global $rootdir;
	global $rooturl;
	$userdir="userdata/$handle";
	$jobid=$_REQUEST['jobid'];
	$jobdir="$rootdir/userdata/$handle/$jobid";
	#echo $jobdir."<br>";
	$title=readfile1("$rootdir/userdata/$handle/$jobid/input/title");
	echo "<header style='size:20'>Results for $title</header>";
	$runDir="$jobdir/output";
	$hashvalue="fastafile";
	$resultLink="$rooturl/userdata/$handle/$jobid/output";
	$table=readtable("$runDir/results.txt");
	$temp=explode("\n",readfile1("$jobdir/input/motifgroup"));
	$motifnamegroup=array();
	$motifgroupname=array();
	$motifgroupnamehash=array();
	foreach($temp as $line){
		$row=explode("\t",trim($line));
		$motifname=$row[0];
		$motifgroup=$row[1];
		if (!isset($motifnamegroup[$motifname])){
			$motifnamegroup[$motifname]=array();
		}
		if (!isset($motifgroupname[$motifgroup])){
			$motifgroupname[$motifgroup]=array();
		}
		/*
		array_push($motifnamegroup[$motifname],$motifgroup);
		array_push($motifgroupname[$motifgroup],$motifname);
		*/
		$motifnamegroup[$motifname][$motifgroup]=1;
		$motifgroupname[$motifgroup][$motifname]=1;
	}
	$motifnamebest=array();
	


	$table2=array();
	foreach ($table as $row){
		$name=basename($row["NAME"]);
		$name=substr($name,0,strlen($name)-4);
		$row["NAME"]=$name;
		$score=$row["Z0SCORE"];
		if (isset($motifnamegroup[$name])){
			$row["GROUP"]=$motifnamegroup[$name];
			foreach ($row["GROUP"] as $motifgroup=>$dummy){
				if (!isset($motifgroupbest[$motifgroup]) || $motifgroupbest[$motifgroup]["Z0SCORE"]<$score){
					$motifgroupbest[$motifgroup]=$row;
				}
			}
		} else {
			$row["GROUP"]=array();
		}
		$table2[$name]=$row;
	}
	array_multisort(getcol($motifgroupbest,"Z0SCORE"),SORT_DESC,$motifgroupbest);
	array_multisort(getcol($table2,"Z0SCORE"),SORT_DESC,$table2);

/*******compute P-value**********/
	require_once "../../../PDL/NormalDistribution.php";
	$hashset=array();
	$scorelist=array();
	$rowcnt=0;
	$skip=0.2*count($table2);
	echo count($table2)." TFs";
	foreach($table2 as $row)
	{
		if($skip<$rowcnt&&$row["SCORE"]>-100)//count($hashset)
			array_push($scorelist,$row["SCORE"]);
		$rowcnt++;
	}
	$sdvalue=sd($scorelist);
	$mean=array_sum($scorelist) / count($scorelist);
	$statobj=new NormalDistribution($mean,$sdvalue);
/*******compute P-value**********/

	if ($_REQUEST["show"]=="family"){
		$showmode="family";
	}
	else if ($_REQUEST["show"]=="factor"){
		$showmode="factor";
	}
	else {
		$showmode="family";
	}
	if ($showmode=="family"){
		$table=$motifgroupbest;
	}
	else {
		$table=$table2;
	}
	if ($_REQUEST["top"]<999999&&$_REQUEST["top"]>0){
		$showtop=$_REQUEST["top"];
	} else {
		$showtop=10;
	}
	#if isset($_REQUEST["family"]){
	$showfamily=$_REQUEST["family"];
	#}



	$i=0;
	echo "<form>";
	echo "Show top <input name=top value=50 size=1> <select name=show><option value=family>Families</option><option value=factor>Factors</option></select>";
	echo "<input type=checkbox> using custom motif family";
	echo "<input type=submit value=Go>";
	echo "<input type=hidden name=email value=$email>";
	echo "<input type=hidden name=handle value=$handle>";
	echo "<input type=hidden name=jobid value=$jobid>";
	echo "</form>";
	echo '<table ALIGN="CENTER" border="1px" cellpadding="0px" cellspacing="0px" width=95%>';
	echo "<tr align=center>";
		echo "<td style='white-space:nowrap'>".ahref("","Clear All")."<br>".ahref("","Check Top")." <input value=50 size=1></td>";
		echo "<td>Name</td>";
		echo "<td>Family</td>";
		echo "<td>Logo</td>";
		echo "<td>LogoR</td>";
		echo "<td>Score</td>";
		echo "<td>Distribution</td>";
		echo "<td>Binding Range</td>";
		echo "<td>Threshold</td>";
		echo "<td>Z0Score</td>";
		echo "<td>Z1Score</td>";
		echo "<td>P-value</td>";
	echo "</tr>";

	foreach ($table as $family=>$row){
		if (isset($showfamily)&&!$motifnamegroup[$family][$showfamily]) continue;
		$i++;
		$name=$row["NAME"];
		$logo=image("$resultLink/$name.logo.png",50);
		$logoR=image("$resultLink/$name.logoR.png",50);
		$disthist=ahrefimage("$resultLink/$name.pos_disthist.jpg","$resultLink/$name.pos_disthist.jpg.tn.jpg",100);
		$distfoldhist=ahrefimage("$resultLink/$name.pos_distfoldhist.jpg","$resultLink/$name.pos_distfoldhist.jpg.tn.jpg",100);
		$score=$row["SCORE"];
		$w=$row["W"];
		$threshold=$row["THRESHOLD"];
		$z0score=$row["Z0SCORE"];
		$z1score=$row["Z1SCORE"];
		$pvalue=sprintf("%.3f",(1-$statobj->CDF($row["SCORE"])));
		echo "<tr align=center>";
		echo "<td><input type=checkbox name='select_$name'> $i</td>";
		echo "<td>$name</td>";
		echo "<td>";
		if ($showmode=="family"){
			echo "<a href='view0.php?family=$family&top=999&show=factor&email=$email&handle=$handle&jobid=$jobid'>$family</a>";
		}
		else{
			$isfirst=1;
			foreach($row["GROUP"] as $family=>$dummy){
				if ($isfirst) $isfirst=0;
				else echo "<br>";
				echo "<a href='view0.php?family=$family&top=999&show=factor&email=$email&handle=$handle&jobid=$jobid'>$family</a>";
			}
		}
		echo "</td>";
		echo "<td>$logo</td>";
		echo "<td>$logoR</td>";
		echo "<td>$score</td>";
		echo "<td>$disthist$distfoldhist</td>";
		echo "<td>$w</td>";
		echo "<td>$threshold</td>";
		echo "<td>$z0score</td>";
		echo "<td>$z1score</td>";
		print "<td>$pvalue</td>";
		echo "</tr>";
		if ($i>=$showtop) break;
	}
	echo "</table>";
}?>
</body></html> 	

<?php

global $rooturl;
global $email;
global $handle;
if (validateemailhandle($email,$handle)){
        mainfunction();
} else {
        header("location:$rooturl"); //redirect to login page
}
?>
