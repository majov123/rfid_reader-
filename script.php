<?php

$servername = "localhost";
$user = "root";
$password = "";
$dbname = "isic_db";

$conn = new mysqli($servername, $user, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(["error" => "Nepodarilo sa pripojiť k databáze: " . $conn->connect_error]));
}

if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST["isic_id"])) {
    $isic_id = $conn->real_escape_string($_POST["isic_id"]);

    $sql = "SELECT Meno, Priezvisko, Cislo_izby, Bezdrôtové_pripojenie_MAC, Bezdrôtové_pripojenie_ip, Pevné_pripojenie_IP, Pevné_pripojenie_MAC   FROM id   WHERE isic_id = '$isic_id'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();
        echo json_encode([
            "meno" => $row["Meno"],
            "priezvisko" => $row["Priezvisko"],
            "cislo_izby" => $row["Cislo_izby"],
            "bezdr_pripojenie_mac" => $row["Bezdrôtové_pripojenie_MAC"],
            "bezdr_pripojenie_ip" => $row["Bezdrôtové_pripojenie_ip"],
            "pevne_pripojenie_ip" => $row["Pevné_pripojenie_IP"],
            "pevne_pripojenie_mac" => $row["Pevné_pripojenie_MAC"]
        ]);
    } else {
        echo json_encode(["error" => "ISIC karta neexistuje"]);
    }
} 

$conn->close();
?>
