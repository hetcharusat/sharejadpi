# Build ShareJadPi into a standalone Windows exe using PyInstaller
param(
    [string]$Python = "python",
    [string]$Icon = "",
    [switch]$OneDir,
    [switch]$Debug,
    [switch]$Console,
    [string]$Version = "1.0.0",
    [string]$Company = "hetpatel7567",
    [string]$Product = "ShareJadPi",
    [string]$Name = "ShareJadPi",
    [switch]$AppendVersion
)

$ErrorActionPreference = "Stop"

# Ensure venv for clean builds (optional)
# python -m venv .venv; .venv\Scripts\Activate.ps1; pip install -r requirements.txt pyinstaller

# Optional UPX detection for compression
$upx = $null
try { $upxCmd = Get-Command upx -ErrorAction SilentlyContinue; if ($upxCmd) { $upx = Split-Path $upxCmd.Source -Parent } } catch {}

# Generate temporary version resource (numeric tuples expected)
$verFile = Join-Path $env:TEMP ("sjp_ver_" + [Guid]::NewGuid().ToString() + ".txt")
$v = [version]$Version
$maj = $v.Major
$min = $v.Minor
$bld = if ($v.Build -ge 0) { $v.Build } else { 0 }
$rev = if ($v.Revision -ge 0) { $v.Revision } else { 0 }
$verText = @"
VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=($maj, $min, $bld, $rev),
        prodvers=($maj, $min, $bld, $rev),
        mask=0x3f,
        flags=0x0,
        OS=0x4,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0)
    ),
    kids=[
        StringFileInfo([
            StringTable('040904B0', [
                StringStruct('CompanyName', '$Company'),
                StringStruct('FileDescription', '$Product'),
                StringStruct('FileVersion', '$Version'),
                StringStruct('InternalName', 'ShareJadPi'),
                StringStruct('OriginalFilename', 'ShareJadPi.exe'),
                StringStruct('ProductName', '$Product'),
                StringStruct('ProductVersion', '$Version')
            ])
        ]),
        VarFileInfo([VarStruct('Translation', [1033, 1200])])
    ]
)
"@
$verText | Set-Content -Encoding ASCII -Path $verFile

$exeName = if ($AppendVersion) { "$Name-$Version" } else { $Name }

$specArgs = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--name", $exeName,
    # Run as background (no console window) unless -Console is specified
    $(if ($Console) { $null } else { "--noconsole" }),
        "--version-file", $verFile,
    "--add-data", "templates;templates",
    "--add-data", "static;static",
    "--hidden-import", "pystray._base",
    "--hidden-import", "pystray._win32",
    "--hidden-import", "PIL._imaging",
    "--hidden-import", "PIL.Image",
    "--hidden-import", "PIL.ImageDraw"
)

if ($Icon) { $specArgs += @("--icon", $Icon) }
if ($OneDir) { $specArgs += "--onedir" } else { $specArgs += "--onefile" }
if ($Debug) { $specArgs += "--log-level=DEBUG" } else { $specArgs += "--log-level=WARN" }
if ($upx) { $specArgs += @("--upx-dir", $upx) }

$specArgs += "sharejadpi.py"

& $Python $specArgs

Write-Host "\nBuild complete. Output in dist\\ShareJadPi.exe (or dist\\ShareJadPi\\*)" -ForegroundColor Green
