

Option Explicit

Dim objFSO
Set objFSO = CreateObject("Scripting.FileSystemObject")

Dim sourceDir, destDir
sourceDir = "C:\Users\GunHee\Desktop\test\src" ' Change this to the source directory path
destDir = "C:\Users\GunHee\Desktop\test\dst" ' Change this to the destination directory path

CopyFolderAndContents sourceDir, destDir

Sub CopyFolderAndContents(source, destination)
    Dim objFolder, objSubfolder, objFile

    ' Check if the source folder exists
    If Not objFSO.FolderExists(source) Then
        WScript.Echo "Source folder does not exist: " & source
        Exit Sub
    End If

    ' Check if the destination folder exists, if not create it
    If Not objFSO.FolderExists(destination) Then
        objFSO.CreateFolder destination
    End If

    Set objFolder = objFSO.GetFolder(source)

    ' Copy each file in the folder
    For Each objFile In objFolder.Files
	
		Do
			Dim destFilePath
			destFilePath = objFSO.BuildPath(destination, objFile.Name)

			' Check if the file already exists in the destination and has the same size
			If objFSO.FileExists(destFilePath) Then
				Dim destFile
				Set destFile = objFSO.GetFile(destFilePath)
				
				If destFile.Size = objFile.Size Then
					WScript.Echo "Skipped file (already exists with same size): " & objFile.Name
					Set destFile = Nothing
					Exit Do
				End If
				
				Set destFile = Nothing
				
			End If

			objFile.Copy destFilePath
			WScript.Echo "Copied file: " & objFile.Name

		Loop While False
    Next

    ' Recursively copy subfolders
    For Each objSubfolder In objFolder.Subfolders
        CopyFolderAndContents objSubfolder.Path, objFSO.BuildPath(destination, objSubfolder.Name)
    Next
End Sub
