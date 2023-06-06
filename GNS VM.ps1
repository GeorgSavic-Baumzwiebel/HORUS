param($pathtoGNSVM)
& "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" start $pathtoGNSVM
Get-Content $pathtoGNSVM | Where-Object {$_ -notmatch 'ethernet'} | Set-Content "C:\gns tmp.vmx"
Add-Content -Path "C:\gns tmp.vmx" -Value 'ethernet0.present = "TRUE"
ethernet0.virtualDev = "e1000"
ethernet0.addressType = "generated"
ethernet0.pciSlotNumber = "32"
ethernet0.wakeonpcktrcv = "false"
ethernet0.allowguestconnectioncontrol = "true"
ethernet1.present = "TRUE"
ethernet1.virtualDev = "e1000"
ethernet1.connectionType = "hostonly"
ethernet1.addressType = "generated"
ethernet1.pciSlotNumber = "33"
ethernet1.wakeonpcktrcv = "false"
ethernet1.allowguestconnectioncontrol = "false"'
Get-Content "C:\gns tmp.vmx" | Set-Content $pathtoGNSVM

$tmp = (Get-NetIPAddress -AddressFamily IPV4 -InterfaceAlias Wlan).IPAddress
$tmpIP = $tmp.ToString()
$IP = $tmp.Substring(0, $tmpIP.LastIndexOf(".")+1)
$last = [int]($tmp.Substring($tmpIP.LastIndexOf(".")+1))+60
$last = $last.ToString()
$GNSIP = "$($IP)$($last)"
$GNSGW = (Get-NetIPConfiguration | Where-Object { $_.InterfaceAlias -eq 'WLAN' }).IPv4DefaultGateway.NextHop

Set-Content -Path C:\90_gns3vm_static_netcfg.yaml -Value "network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      addresses:
        - ${GNSIP}/24
      gateway4: ${GNSGW}
      nameservers:
           addresses: [8.8.8.8, 8.8.8.4]"



& "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" -T ws -gu gns3 -gp gns3 CopyFileFromHostToGuest $pathtoGNSVM "C:\90_gns3vm_static_netcfg.yaml" "/etc/netplan/90_gns3vm_static_netcfg.yaml"
& "C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe" -T ws -gu gns3 -gp gns3 runScriptInGuest $pathtoGNSVM /bin/bash "sudo rm /etc/netplan/90_gns3vm_static_netcfg.yaml"
#Netzadapter auf labor pcs heißt Ethernet