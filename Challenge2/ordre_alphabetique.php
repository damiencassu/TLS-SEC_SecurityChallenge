<?php
//$ligne = file($_SERVER['argv'][1]);
//$ligne = file("dico.txt");
//sort($ligne);

$lines = file($_SERVER['argv'][1]);
natsort($lines);
file_put_contents($_SERVER['argv'][1], implode("", $lines));
?>