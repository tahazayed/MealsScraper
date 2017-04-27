call GetFileSize.bat links.txt
echo %GetFileSize%
if (%GetFileSize%) == ()     goto No_File
if (%GetFileSize%) == (0)    goto No_File

del /f oldlinks.txt
copy links.txt oldlinks.txt
jupyter nbconvert --to script Cookpad.ipynb

python Cookpad.py

cd output

for %%f in (*.json) do ("mongoimport.exe" -h taha-amin:27017 --jsonArray --db meals --collection "recipes" --file "%%~nf.json" /username:admin /password:dodido_2008 --authenticationDatabase admin)
cd "..\..\01-Extract Links"

:No_File
cd "..\01-Extract Links"
pause


