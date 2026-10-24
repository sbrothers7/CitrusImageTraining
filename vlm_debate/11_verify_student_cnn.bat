@echo off
setlocal
chcp 65001 >nul 2>&1
set "PYTHONIOENCODING=utf-8"
set "PYTHONUTF8=1"
cd /d "%~dp0"

set "PY="
rem 1) the exact Python that worked in step 4/5, then other known locations
for %%P in ("%LOCALAPPDATA%\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0\python.exe" "%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe" "%LOCALAPPDATA%\Microsoft\WindowsApps\python3.exe") do (
  if not defined PY if exist %%P ( %%P -c "import sys" >nul 2>&1 && set PY="%%~P" )
)
for /d %%D in ("%LOCALAPPDATA%\Programs\Python\Python3*") do (
  if not defined PY if exist "%%~D\python.exe" set PY="%%~D\python.exe"
)
if not defined PY ( py -3 -c "import sys" >nul 2>&1 && set "PY=py -3" )
if not defined PY ( python -c "import sys" >nul 2>&1 && set "PY=python" )
if defined PY goto have_py
if not exist logs mkdir logs
set PATH > logs\pyfind.txt 2>&1
where python >> logs\pyfind.txt 2>&1
where py >> logs\pyfind.txt 2>&1
dir "%LOCALAPPDATA%\Microsoft\WindowsApps\*python*" >> logs\pyfind.txt 2>&1
echo [ERROR] Python not found. Details saved to logs\pyfind.txt - tell Claude.
pause
exit /b 1
:have_py
echo Using Python: %PY%

if not exist logs mkdir logs
echo ============================================================
echo   Step 11 - reproduce the student's CNN experiment
echo   densenet121, one source vs two sources, seeds 42 / 1 / 2
echo   First run downloads PyTorch (about 2.5 GB) and datasets.
echo   About 1.5-2.5 hours. Keep the laptop plugged in.
echo   Log: logs\verify_student.log
echo ============================================================
%PY% -u tools\verify_student_cnn.py
echo.
echo Finished. Tell Claude it is done.
pause
