param([switch]$Elevated)

function Test-Admin {
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent())
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}

if ((Test-Admin) -eq $false)  {
    if ($elevated) {
        # tried to elevate, did not work, aborting
    } else {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}

# Write-Host "running with full privileges"

$iCloneInstallPathKey = "HKLM:\SOFTWARE\Reallusion\iClone\8.0"  

$iCloneInstallPath = Get-ItemPropertyValue -Path $iCloneInstallPathKey -Name "Install Path"

# Check if OpenPlugin folder exists, create it if not
if ((Test-Path -Path "$iCloneInstallPath\OpenPlugin")) {
    Write-Host ""
    Write-Host "OpenPlugin folder exists (in $iCloneInstallPath)"
}else{
    Write-Host ""
    Write-Host "Creating OpenPlugin folder in $iCloneInstallPath"
    New-Item -Path "$iCloneInstallPath\OpenPlugin" -ItemType Directory
}

# Get the script's directory
$ScriptDirectory = $PSScriptRoot
$FolderName = Split-Path -Path $ScriptDirectory -Leaf

# Create symbolic link from OpenPlugin to script directory
# New-Item -Path "$iCloneInstallPath\OpenPlugin\$FolderName" -ItemType SymbolicLink -Target "$ScriptDirectory"

# Junction works
$JunctionPath = "$iCloneInstallPath\OpenPlugin\$FolderName"
cmd /c mklink /J "$JunctionPath" "$ScriptDirectory" | Out-Null

Write-Host ""
Write-Host "Folder shortcut $JunctionPath has been created"
Write-Host ""
Write-Host "Relaunch iClone if it is currently open."
Write-Host ""
Write-Host "Press any key to continue..."
Write-Host ""
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
Write-Host "This window can now be safely closed."