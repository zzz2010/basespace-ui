<?
echo "<title>".basename(dirname($_SERVER["SCRIPT_FILENAME"]))."</title>";
echo "<H1>".basename(dirname($_SERVER["SCRIPT_FILENAME"]))."</H1>";
$files1 = scandir("./");
$prefix=dirname($_SERVER["SCRIPT_FILENAME"])."/";

foreach($files1 as $d)
{
 if(is_dir($prefix.$d)&&strlen($d)>2)
        {
		
		if(strpos($d,"CENTDIST")!== false)
		{
			echo "<hr>";			
			echo "<H3>Motif Enrichment(CENTDIST)</H3>";
			$files2 = scandir("./".$d);
			foreach($files2 as $d2)
			{
				if(is_dir($prefix.$d."/".$d2)&&strlen($d2)>2)
				{
				$rundir2=$prefix.$d."/".$d2;
?>
 <a href=http://plap11/newgenomeviewer/ZZZ/webseqtools2/TASKS/Motif_Enrichment/viewresult.php?rundir=<? echo $rundir2 ; ?>  target=_blank > <? echo $d2; ?></a><br>

<?
				}
			}
			echo "<hr>";
		}
	
	        else if(strpos($d,"denovo")!== false)
                {
			echo "<hr>";
			echo "<H3>DeNovo Motif Result</H3>";
                 $files2 = scandir("./".$d);
                        foreach($files2 as $d2)
                        {
                                if(is_dir($prefix.$d."/".$d2)&&strlen($d2)>2)
                                {
                                $rundir2=$prefix.$d."/".$d2;
?>
 <a href=http://plap11/newgenomeviewer/ZZZ/webseqtools2/TASKS/metaNovo/viewresult.php?rundir=<? echo $rundir2 ; ?> target=_blank > <? echo $d2; ?></a><br>

<?
                                }
                        }
			echo "<hr>";
                }
		
		else 
		{
				?>

<a href=showdir.php?dir=<? echo $d ; ?> target=_blank > <? echo $d; ?></a><br>
<?
		}


}
}

echo "<hr><H2>Pipeline Parameters:</H2>";
$cfgfile=glob("./*.cfg");
$lines=file($cfgfile[0]);
foreach ($lines as $line_num => $line) {
    echo   htmlspecialchars($line) . "<br />\n";
}


?>
