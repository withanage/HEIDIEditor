<?php
if (!empty($_FILES)) {
    $filename = dirname(__FILE__) . "/files/" . $_FILES['file']['name'];
    $path = pathinfo($filename);
    move_uploaded_file($_FILES['file']['tmp_name'], $filename);
    chmod($filename, 0666);
    system("python ../meTypeset/bin/meTypeset.py " .  $path["extension"] . " " . $filename . " ./files/out_" . $path["filename"]);
    system("python ../cgi/convertXml2Json.py ./files/out_" . $path["filename"] . "/nlm/out.xml ./files/".$path["filename"].".json");
    copy("./files/out_" . $path["filename"] . "/nlm/out.xml", "./files/" . $path["filename"] . ".xml");

}
