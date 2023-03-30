Function Install-PowerCLI {
    [CmdletBinding()]
    Param (
        [Parameter(Mandatory=$false)]
        [string]$InstallerUrl = "https://download3.vmware.com/software/vmw-tools/powerclicore/PowerCLI_Core.zip"
    )
    $installerPath = "$env:USERPROFILE\Downloads\PowerCLI_Core.zip"

    try {
        # Download the PowerCLI installer
        Write-Verbose "Downloading PowerCLI from $InstallerUrl to $installerPath"
        Invoke-WebRequest -Uri $InstallerUrl -OutFile $installerPath

        # Unzip the PowerCLI installer to a temporary location
        Write-Verbose "Extracting PowerCLI to a temporary location"
        Expand-Archive -Path $installerPath -DestinationPath "$env:USERPROFILE\Downloads\PowerCLI"

        # Install the PowerCLI module
        Write-Verbose "Installing PowerCLI"
        Install-Module -Name VMware.PowerCLI -Scope AllUsers -Force

        Write-Output "PowerCLI installed successfully"
    }
    catch {
        Write-Error "Error installing PowerCLI: $($_.Exception.Message)"
    }
    finally {
        # Clean up temporary files
        Remove-Item -Path $installerPath -ErrorAction SilentlyContinue
        Remove-Item -Recurse -Path "$env:USERPROFILE\Downloads\PowerCLI" -ErrorAction SilentlyContinue
    }
}

function Get-VSphereInventory {
    try {
        # Get the vCenter server object
        $vCenterServer = Get-View -Id 'ServiceInstance'

        # Get data on all ESXi hosts in the vSphere server
        $esxiHosts = Get-VMHost | Select-Object Name, ConnectionState, PowerState, Version, Manufacturer, Model, NumCpu, MemoryMB, NumNics, NumHBAs

        # Get data on all virtual machines in the vSphere server
        $virtualMachines = Get-View -ViewType VirtualMachine -Property Name, Guest, Config.Hardware.NumCPU, Config.Hardware.MemoryMB, Config.Version, Runtime.Host | ForEach-Object {
            [PSCustomObject]@{
                Name = $_.Name
                Guest = $_.Guest.GuestId
                NumCpu = $_.Config.Hardware.NumCPU
                MemoryMB = $_.Config.Hardware.MemoryMB
                Version = $_.Config.Version
                ESXiHost = $_.Runtime.Host.Name
            }
        }

        # Get data on all datastores in the vSphere server
        $datastores = Get-Datastore | Select-Object Name, FreeSpaceMB, CapacityMB, @{Name='Type';Expression={($_.Type).ToString()}}, @{Name='ESXiHost';Expression={($_.VMHost).Name}}

        # Get data on all networks in the vSphere server
        $networks = Get-VirtualSwitch | Select-Object Name, NumPorts, @{Name='ESXiHost';Expression={($_.VMHost).Name}}

        # Create a hashtable to store all the inventory data
        $inventoryData = @{
            'vCenterServer' = $vCenterServer.Name
            'ESXiHosts'     = $esxiHosts
            'VirtualMachines' = $virtualMachines
            'Datastores'    = $datastores
            'Networks'      = $networks
        }

        # Output the inventory data as JSON
        ConvertTo-Json $inventoryData
    }
    catch {
        Write-Error "Error getting vSphere inventory: $($_.Exception.Message)"
    }
}

function New-FolderSnapshot {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)]
        [string]$FolderName,
        
        [Parameter(Mandatory=$true)]
        [string]$SnapshotName,
        
        [Parameter(Mandatory=$true)]
        [string]$SnapshotDescription
    )
    
    try {
        
        # Get the folder object
        $folder = Get-Folder -Name $FolderName
        
        # Get all virtual machines in the folder
        $vms = Get-VM -Location $folder
        
        # Create the snapshot for each virtual machine
        foreach ($vm in $vms) {
            Write-Host "Creating snapshot for VM '$($vm.Name)'"
            New-Snapshot -VM $vm -Name $SnapshotName -Description $SnapshotDescription -Memory
        }
        
        Write-Host "Snapshot creation complete"
    }
    catch {
        Write-Error "Error creating snapshot: $($_.Exception.Message)"
    }
    
}

function New-VMSnapshotAll {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
        $vCenter,

        [Parameter(Mandatory=$true)]
        [string]$FolderName,
        
        [Parameter(Mandatory=$true)]
        [string]$SnapshotName,
        
        [Parameter(Mandatory=$true)]
        [string]$SnapshotDescription
    )

    try {
        # Get all virtual machines on the server
        $vms = Get-VM -Server $vCenter

        # Create a snapshot of each virtual machine
        foreach ($vm in $vms) {
            $snapshotParams = @{
                Name = $SnapshotName
                Description = $SnapshotDescription
                Confirm = $false
            }

            New-Snapshot -VM $vm -Memory -Quiesce @snapshotParams
        }

        Write-Output "Snapshots created successfully"
    }
    catch {
        Write-Error "Error creating snapshots: $($_.Exception.Message)"
    }
    finally {
        Disconnect-VIServer -Server $Server -Confirm:$false -ErrorAction SilentlyContinue
    }
}

function Restore-VMToSnapshot {
    param(
        [Parameter(Mandatory=$true)]
        [string]$VMName,
        
        [Parameter(Mandatory=$true)]
        [string]$FolderName,
        
        [Parameter(Mandatory=$true)]
        [string]$SnapshotName
    )
    # Get the virtual machine object
    $vm = Get-VM -Name $VMName -Location $FolderName

    if (!$vm) {
        Write-Error "Virtual machine '$VMName' not found in folder '$FolderName'."
        return
    }

    # Get the snapshot object
    $snapshot = Get-Snapshot -VM $vm | Where-Object {$_.Name -eq $SnapshotName}

    if (!$snapshot) {
        Write-Error "Snapshot '$SnapshotName' not found for virtual machine '$VMName'."
        return
    }

    # Revert to the snapshot
    $snapshot | Set-VMSnapshot -Confirm:$false

    Write-Output "Virtual machine '$VMName' rolled back to snapshot '$SnapshotName'."
}


# Connect to the vCenter server
$server = Read-Host "Enter the vsphere server ip or FQDN"
Connect-VIServer -Server $server -Credential (Get-Credential) -ErrorAction Stop

# Define the menu options
$menuOptions = @{
    '1' = 'Install PowerCLI'
    '2' = 'Get vSphere Inventory'
    '3' = 'Create Folder Snapshot'
    '4' = 'Create VM Snapshot'
    'q' = 'Quit'
}

$running = $true
# Display the menu
while ($running) {
    Write-Host ""
    Write-Host "Select an option:"
    foreach ($option in $menuOptions.GetEnumerator() | Sort-Object Name) {
        Write-Host "$($option.Key). $($option.Value)"
    }

    # Prompt for user input
    $choice = Read-Host "Enter an option"

    # Execute the selected function or quit
    switch ($choice) {
        '1' {
            Install-PowerCLI
        }
        '2' {
            $inventoryData = Get-VSphereInventory
            Write-Output "Writing to ./inventory.json"
            Write-Output $inventoryData > inventory.json
        }
        '3' {
            $folderName = Read-Host "Enter the folder name"
            $snapshotName = Read-Host "Enter the snapshot name"
            $snapshotDescription = Read-Host "Enter the snapshot description"
            New-FolderSnapshot -FolderName $folderName -SnapshotName $snapshotName -SnapshotDescription $snapshotDescription
        }
        '4' {
            $folderName = Read-Host "Enter the folder name"
            $snapshotName = Read-Host "Enter the snapshot name"
            $snapshotDescription = Read-Host "Enter the snapshot description"
            New-VMSnapshotAll -vCenter $server -FolderName $folderName -SnapshotName $snapshotName -SnapshotDescription $snapshotDescription
        }
        '5' {
            $folderName = Read-Host "Enter the folder name"
            $snapshotName = Read-Host "Enter the snapshot name"
            $vmName = Read-Host "Enter the vm name"
            Restore-VMToSnapshot -VMName $vmName -FolderName $folderName -SnapshotName $snapshotName
        }
        'q' {
            $running = $false
            Disconnect-VIServer -Server $server -Confirm:$false -ErrorAction SilentlyContinue
            break;
        }
        default {
            Write-Host "Invalid option"
        }
    }
}

