import os
import shutil

# 동일 파일을 이동시킬 폴더
dest_root_path = "G:/temp/"


# 파일 이동 함수
def file_move(src):
    # 현재 폴더 구조 그대로 dest_root_path에 지정한 위치에 이동
    dest_file = dest_root_path + src
    dest_folder = os.path.dirname(dest_file)
    try:
        shutil.move(src, dest_file)
    except:
        # 만약 에러가 발생하면 폴더가 존재하는지 확인 하여 없으면 파일 생성 후 이동
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            shutil.move(src, dest_file)


# 동일 파일 검색 및 이동
def search_same_files(search_path):
    exist_file_names = {}
    print(search_path)

    for (path, dir, files) in os.walk(search_path):
        for filename in files:
            # 이미 발견된 파일 이름과 같은지 비교
            if filename in exist_file_names:
                '''
                exist_file_names[파일명] = 파일 크기
                '''
                # 이미 발견된 파일 크기 얻기
                file_size_already_exist = exist_file_names[filename]
                # 지금 발견된 파일 크기 얻기
                file_size = os.path.getsize(path + "/" + filename)

                # 파일 크기가 같으면 동일 파일
                if file_size_already_exist == file_size:
                    file_path = "%s/%s" % (path, filename)
                    print(file_path)

                    # 파일을 다른 곳으로 이동
                    file_move(file_path)

                    print('same file : ', filename, end='')
                    print(', file_size_already_exist : ', file_size_already_exist, end='')
                    print(', file size : ', file_size)

                else:
                    # 파일이름은 같지만 크기가 다르면 다른 파일로 간주
                    # print('not the same file : ', filename)
                    pass
            else:
                # 처음 발견된 파일
                # key로 파일 명을 지정하고
                # value는 파일 크기를 저장한다.
                exist_file_names[filename] = os.path.getsize(path + "/" + filename)


search_same_files('../')