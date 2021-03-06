<header><title>Submit Motif Enrichment Job</title></header>
<?php
include_once('../../common.inc');?>
<?php
$taskdir=getcwd();?>
<script type="text/javascript">
function loadXMLDoc(file,callback)
{
	if( file.indexOf('Custom')>0)
	{
		document.getElementById('jobtitle').value='';
		document.getElementById('peakfile').value='';
		return;
		
	}
	document.getElementById('jobtitle').value ='Run '+document.getElementById('samplesList').value+' sample';
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
callback(xmlhttp.responseText);
//    document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
    }
  }
xmlhttp.open("GET",file,true);
xmlhttp.send();
}
function loadtext(file,callback)
{
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
xmlhttp.onreadystatechange=function()
  {
  if (xmlhttp.readyState==4 && xmlhttp.status==200)
    {
callback(xmlhttp.responseText);
//    document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
    }
  }
xmlhttp.open("GET",file,true);
xmlhttp.send();
}
function callback(text){
	if(document.getElementById('samplesList').value.match('lncap'))
		 document.getElementById('genome').value='hg18'
	if(document.getElementById('samplesList').value.match('loci'))
	                 document.getElementById('genome').value='mm8'

	document.getElementById('peakfile').value =text;
	document.getElementById('motifstartwith').value='V';
	document.getElementById('cbmotifstartwith').checked=true;
	update_motiffilter();
  	 addalltomotifselect();
	 
}

</script>
<?php
function submit(){
	//create a timestamp directory
	global $email;
	global $handle;
	global $rootdir;
	global $rooturl;
	global $taskdir;
	$jobserverdir="$rootdir/JOBSERVER";
	$jobdir=tempdir("$rootdir/userdata/$handle");
	
	$jobid=basename($jobdir);
	$jobtype=basename($taskdir);

	chmod ($jobdir,0777);
	$inputfilesdir=("$jobdir/input");
	mkdir($inputfilesdir);
	chmod ($inputfilesdir,0777);
	$outputfilesdir=($jobdir."/output");
	mkdir($outputfilesdir);
	chmod ($outputfilesdir,0777);
	echo "<br>";
	createinputfiles($inputfilesdir,array());
	global $configfile;
	chdir($jobdir);
	execprint("echo '$jobtype' > input/jobtype");
	echo "<br>jobdir = $jobdir<br>";
	$retval=makeconfig("input","config.txt");
	if ($retval) die("makeconfig failed");
	$jobfile=execprint("python $rootdir/JOBSERVER/submitjob.py 'python $taskdir/run.py -configfile config.txt' 2>&1",$output,$retval);
	execprint("echo '$jobfile' > input/jobfile");
	return $retval==0;
}?>

<?php
function mainfunction(){
	//print_r($_REQUEST);
	if ($_REQUEST["command"]=="Submit Job"){
		submit();
		global $email;
		global $handle;
		global $rooturl;
		redirect("$rooturl/TASKS/viewjobs.php?email=$email&handle=$handle");
	} else{
		form();
	}
}?>
<?php
function form(){?>
	<?php

	global $genomedir;
	global $email;
	global $handle;
	global $rootdir;
	global $rooturl;
	if (isset($_REQUEST["admin"])){
		$admin=1;
	}
	else{$admin=0;}
	?>
	<fieldset style="width:800">
	<?php
 echo image("$rooturl/logo.png",200,400)?>
	<?php
 echo image("logo.png",200,400)?>
	<div style="text-align:left">
	<a href=<?php
 echo "$rooturl/";?> target="_blank">Login</a><br>
	<a href=<?php
 echo "$rooturl/TASKS/viewjobs.php?email=guest";?> target="_blank">View Jobs</a><br>
	<a href=<?php
 echo "$rooturl/../centdist/help.htm";?> target="_blank">Help on CENTDIST</a><br>
	<a href=<?php
 echo "$rooturl/TASKS/Motif_Enrichment/view.php?jobid=TEV0sE.example&email=SHARED&handle=SHARED";?> target="_blank">Sample Output(AR_LNCAP)</a> <br>
	</div>
	<form target=_blank method=POST onsubmit="return checkform()">
		<br>
		Title: <input name=title id=jobtitle style="width:90%"><br>
		<div style="text-align:center">
		<fieldset>
		<legend>Upload peak coordinates</legend>
		<button type=button onclick="document.getElementById('samplesList').value='lncap_AR';loadXMLDoc('<?php
 echo '../../EXAMPLE/' ?>'+'lncap_AR.peak',callback)">Load sample ChIP-seq peaks:</button>
		<select name=samplesList id=samplesList onchange="loadXMLDoc('<?php
 echo '../../EXAMPLE/' ?>'+this.value+'.peak',callback)">
		<option selected> Custom</option>
		<?php

			$samples=glob("$rootdir/EXAMPLE/*.peak");
			foreach ($samples as $sample){
				$sample=explode("/",$sample);
				echo "<option>".str_replace('.peak','',$sample[count($sample)-1])."</option>";
			}
		?>
		</select>
		<br>
		<textarea name=peakfile id=peakfile rows=20 style="width:95%"></textarea><br>
		Genome Build
		<select name=genome id=genome>
		<?php

			$genomes=glob("$genomedir/*/.");
			foreach ($genomes as $genome){
				$genome=explode("/",$genome);
				if($genome[count($genome)-2]=='mm8')
				echo "<option selected>".$genome[count($genome)-2]."</option>";
				else
				echo "<option>".$genome[count($genome)-2]."</option>";
			}
		?>
		
		</select><br>
		</fieldset>
		<fieldset>
		<legend>Motif</legend>
		<fieldset>
		<legend>Select</legend>
		Filter group <select onchange="update_motiffilter();" id="motiffilter"></select><input onchange="update_motiffilter()" type=checkbox id=cbmotifstartwith>Show only motif whose first characters are <input onchange="update_motiffilter()" id=motifstartwith value="PV"><br>
		<table width=100%>
		<td width=40%>
		<select id=motifgrouplist multiple=multiple size=10 style="width:100%;"></select>
		</td>
		<td width=20%>
		<button type=button onclick="addalltomotifselect()" style="width:100%;display:block;"><html>Add All</html></button>
		<button type=button onclick="addtomotifselect()" style="width:100%;display:block;"><html>Add selected</html></button>
		<button type=button onclick="clearmotifselect()" style="width:100%;display:block;"><html>Clear</button>
		</td>
		<td width=40%>
		<textarea id=motifselect name=motifselect rows=10 style="width:100%"></textarea>
		</td>
		</table>
		</fieldset>
		<input type=checkbox id=cbcustommotif onclick="checkcustommotif()">Use custom motif database<br>
		<div id=custommotif style="visibility:hidden;height:1;overflow:hidden">
			<a href=<?php
 echo "$rooturl/TOOLS/genmotif.php";?> target="_blank">Generate motif from matrix</a>
			<table width=100%>
			<tr><td width=55%>
			<fieldset style="text-align:center">
			<legend>Motif Database</legend>
			<textarea id=motifdatabase name=motifdatabase rows=20 style="width:95%" wrap=off></textarea><br>
			</fieldset>
			</td>
			<td width=35%>
			<fieldset style="text-align:center">
			<legend>Motif Group File</legend>
			<textarea id=motifgroup name=motifgroup rows=20 style="width:95%"></textarea>
			</fieldset>
			</td>
			<td width=10%>
			<button type=button onclick="restore_motifdatabase()" style="width:120px;display:block;"><html>Restore Default <br> Motif Database</html></button>
			<button type=button onclick="restore_motifgroup()" style="width:120px;display:block;"><html>Restore Default <br> Motif Group</html></button>
			<button type=button onclick="update_motifselectlist()" style="width:120px;display:block;"><html>Update Motif<br>Select List</html></button>
			</td>
			</tr>
			</table>
			</div>
			<fieldset style="<?php
if (!$admin){echo 'visibility:hidden;height:1;overflow:hidden';}?>">
			<legend>Settings</legend>
			Max comotif distance<input name=Max_Comotif_Dist value=1000><br>
			Scanning false positive<input name=FP value=0.0001><br>
			</fieldset>
			<input type=submit name=command value="Submit Job">
		</div>
		<input type=hidden name=email value="<?php
echo $email;?>">
		<input type=hidden name=handle value="<?php
echo $handle;?>">
	</form>
	</fieldset>
	<textarea readonly=true id="default_motifdatabase" style="width:1;height:1"><?php
 echo readfile1("$rootdir/DEFAULT/transfac.motifs");?></textarea>
	<textarea readonly=true id="default_motifgroup" style="width:1;height:1"><?php
 echo readfile1("$rootdir/DEFAULT/transfac.group");?></textarea>
	<script>
	function restore_motifdatabase(){
		document.getElementById('motifdatabase').value=document.getElementById('default_motifdatabase').value;
	}
	function restore_motifgroup(){
		document.getElementById('motifgroup').value=document.getElementById('default_motifgroup').value;
	}
	function trim(str, chars) {
		return ltrim(rtrim(str, chars), chars);
	}
	 
	function ltrim(str, chars) {
		chars = chars || "\\s";
		return str.replace(new RegExp("^[" + chars + "]+", "g"), "");
	}
	 
	function rtrim(str, chars) {
		chars = chars || "\\s";
		return str.replace(new RegExp("[" + chars + "]+$", "g"), "");
	}
	function stringtomatrix(s){
		s=trim(s).split('\n');
		var i,ss;
		for (i=0;i<s.length;i++){
			ss=s[i].split('\t');
			for (j=0;j<ss.length;j++){
				ss[j]=trim(ss[j]);
			}
			s[i]=ss
		}
		return s;
	}
	function clone(s){
		var i,s2;
		s2=new Array();
		for (i=0;i<s.length;i++){
			s2[i]=s[i];
		}
		return s2;
	}
	function sorted(s){
		var s2;
		s2=clone(s);
		s2.sort();
		return s2;
	}
	function sortunique(s){
		var i,s2,s3;
		s2=sorted(s);
		s3=new Array();
		for (i=0;i<s2.length;i++){
			if (i==0 || s2[i]!=s2[i-1]){
				s3[s3.length]=s2[i];
			}
		}
		return s3;
	}
	function map(f,s){
		var i,s2=new Array();
		for (i=0;i<s.length;i++){
			s2[i]=f(s[i]);	
		}
		return s2;
	}
	function filter(f,s){
		var s2=new Array();
		for (i=0;i<s.length;i++){
			if (f(s[i])) s2[s2.length]=s[i];
		}
		return s2;
	}
	function update_motifselectlist(){
		var i,j;
		motifgroup=document.getElementById('motifgroup').value;
		motifgroup=sortunique(map(function(x){return x[1]},stringtomatrix(motifgroup)));
                var i;
                var myselect=document.getElementById("motiffilter")
                myselect.scrollTop=0;
                clearoptions(myselect.options);
		myselect.options[myselect.options.length]=new Option('(ALL)','(ALL)');
		for (i=0;i<motifgroup.length;i++){
			myselect.options[myselect.options.length]=new Option(motifgroup[i],motifgroup[i]);
		}
		update_motiffilter();
		verifymotifselect();
	}
	function Set(x){
		var i;
		var obj=new Object();
		for (i=0;i<x.length;i++){
			obj[x[i]]=1;
		}
		return obj;
	}
	function update_motiffilter(){
		allmotifs=map(function(x){return trim(x.split('\t')[1])},filter(function(x){return x.split('\t')[0]=='DE'},document.getElementById('motifdatabase').value.split('\n')));
		var cbmotifstartwith=document.getElementById('cbmotifstartwith').checked;
		var motifstartwith=Set(document.getElementById('motifstartwith').value.split(''));
		motifset=Set(allmotifs);
		var motifgroup=document.getElementById('motifgroup').value;
		var motifgroup=stringtomatrix(motifgroup);
		var motiffiltervalue=document.getElementById("motiffilter").value;
		var i;
		var x;
		if (motiffiltervalue=='(ALL)'){
			x=filter(function(x){return (!cbmotifstartwith||motifstartwith[x.charAt(0)])},allmotifs);
		}
		else {
			x=map(function(x){return x[0]},filter(function(x){return motifset[x[0]] && x[1]==motiffiltervalue && (!cbmotifstartwith||motifstartwith[x[0].charAt(0)])},motifgroup));
		}
                var myselect=document.getElementById("motifgrouplist")
                myselect.scrollTop=0;
		clearoptions(myselect);
		x.sort();
		for (i=0;i<x.length;i++){
			myselect.options[myselect.options.length++]=new Option(x[i],x[i]);
		}
	}
	function clearmotifselect(){
                document.getElementById("motifselect").value="";
	}
	function verifymotifselect(){
                var motifselect=document.getElementById("motifselect")
		motifselectlist=filter(function(x){return motifset[x]},map(trim,motifselect.value.split('\n')));
		motifselect.value=motifselectlist.join('\n');
		motifselectset=Set(motifselectlist);
	}
	function joinarray(x,y){
		var z=clone(x);
		var i;
		for (i=0;i<y.length;i++){
			z[z.length]=y[i];
		}
		return z;
	}
	function addtomotifselect(){
		verifymotifselect();
                var myselect=document.getElementById("motifgrouplist")
		var y=getSelected(myselect)
		y=filter(function(x){return motifset[x]&!motifselectset[x]},y)
                var motifselect=document.getElementById("motifselect")
		motifselect.value=joinarray(motifselectlist,y).join('\n')
	}
	function addalltomotifselect(){
		verifymotifselect();
                var myselect=document.getElementById("motifgrouplist")
		var y=getAllOption(myselect)
		y=filter(function(x){return motifset[x]&!motifselectset[x]},y)
                var motifselect=document.getElementById("motifselect")
		motifselect.value=joinarray(motifselectlist,y).join('\n')
	}
        function getSelected(opt) {
                var selected = new Array();
                var index = 0;
                var s="";
                var i=0;
                for (var intLoop=0; intLoop < opt.length; intLoop++) {
                        if (opt[intLoop].selected) selected[i++]=opt[intLoop].value;
                }
                return selected;
        }
	function getAllOption(opt){
                var selected = new Array();
                var index = 0;
                var s="";
                var i=0;
                for (var intLoop=0; intLoop < opt.length; intLoop++) {
                        selected[i++]=opt[intLoop].value;
                }
		return selected;
	}
	function clearoptions(opt){
		while (opt.length>0){
			opt[opt.length-1]=null;
		}
	}
	function checkform(){
		verifymotifselect();
                if (document.getElementById("motifselect").value==""){
			alert("Please add at least one motif");
			return false;
		}
	}
	function checkcustommotif(){
		var cbcustommotif=document.getElementById("cbcustommotif").checked;
		var custommotif=document.getElementById("custommotif");
		if (cbcustommotif){
			custommotif.style['visibility']='visible'
			custommotif.style['overflow']='visible'
			custommotif.style['height']=null
		} else {
			custommotif.style['visibility']='hidden'
			custommotif.style['overflow']='hidden'
			custommotif.style['height']=1
		}
	}
	</script>

	<input type=hidden id=DUMMY value=0 onload="alert(1)"></div>
	<script>
	window.onload=function(){
	if (document.getElementById("DUMMY").value==0){
	document.getElementById("DUMMY").value=1;
	restore_motifdatabase();
	restore_motifgroup();
	update_motifselectlist();
	} else {
		update_motifselectlist();
	}
	<?php
if (isset($_REQUEST["jobid"])){?>
	dir='<?php
echo "$rooturl/userdata/$handle/".$_REQUEST["jobid"]."/input";?>'
        step0=function(){loadtext(dir+"/title",function(text){document.getElementById('jobtitle').value=text;step1()})}
        step1=function(){loadtext(dir+"/genome",function(text){document.getElementById('genome').value=text;step2()})}
        step2=function(){loadtext(dir+"/peakfile",function(text){document.getElementById('peakfile').value=text;step3()})}
        step3=function(){loadtext(dir+"/motifselect",function(text){document.getElementById('motifselect').value=text;step4()})}
        step4=function(){loadtext(dir+"/motifdatabase",function(text){document.getElementById('motifdatabase').value=text;step5()})}
        step5=function(){loadtext(dir+"/motifgroup",function(text){document.getElementById('motifgroup').value=text;})}
	step0();
	<?php
}?>
	}
	</script>
<?php
}?>
<?php

global $rooturl;
global $email;
global $handle;
if (validateemailhandle($email,$handle)){
        mainfunction();
} else {
	$email="guest";
	$handle="guest";
	mainfunction();
//	redirect($rooturl);
}
?>

