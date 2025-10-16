; ShareJadPi v3.0.1 Installer Script for Inno Setup
; Download Inno Setup from: https://jrsoftware.org/isdl.php

#define MyAppName "ShareJadPi"
#define MyAppVersion "3.0.1"
#define MyAppPublisher "hetcharusat"
#define MyAppURL "https://github.com/hetcharusat/sharejadpi"
#define MyAppExeName "ShareJadPi-3.0.1.exe"

[Setup]
; Basic Information
AppId={{ShareJadPi-A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer_output
OutputBaseFilename=ShareJadPi-3.0.1-Setup
SetupIconFile=icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "contextmenu"; Description: "Add 'Share with ShareJadPi' to right-click menu"; GroupDescription: "Integration:"; Flags: checkedonce
Name: "autostart"; Description: "Start ShareJadPi when Windows starts"; GroupDescription: "Integration:"; Flags: checkedonce
Name: "firewall"; Description: "Add Windows Firewall rule (required for mobile access)"; GroupDescription: "Network:"; Flags: checkedonce

[Files]
; Main executable
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

; Icon file for context menu
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "TROUBLESHOOTING.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "RELEASE_NOTES_v3.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "EXE_FIX_NOTES.md"; DestDir: "{app}"; Flags: ignoreversion

; Helper scripts
Source: "fix_firewall.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "show_connection_info.ps1"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Troubleshooting Guide"; Filename: "{app}\TROUBLESHOOTING.md"
Name: "{group}\Fix Firewall"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\fix_firewall.ps1"""
Name: "{group}\Show Connection Info"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\show_connection_info.ps1"""
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; Context Menu Integration
Root: HKCR; Subkey: "*\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu

Root: HKCR; Subkey: "Directory\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu

; Autostart
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ShareJadPi"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

[Run]
; Add firewall rule during installation
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""ShareJadPi Port 5000"""; Flags: runhidden; Tasks: firewall
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""ShareJadPi Port 5000"" dir=in action=allow protocol=TCP localport=5000 profile=any"; Flags: runhidden; Tasks: firewall
; Run app after installation
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
; Remove firewall rule during uninstall
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""ShareJadPi Port 5000"""; Flags: runhidden
; Kill running process before uninstall
Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden; RunOnceId: "KillShareJadPi"

[Code]
// Check if app is running before uninstall
function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  // Try to kill gracefully first
  Exec('taskkill', '/IM ShareJadPi-3.0.1.exe /F', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

// Custom messages during installation
procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Show success message
    MsgBox('ShareJadPi has been installed successfully!' + #13#10 + #13#10 +
           'The app will start automatically. Look for the green icon in your system tray.' + #13#10 + #13#10 +
           'Tips:' + #13#10 +
           '• Right-click the tray icon to access all features' + #13#10 +
           '• Use "Show QR" to connect from mobile devices' + #13#10 +
           '• If mobile can''t connect, run "Fix Firewall" from Start Menu' + #13#10 + #13#10 +
           'See TROUBLESHOOTING.md for help!',
           mbInformation, MB_OK);
  end;
end;

// Pre-install checks
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  
  // Check if app is already running
  if CheckForMutexes('ShareJadPi-3.0.1-Running') then
  begin
    if MsgBox('ShareJadPi is currently running. Setup will close it to continue.' + #13#10 + #13#10 +
              'Continue with installation?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec('taskkill', '/IM ShareJadPi-3.0.1.exe /F', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Result := True;
    end
    else
      Result := False;
  end;
end;
