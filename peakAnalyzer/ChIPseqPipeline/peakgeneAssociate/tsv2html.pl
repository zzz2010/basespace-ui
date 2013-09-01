print <<END;
<table border="1" cellspacing="0" cellpadding="4">
<thead>
<tr><th>
END
s?\t?</th><th>?g;
print "$_</th></tr>\n";
print "</tr>\n</thead>\n<tbody>\n";
while (<>) {
    print "<tr>\n";
    my @fields = split('\t');
    for $cell(@fields) {
	if($cell =~ /^(\d|\s)+$/) {
	    print "<td align=\"right\">$cell</td>"; }
	else {
	    print "<td>$cell</td>"; } }
    print "</tr>\n"; }
print "</tr>\n</tbody>\n</table>\n";
