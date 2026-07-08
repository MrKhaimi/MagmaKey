[Setup]
AppName=MagmaKey
AppVersion=1.0.5
AppPublisher=MrKhaimi
DefaultDirName={pf}\MagmaKey
DefaultGroupName=MagmaKey
PrivilegesRequired=admin
UninstallDisplayIcon={app}\MagmaKey.exe
OutputDir=.\Installer
OutputBaseFilename=MagmaKey_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
SetupIconFile=magmakey.ico

[Files]
Source: "dist\MagmaKey\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userdesktop}\MagmaKey"; Filename: "{app}\MagmaKey.exe"
Name: "{userprograms}\MagmaKey\MagmaKey"; Filename: "{app}\MagmaKey.exe"

[Run]
Filename: "{app}\MagmaKey.exe"; Description: "Запустить MagmaKey"; Flags: nowait postinstall skipifsilent
