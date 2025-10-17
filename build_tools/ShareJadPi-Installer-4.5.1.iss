#define MyAppName "ShareJadPi"
#define MyAppVersion "4.5.1"
#define MyAppPublisher "ShareJadPi Team"
#define MyAppURL "https://github.com/hetp2/sharejadpi"
#define MyAppExeName "ShareJadPi-4.5.1.exe"
#define MyAppIcon "icon.ico"

[Setup]
AppId={{ShareJadPi-4.5.1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE
OutputDir=..\installer_output
OutputBaseFilename=ShareJadPi-4.5.1-Setup
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
Source: "..\assets\{#MyAppIcon}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\scripts\*"; DestDir: "{app}\scripts"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userstartup}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: autostart
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

[Registry]
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
