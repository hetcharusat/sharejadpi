; Inno Setup script for ShareJadPi 4.5.4
#define MyAppName "ShareJadPi"
#define MyAppVersion "4.5.4"
#define MyAppPublisher "hetcharusat"
#define MyAppURL "https://github.com/hetcharusat/sharejadpi"
#define MyAppExeName "ShareJadPi-4.5.4.exe"

[Setup]
AppId={{ShareJadPi}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
OutputDir=..\installer_output
OutputBaseFilename=ShareJadPi-4.5.4-Setup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64

[Files]
Source: "..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\assets\icon.ico"; DestDir: "{app}"
Source: "..\cloudflared.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\ShareJadPi"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\ShareJadPi"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop icon"; GroupDescription: "Additional options:"; Flags: checkedonce
Name: "autostart"; Description: "Start ShareJadPi when Windows starts"; GroupDescription: "Additional options:"; Flags: checkedonce

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "ShareJadPi"; ValueData: """{app}\{#MyAppExeName}"""; Tasks: autostart; Flags: uninsdeletevalue

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch ShareJadPi"; Flags: nowait postinstall skipifsilent
