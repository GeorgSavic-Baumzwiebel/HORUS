# Nicht vergessen Wake On LAN am Netzwerkadapter un BIOS zu aktivieren
# Absoluter Pfad zur Datei mit den MAC-Adressen im Format AA:BB:CC:DD:EE:FF oder AA-BB-CC-DD-EE-FF
[Parameter(Mandatory,ValueFromPipeline,ValueFromPipelineByPropertyName)]
param(
[string]
$FilePath
)

# Erstellt einen UDP Broadcast Client
$UDPclient = [System.Net.Sockets.UdpClient]::new()
$UDPclient.Connect(([System.Net.IPAddress]::Broadcast),4000)
# Geht durch alle Zeilen im File
foreach($mac in Get-Content $FilePath) {
    #Erstellt ein 102 byte array wo alle Werte mit FF gefüllt sind
    $packet = [byte[]](,0xFF * 102)
    # Konvertiert die Mac-Adresse in ein Byte Array
    $mac = $mac -split '[:-]' | ForEach-Object {
        [System.Convert]::ToByte($_, 16)
    }
    6..101 | Foreach-Object {
        $packet[$_] = $mac[($_ % 6)]
    }
    # Schickt packet
    $null = $UDPclient.Send($packet, $packet.Length)
    #Gibt Packet aus, DEBUG
    $Packet =  $packet -join ''
    echo $packet
    echo ""
}
# Schließt den UDP Client
$UDPclient.Close()
$UDPclient.Dispose()