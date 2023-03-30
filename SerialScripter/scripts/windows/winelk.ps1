param(
    [Parameter(Mandatory=$true)]
    [string]$ELKIPAddress
)

# Download the Winlogbeat installation package
# Invoke-WebRequest -Uri "https://artifacts.elastic.co/downloads/beats/winlogbeat/winlogbeat-7.14.1-windows-x86_64.zip" -OutFile "$env:TEMP\winlogbeat.zip"
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true} ;
$url = "https://artifacts.elastic.co/downloads/beats/winlogbeat/winlogbeat-7.14.1-windows-x86_64.zip"

$file = "$env:TEMP\winlogbeat.zip"

$webclient = New-Object System.Net.WebClient
$webclient.DownloadFile($url, $file)
# Extract the Winlogbeat installation package
Expand-Archive -Path "$env:TEMP\winlogbeat.zip" -DestinationPath "$env:ProgramFiles\Winlogbeat" -Force

# Configure Winlogbeat
$winlogbeatConfigPath = "$env:ProgramFiles\Winlogbeat\winlogbeat-7.14.1-windows-x86_64\winlogbeat.yml"
$winlogbeatConfig = Get-Content $winlogbeatConfigPath
$winlogbeatConfig = $winlogbeatConfig.replace("#output.elasticsearch:", "output.elasticsearch:")
#$winlogbeatConfig = $winlogbeatConfig -replace "#hosts: \[\"localhost:9200\"\]","hosts: [\"$($ELKIPAddress):9200\"]"
#$winlogbeatConfig = $winlogbeatConfig -replace 'hosts: \["localhost:9200"\]', ('hosts: ["{0}:9200"]' -f $ELKIPAddress)
#$winlogbeatConfig = $winlogbeatConfig -replace 'hosts: \["localhost:9200"\]', "hosts: [""$ELKIPAddress:9200""]"


# If you're not receiving any log data after running this script, it's likely the winlogbeat.yml file didn't update properly. Fix:
	# $env:ProgramFiles\Winlogbeat\winlogbeat-7.14.1-windows-x86_64\winlogbeat.yml - open up in notepad
	# CTRL + F to find output.elasticsearch
	# Replace the localhost:9200 with the IP address of the ELK server:9200
	# Restart winlogbeat service


$winlogbeatConfig = $winlogbeatConfig -replace 'hosts: \["localhost:9200"\]', ('hosts: ["' + $ELKIPAddress + ':9200"]')
Set-Content $winlogbeatConfigPath $winlogbeatConfig

# Install Winlogbeat as a service
& "$env:ProgramFiles\Winlogbeat\winlogbeat-7.14.1-windows-x86_64\install-service-winlogbeat.ps1"

# Start the Winlogbeat service
Start-Service winlogbeat
