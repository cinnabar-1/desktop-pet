## lib
pyinstaller

## build project 
 - pyinstaller -y --add-data '*.gif;.' .\pet.py
 - pyinstaller -y -i icon.ico --add-data '*.gif;.' .\pet.py
 - pyinstaller -w -F -i icon.ico --add-data 'assets;assets' .\pet.py -y