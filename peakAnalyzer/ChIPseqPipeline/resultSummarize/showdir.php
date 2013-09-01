<?

include_once('http://plap11/newgenomeviewer/ZZZ/webseqtools2/common.inc');

function showlinks($htmllist)
{
for ( $counter = 0; $counter <count($htmllist); $counter += 1) {

echo "<a  href='".$htmllist[$counter]."' target=_blank>".basename($htmllist[$counter])."</a><br>";
}

}


function showDirs($indir)
{
$files1 = scandir($indir);
$prefix=dirname($_SERVER["SCRIPT_FILENAME"])."/";
foreach($files1 as $d)
{

 	if(is_dir($indir."/".$d)&&strlen($d)>2)
	{	
		echo "<a  href='showdir.php?dir=".$indir."/".$d."' target=_blank>".$d."</a><br>";

	}
}

}
function imglayout($imglist, $ncol)
{
echo "<table><tr>";
        for ( $counter = 0; $counter <count($imglist); $counter += 1) {

        echo "<td>";
        echo "<a  href='".$imglist[$counter]."' target=_blank><img src='".$imglist[$counter]."' width='".(800/$ncol)."'/><br>".basename($imglist[$counter])."</a>";
        echo "</td>";
        if($counter%$ncol==($ncol-1))
                echo "</tr><tr>";
}

echo "</tr></table>";

}

function readtable2($FileName){
$FileHandle = fopen($FileName,"r");
$FileContent = fread ($FileHandle,filesize ($FileName));
fclose($FileHandle);
// You can replace the \t with whichever delimiting character you are using
$lines = explode("\n", $FileContent);
$headerrow=1;
$header=array();
$data=array();
foreach($lines as $CurrValue)
{
        $cells=explode(" ",$CurrValue);
        if ($headerrow==1){
		$cells=explode("\t",$CurrValue);
                $header=$cells;
                $headerrow=0;
                continue;
        }
        $i=0;
        $x=array();
        if (count($cells)<2) continue;
        foreach($cells as $cell){
                $x[$header[$i]]=$cell;
                $i++;
        }
        array_push($data,$x);
}
return $data;
 
}

$dirpath="./";

if(isset($_GET["dir"]))
$dirpath.=$_GET["dir"];

showDirs($dirpath);
$htmlist=glob($dirpath."/*.htm*");

showlinks($htmlist);

$imglist=glob($dirpath."/*.png");	
imglayout( $imglist,2);

?>
