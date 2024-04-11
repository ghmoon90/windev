@echo off
setlocal enabledelayedexpansion

set "sourceDir=C:\Users\user\Desktop\test\src"
set "destDir=C:\Users\user\Desktop\test\dst"

call :CopyFolderAndContents "%sourceDir%" "%destDir%"
exit /b

:CopyFolderAndContents
set "source=%~1"
set "destination=%~2"

rem Check if the source folder exists
if not exist "%source%" (
    echo Source folder does not exist: !source!
    exit /b
)

rem Check if the destination folder exists, if not create it
if not exist "%destination%" (
    mkdir "%destination%"
)

rem Copy each file in the folder
for %%I in ("%source%\*") do (
    set "destFilePath=%destination%\%%~nxI"

    rem Check if the file already exists in the destination
    if exist "!destFilePath!" (
        rem Get size of source and destination files
        for %%J in ("!destFilePath!") do set "destSize=%%~zJ"
        set "srcSize=%%~zI"

        rem Compare sizes
        if !destSize! equ !srcSize! (
            echo Skipped file (already exists with same size): %%~nxI
        ) else (
            copy "%%I" "%destination%"
            echo Copied file: %%~nxI
        )
    ) else (
        copy "%%I" "%destination%"
        echo Copied file: %%~nxI
    )
)

rem Recursively copy subfolders
for /D %%D in ("%source%\*") do (
    call :CopyFolderAndContents "%%~fD" "%destination%\%%~nxD"
)

exit /b
