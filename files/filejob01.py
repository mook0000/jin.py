import os

a = '\n현재 작업폴더 얻기'
print(a)
print(os.getcwd())
# /Users/evan/dev/python/web-crawler-py/parsed_data

a = '\n현 작업 디렉토리변경'
print(a)
os.chdir("c:/temp")
print(os.getcwd())
# /Users

a = '\n특정경로에 대해 절대 경로 얻기'
print(a)
print(os.path.abspath("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# /Users/evan/dev/python/web-crawler-py/parsed_data/web-crawler-py/parsed_data

a = '\n경로중 디렉토리명만 얻기'
print(a)
print(os.path.dirname("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# Users/evan/dev/python/web-crawler-py

a = '\n경로중 파일명만 얻기'
print(a)
print(os.path.basename("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# parsed_data

a = '\n경로중 디렉토리명과 파일명 나누어 얻기'
print(a)
dir, file = os.path.split("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log")
print(dir, file, sep="/n")
# /Users/evan/dev/python/web-crawler-py
# parsed_data

a = '\n파일 경로를 리스트로 얻기'
print(a)
print("/Users/LIM/Documents".split(os.path.sep))
# ['', 'Users', 'evan', 'dev', 'python', 'web-crawler-py', 'parsed_data']

a = '\n경로를 병합하여 새 경로 생성'
print(a)
print(os.path.join("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# /Users/evan/dev/python/web-crawler-py/parsed_data/test

a = '\n디렉토리 안의 파일/서브 디렉토리 리스트'
print(a)
print(os.listdir("C:/Users/Public"))
# ['migrations', 'models.py', '__init__.py', '__pycache__', 'apps.py', 'parser.py', 'admin.py', 'tests.py', 'views.py']

a = '\n파일 혹은 디렉토리가 존재하는지 체크'
print(a)
print(os.path.exists("c:/Users/LIM/NTUSER.DAT"))
# True
print(os.path.exists("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# True

a = '\n디렉토리가 존재하는지 체크'
print(a)
print(os.path.isdir("C:/Arduino/connect_wifitemp"))
# True
print(os.path.isdir("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
# False

a = '\n파일의 크기'
print(a)
print(os.path.getsize("C:/Naver MYBOX/녹화_2021_01_27_16_10_20_686.mp4"))
# 352

print(os.path.getatime("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
print(os.path.getctime("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))
print(os.path.getmtime("C:/Fuji Xerox/ApeosWare_MS/Installer/logs/UDS_Setup_20210129-1.log"))