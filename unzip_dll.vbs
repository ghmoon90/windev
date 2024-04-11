Set objShell = CreateObject("Shell.Application")
Set objFSO = CreateObject("Scripting.FileSystemObject")

' Check if the script was called with an argument
If WScript.Arguments.Count = 0 Then
    MsgBox "Please provide the path to the zip file as an argument.", vbExclamation
    WScript.Quit
End If

' Get the zip file path from the argument
zipPath = WScript.Arguments.Item(0)

' Check if the zip file exists
If Not objFSO.FileExists(zipPath) Then
    MsgBox "The specified zip file does not exist.", vbExclamation
    WScript.Quit
End If

' Extract the directory name from the zip file path
zipFileName = objFSO.GetFileName(zipPath)
dstPath = objFSO.GetParentFolderName(zipPath) & "\" & objFSO.GetBaseName(zipFileName)

' Create the destination directory if it doesn't exist
If Not objFSO.FolderExists(dstPath) Then
    objFSO.CreateFolder dstPath
End If


' Create a reference to the zip file
Set zipObject = objShell.NameSpace(zipPath)
' Create a reference to the destination folder
Set destinationObject = objShell.NameSpace(dstPath)

' unzip 
destinationObject.CopyHere(zipObject.Items)


' Function to recursively search for DLL files in subfolders
Sub SearchForDlls(folder)
    Dim subfolder
    For Each subfolder In folder.SubFolders
        SearchForDlls subfolder
    Next
    Dim file
    For Each file In folder.Files
        If LCase(objFSO.GetExtensionName(file.Path)) = "dll" Then
            objFSO.CopyFile file.Path, objFSO.BuildPath(objFSO.GetParentFolderName(dstPath), objFSO.GetFileName(file.Path)), True
        End If
    Next
End Sub

' Call the function to search for DLL files in subfolders
SearchForDlls objFSO.GetFolder(dstPath)

MsgBox "Extraction and copying completed.", vbInformation
