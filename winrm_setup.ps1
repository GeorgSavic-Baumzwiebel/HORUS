winrm quickconfig
Enable-PSRemoting
winrm set winrm/config/service/Auth '@{Basic="true"}'
winrm set winrm/config/client/Auth '@{Basic="true"}'
winrm set winrm/config/client '@{AllowUnencrypted="true"}'
winrm set winrm/config/service '@{AllowUnencrypted="true"}'
winrm set winrm/config/service '@{RootSDDL="O:NSG:BAD:P(A;;GAGXGWGR;;;BA)(A;;GR;;;IU)(A;;GAGXGWGR;;;S-1-5-21-790852054-814587399-2739493028-1002)S:P(AU;FA;GA;;;WD)(AU;SA;GXGW;;;WD)"}'
netsh advfirewall firewall add rule name="WinRM-HTTP" dir=in localport=5985 protocol=TCP action=allow
Set-NetConnectionProfile -InterfaceAlias Ethernet1 -NetworkCategory "Private"
