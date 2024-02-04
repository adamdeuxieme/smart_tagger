@echo off
setlocal enabledelayedexpansion
set "exclude="

:loop
if "%~1"=="" goto :continue
if "%~1"=="--exclude" set "exclude=%~2"
if "%~1"=="-e" set "exclude=%~2"
shift
goto :loop

:continue
set "count=0"
set "total=0"

for %%i in (*.md) do (
    set /a "total+=1"
    if /I not "%%~nxi"=="%exclude%" (
        python C:\Users\adams\tools\bin\main.py tag -f "%%i" -t C:\Users\adams\tools\bin\tags.md -tn 4 > nul
        set /a "count+=1"
    )
    echo Processed !count! out of !total! files.
)

endlocal