; ShareJadPi v4.1.3 Installer Script for Inno Setup
; Download Inno Setup from: https://jrsoftware.org/isdl.php

#define MyAppName "ShareJadPi"
#define MyAppVersion "4.1.3"
#define MyAppPublisher "hetcharusat"
#define MyAppURL "https://github.com/hetcharusat/sharejadpi"
#define MyAppExeName "ShareJadPi-4.1.3.exe"

[Setup]
; Basic Information
AppId={{ShareJadPi-A1B2C3D4-E5F6-7890-ABCD-EF1234567890}}
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
LicenseFile=..\LICENSE
OutputDir=..\installer_output
OutputBaseFilename=ShareJadPi-4.1.3-Setup
SetupIconFile=..\assets\icon.ico
Compression=lzma2/max
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
ChangesAssociations=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "contextmenu"; Description: "Add 'Share with ShareJadPi' to right-click menu"; GroupDescription: "Integration:"; Flags: checkedonce
Name: "autostart"; Description: "Start ShareJadPi when Windows starts"; GroupDescription: "Integration:"; Flags: checkedonce
Name: "firewall"; Description: "Add Windows Firewall rule (required for mobile access)"; GroupDescription: "Network:"; Flags: checkedonce

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\cloudflared.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\\TROUBLESHOOTING.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\\fix_firewall.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\\show_connection_info.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Troubleshooting Guide"; Filename: "{app}\TROUBLESHOOTING.md"
Name: "{group}\Fix Firewall"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\fix_firewall.ps1"""
Name: "{group}\Show Connection Info"; Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{app}\show_connection_info.ps1"""
Name: "{group}\Install Context Menu (User)"; Filename: "{app}\{#MyAppExeName}"; Parameters: "install-context-menu"; WorkingDir: "{app}"
Name: "{group}\Remove Context Menu (User)"; Filename: "{app}\{#MyAppExeName}"; Parameters: "uninstall-context-menu"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
Root: HKCR; Subkey: "*\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Local)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Local)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPiOnline"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Online)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPiOnline"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "*\shell\ShareJadPiOnline\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" open-online ""%1"""; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPiOnline"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Online)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPiOnline"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCR; Subkey: "Directory\shell\ShareJadPiOnline\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" open-online ""%1"""; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ShareJadPi"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: autostart

; Also create per-user context menus under HKCU for reliability (no admin needed)
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Local)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPi"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Local)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPi"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPi\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" share ""%1"""; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPiOnline"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Online)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPiOnline"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\*\shell\ShareJadPiOnline\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" open-online ""%1"""; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPiOnline"; ValueType: string; ValueName: ""; ValueData: "Share with ShareJadPi (Online)"; Flags: uninsdeletekey; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPiOnline"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Tasks: contextmenu
Root: HKCU; Subkey: "Software\Classes\Directory\shell\ShareJadPiOnline\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" open-online ""%1"""; Tasks: contextmenu

[Run]
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""ShareJadPi Port 5000"""; Flags: runhidden; Tasks: firewall
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""ShareJadPi Port 5000"" dir=in action=allow protocol=TCP localport=5000 profile=any"; Flags: runhidden; Tasks: firewall
Filename: "{cmd}"; Parameters: "/c ie4uinit.exe -ClearIconCache"; Flags: runhidden
Filename: "{cmd}"; Parameters: "/c ie4uinit.exe -show"; Flags: runhidden
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallRun]
Filename: "netsh"; Parameters: "advfirewall firewall delete rule name=""ShareJadPi Port 5000"""; Flags: runhidden
Filename: "taskkill"; Parameters: "/F /IM {#MyAppExeName}"; Flags: runhidden; RunOnceId: "KillShareJadPi"

[Code]
const
  SHCNE_ASSOCCHANGED = $08000000;
  SHCNF_IDLIST = $0000;

procedure SHChangeNotify(EventID: Integer; Flags: Cardinal; Item1, Item2: Integer);
  external 'SHChangeNotify@shell32.dll stdcall setuponly';

function InitializeUninstall(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  Exec('taskkill', '/IM {#MyAppExeName} /F', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, 0, 0);
    MsgBox('ShareJadPi has been installed successfully!' + #13#10 + #13#10 +
      'The app will start automatically. Look for the green icon in your system tray.' + #13#10 + #13#10 +
      'Tips:' + #13#10 +
      '- Right-click the tray icon to access all features' + #13#10 +
      '- Use "Show QR" to connect from mobile devices' + #13#10 +
      '- If mobile can''t connect, run "Fix Firewall" from Start Menu' + #13#10 + #13#10 +
      'See TROUBLESHOOTING.md for help!',
      mbInformation, MB_OK);
  end;
end;

function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;
  if CheckForMutexes('ShareJadPi-Running') then
  begin
    if MsgBox('ShareJadPi is currently running. Setup will close it to continue.' + #13#10 + #13#10 +
              'Continue with installation?', mbConfirmation, MB_YESNO) = IDYES then
    begin
      Exec('taskkill', '/IM {#MyAppExeName} /F', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      Result := True;
    end
    else
      Result := False;
  end;
end;
