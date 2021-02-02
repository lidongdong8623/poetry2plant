@echo off

echo Install  python ... 

start /w "" python-3.6.8-amd64.exe 

echo install python ok!  

pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

xcopy  zh-CN  C:\Users\Administrator\AppData\Local\Programs\Python\Python36\Lib\site-packages\speech_recognition\pocketsphinx-data\zh-CN\  /E /Y 

python poetry2plant.py  

pause