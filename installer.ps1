function Install {
    $appDataLocal = $env:LOCALAPPDATA  # Store AppData\Local path

    # Define paths within AppData\Local
    $bigBrotherDir = Join-Path $appDataLocal "BigBrother"
    $venvDir = Join-Path $bigBrotherDir "venv"
    $soundsDir = Join-Path $bigBrotherDir "sounds"
    $binDir = Join-Path $bigBrotherDir "bin"

    #--- Installation Steps ---
    Try {
        # Set file permissions (if needed)
        Set-ItemProperty -Path bigbrother -Name Access -Value (Get-Acl bigbrother).Access
        
        # Create directories
        New-Item -ItemType Directory -Force -Path $bigBrotherDir, $soundsDir, $binDir

        # Copy files
        Copy-Item -Path bigbrother -Destination $binDir
        Copy-Item -Path police.mp3 -Destination $soundsDir

        # Create virtual environment 
        python -m venv $venvDir 

        # Install dependencies
        & $venvDir\Scripts\pip.exe install -r requirements.txt 

            # Modify the User's PATH environment variable
        $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        $newPath = $userPath + ";" + $binDir  # Add binDir to the path

        [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")

        Write-Output "Installation successful! The path was updated. You may need to open a new command prompt/PowerShell window for changes to take effect."
    } Catch {
        # Handle errors gracefully
        Write-Error "Installation failed: $_" 
    }
}

function Uninstall {
    $appDataLocal = $env:LOCALAPPDATA
    $bigBrotherDir = Join-Path $appDataLocal "BigBrother"

    Try {
        # Remove the entire BigBrother directory 
        Remove-Item -Recurse -Force $bigBrotherDir

        Write-Output "Uninstall successful!"
    } Catch {
        Write-Error "Uninstall failed: $_"
    }
}

function Usage {
    Write-Output @"
Usage: $MyInvocation.MyCommand.Name OPTIONS
This script installs or uninstalls The Big Brother.
OPTIONS:
    -i             Install The Big Brother.
    -r             Uninstall The Big Brother.
    -h, --help     Print this help message.
"@
}

switch ($args[0]) {  # PowerShell uses $args for script arguments
    "-h" {
        $Usage;
        break
    } 
    "--help" {
        $Usage; 
        break
    }  
    "-i" {
        Install;
        break
    }
    "-r" {
        Uninstall;
        break
    }
    default {$Usage} 
}