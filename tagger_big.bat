@echo on
python C:\Users\adams\tools\bin\main.py tag -f "%~1" -t C:\Users\adams\tools\bin\tags.md -tn 10 > C:\Users\adams\tools\bin\output.txt
type C:\Users\adams\tools\bin\output.txt
pause
del C:\Users\adams\tools\bin\output.txt