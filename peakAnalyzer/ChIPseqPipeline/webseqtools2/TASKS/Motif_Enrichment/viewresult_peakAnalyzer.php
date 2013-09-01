<?include_once('../../common.inc')?>

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

<?function mainfunction(){
	global $email;
	global $handle;
	global $rootdir;
	global $rooturl;
	$userdir="userdata/$handle";
	$jobid=$_REQUEST['jobid'];
	$jobdir="$rootdir/userdata/$handle/$jobid";
         $rootdir="/home/chipseq/public_html/";
         $rooturl="http://genome.ddns.comp.nus.edu.sg";
        $rundir=$_REQUEST['rundir'];
        $resultLink="$rooturl/$rundir";
	//$resultLink=str_replace("//home/chipseq/basespace",$rooturl,$rundir);
	$runDir=$rootdir.$rundir;
	if(substr($rundir,0,5)==="/home")
	{
		$runDir=$rundir;
		$comps=explode("/",$rundir);
		$rooturl=str_replace("chipseq",$comps[2],$rooturl);
		$resultLink="$rooturl/".implode("/",array_slice($comps, 4));
	}
	$table=readtable("$runDir/results.txt");
	$mgroupfile="./motifgroup";
	if(file_exists("$runDir/motifgroup"))
		$mgroupfile="$runDir/motifgroup";
	$temp=explode("\n",readfile1($mgroupfile));
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
		$score=$row["SCORE"];
		if (isset($motifnamegroup[$name])){
			$row["GROUP"]=$motifnamegroup[$name];
			foreach ($row["GROUP"] as $motifgroup=>$dummy){
				if (!isset($motifgroupbest[$motifgroup]) || $motifgroupbest[$motifgroup]["SCORE"]<$score){
					$motifgroupbest[$motifgroup]=$row;
				}
			}
		} else {
			$row["GROUP"]=array();
		}
		$table2[$name]=$row;
	}
	array_multisort(getcol($motifgroupbest,"SCORE"),SORT_DESC,$motifgroupbest);
	array_multisort(getcol($table2,"SCORE"),SORT_DESC,$table2);

/*******compute P-value**********/
	require_once "../../../PDL/NormalDistribution.php";
	$hashset=array();
	$scorelist=array();
	$rowcnt=0;
	$skip=0.2*count($table2);
	echo count($table2)." TFs";
	foreach($table2 as $row)
	{
		if($skip<$rowcnt&&$row["SCORE"]>-100&&$row["SCORE"]<1000)//count($hashset)
			array_push($scorelist,$row["SCORE"]);
		$rowcnt++;
	}
	$sdvalue=sd($scorelist);
	$mean=array_sum($scorelist) / count($scorelist);
	//if(count($table2)>10)
	//	$statobj=new NormalDistribution($mean,$sdvalue);
	//else
		$statobj=false;
	echo "\nTEST";
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
	#if ($_REQUEST["top"]<999999&&$_REQUEST["top"]>0){}
	if (isset($_REQUEST["top"])){
		$showtop=$_REQUEST["top"];
	} else {
		$showtop=10;
	}
	#if isset($_REQUEST["family"]){
	$showfamily=$_REQUEST["family"];
	#}
	if ($_REQUEST["submit"]=="Download As Text"){
	$downloadastext=1;
	}

if (!$downloadastext){
	$i=0;
	echo "<form>";
	if ($showmode=="family"){
	$familyselected="selected";
	} else {
	$factorselected="selected";
	}
	if (isset($_REQUEST["top"])){
		echo "Show top <input name=top value=$showtop size=1> <select name=show><option value=family $familyselected>Families</option><option value=factor $factorselected>Factors</option></select>";
	}else{
		echo "Show top <input name=top value=50 size=1> <select name=show><option value=family>Families</option><option value=factor>Factors</option></select>";
	}
	//echo "<input type=checkbox> using custom motif family";
	echo "<input type=submit name=submit value=Go>";
	echo "<input type=submit name=submit value='Download As Text'>";
	echo "<input type=hidden name=rundir value=$rundir>";
	echo "</form>";
	echo '<table ALIGN="CENTER" border="1px" cellpadding="0px" cellspacing="0px" width=95%>';
	echo "<tr align=center>";
		echo "<td>RANK</td>";
		//echo "<td style='white-space:nowrap'>".ahref("","Clear All")."<br>".ahref("","Check Top")." <input value=50 size=1></td>";
		echo "<td>Name</td>";
		echo "<td>Family</td>";
		echo "<td>Logo</td>";
		echo "<td>LogoR</td>";
		echo "<td>Score</td>";
		echo "<td>Distribution</td>";
		echo "<td>%Sequence having<br>motif above<br>optimal cutoff<br>within optimal<br>binding range</td>";
		echo "<td>%Sequence having<br>motif above<br>1e-4 cutoff<br>within 200bp</td>";
		echo "<td>Binding Range</td>";
		echo "<td>Threshold</td>";
		echo "<td>Z0Score</td>";
		echo "<td>Z1Score</td>";
		echo "<td>P-value</td>";
	echo "</tr>";
	$topmotifFP=fopen("$runDirtopmotif",'w');	
	foreach ($table as $family=>$row){
		if (isset($showfamily)&&!$motifnamegroup[$family][$showfamily]) continue;
		$i++;
		$name=$row["NAME"];
		
		$logo=image("$resultLink/$name.logo.png",50);
		$logoR=image("$resultLink/$name.logoR.png",50);
		$disthist=ahrefimage("$resultLink/$name.pos_disthist.jpg","$resultLink/$name.pos_disthist.jpg",100);
		$distfoldhist=ahrefimage("$resultLink/$name.pos_distfoldhist.jpg","$resultLink/$name.pos_distfoldhist.jpg",100);
		#$disthistnew=ahrefimage("$resultLink/$name.pos.disthist.new.jpg","$resultLink/$name.pos.disthist.new.jpg",100);
		$movingaverage=ahrefimage("$resultLink/$name.pos.movingaverage.jpg","$resultLink/$name.pos.movingaverage.jpg",100);
		$movingaverage2=ahrefimage("$resultLink/$name.pos.movingaverage2.jpg","$resultLink/$name.pos.movingaverage2.jpg",100);
		$count1=readfile1("$runDir$name.count1");
		$count2=readfile1("$runDir$name.count2");
		$score=$row["SCORE"];
		$w=$row["W"];
		$threshold=$row["THRESHOLD"];
		$z0score=$row["Z0SCORE"];
		$z1score=$row["Z1SCORE"];
		if($statobj!=false)
		$pvalue=sprintf("%.3f",(1-$statobj->CDF($row["SCORE"])));
		
		if($i<150 &&  $score > 8 )
		fwrite($topmotifFP, $name."\n");
		
		
		echo "<tr align=center>";
		echo "<td>$i</td>";
		//echo "<td><input type=checkbox name='select_$name'> $i</td>";
		echo "<td>$name</td>";
		echo "<td>";
		if ($showmode=="family"){
			echo "<a href='viewresult_peakAnalyzer.php?family=$family&top=999&show=factor&rundir=$rundir'>$family</a>";
		}
		else{
			$isfirst=1;
			foreach($row["GROUP"] as $family=>$dummy){
				if ($isfirst) $isfirst=0;
				else echo "<br>";
				echo "<a href='viewresult_peakAnalyzer.php?family=$family&top=999&show=factor&rundir=$rundir'>$family</a>";
			}
		}
		echo "</td>";
		echo "<td>$logo</td>";
		echo "<td>$logoR</td>";
		echo "<td>$score</td>";
		echo "<td>$disthist$distfoldhist</td>";
		echo "<td>$movingaverage<br>$count1</td>";
		echo "<td>$movingaverage2<br>$count2</td>";
		echo "<td>$w</td>";
		echo "<td>$threshold</td>";
		echo "<td>$z0score</td>";
		echo "<td>$z1score</td>";
		print "<td>$pvalue</td>";
		echo "</tr>";
		if ($i>=$showtop) break;
	}
	echo "</table>";
	fclose($topmotifFP);
	chmod("$runDirtopmotif",644);
}
else{

        $mime_type="application/force-download";

        @ob_end_clean(); //turn off output buffering to decrease cpu usage

        // required for IE, otherwise Content-Disposition may be ignored
        if(ini_get('zlib.output_compression'))
        ini_set('zlib.output_compression', 'Off');

        header('Content-Type: ' . $mime_type);
        header('Content-Disposition: attachment; filename="result.txt"');
        header("Content-Transfer-Encoding: binary");
        header('Accept-Ranges: bytes');

        /* The three lines below basically make the
        download non-cacheable */
        header("Cache-control: private");
        header('Pragma: private');
        header("Expires: Mon, 26 Jul 1997 05:00:00 GMT");




	$i=0;
	if ($showmode=="family"){
	$familyselected="selected";
	} else {
	$factorselected="selected";
	}
	echo "RANK\t";
	//echo "<td style='white-space:nowrap'>".ahref("","Clear All")."<br>".ahref("","Check Top")." <input value=50 size=1>";
	echo "Name\t";
	echo "Family\t";
	echo "Score\t";
	echo "Binding Range\t";
	echo "Threshold\t";
	echo "Count1\t";
	echo "Count2\t";
	echo "Z0Score\t";
	echo "Z1Score\t";
	echo "P-value";
	echo "\n";
	foreach ($table as $family=>$row){
		if (isset($showfamily)&&!$motifnamegroup[$family][$showfamily]) continue;
		$i++;
		$name=$row["NAME"];
		$logo=image("$resultLink/$name.logo.png",50);
		$logoR=image("$resultLink/$name.logoR.png",50);
		$disthist=ahrefimage("$resultLink/$name.pos_disthist.jpg","$resultLink/$name.pos_disthist.jpg",100);
		$distfoldhist=ahrefimage("$resultLink/$name.pos_distfoldhist.jpg","$resultLink/$name.pos_distfoldhist.jpg",100);
		$disthistnew=ahrefimage("$resultLink/$name.pos.disthist.new.jpg","$resultLink/$name.pos.disthist.new.jpg",100);
		$movingaverage=ahrefimage("$resultLink/$name.pos.movingaverage.jpg","$resultLink/$name.pos.movingaverage.jpg",100);
		$movingaverage2=ahrefimage("$resultLink/$name.pos.movingaverage2.jpg","$resultLink/$name.pos.movingaverage2.jpg",100);
		$count1=trim(readfile1("$runDir$name.count1"));
		$count2=trim(readfile1("$runDir$name.count2"));
		$score=$row["SCORE"];
		$w=$row["W"];
		$threshold=$row["THRESHOLD"];
		$z0score=$row["Z0SCORE"];
		$z1score=$row["Z1SCORE"];
		$pvalue=sprintf("%.3f",(1-$statobj->CDF($row["SCORE"])));
		echo "$i\t";
		//echo "<td><input type=checkbox name='select_$name'> $i</td>";
		echo "$name\t";
		if ($showmode=="family"){
			echo "$family";
		}
		else{
			$isfirst=1;
			foreach($row["GROUP"] as $family=>$dummy){
				echo "$family";
				break;
			}
		}
		echo "\t";
		echo "$score\t";
		echo "$w\t";
		echo "$threshold\t";
		echo "$count1\t";
		echo "$count2\t";
		echo "$z0score\t";
		echo "$z1score\t";
		print "$pvalue";
		echo "\n";
		if ($i>=$showtop) break;
	}
}
}
?>
</body></html> 	

<?
global $rooturl;
global $email;
global $handle;
        mainfunction();
?>
