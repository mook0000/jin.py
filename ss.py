#자기사진 사용
# 512x512 이미지 처리하기
# -밝게, 어둡게, 반전, 흑백(127,평균값, 중앙값)
# -90도 회전, 180도 회전, 270도 회전
# -좌우 미러링, 상하 미러링
#-------------------------여기가지 했슴다-------------------------
# -(심화) 감마 연산, 파라볼라 연산
# -(심화) 2배 축소, 2배 확대
# -(심화) 45도 회전

#라이브러리
import os
from tkinter import *
import math
import sys
sys.setrecursionlimit(262144)


## 함수
def displayImage():
    global window,canvas,paper,height,width,filename
    if canvas is not None:
        canvas.destroy()

    canvas = Canvas(window, height=512, width=512)
    paper = PhotoImage(height=512, width=512)
    canvas.create_image((512 / 2, 512 / 2), image=paper, state='normal')

    for i in range(height) :
        for k in range(width) :
            r = g = b = image[i][k]
            paper.put('#%02x%02x%02x' % (r, g, b), (k, i))
    canvas.pack()

def brightbtn():
    for i in range(height):
        for k in range(width):
            if(image[i][k]+100 >256):
                image[i][k]=255
            else:
                image[i][k] +=100
    displayImage()

def darkbtn():
    for i in range(height):
        for k in range(width):
            if(image[i][k]-100 <0):
                image[i][k]=0
            else:
                image[i][k] -=100
    displayImage()

def reversebtn():
    for i in range(height):
        for j in range(width):
            image[i][j] = 255 - image[i][j]
    displayImage()

def getAvg():
    hap = 0
    for i in range(height):
        for j in range(width):
            hap +=image[height][width]
    return int(hap/(height*width))

def dark127btn():
    for i in range(height):
        for j in range(width):
            if(image[i][j] >127):
                image[i][j] = 255
            else:
                image[i][j] = 0
    displayImage()
def darkAvgbtn():
    for i in range(height):
        for j in range(width):
            if(image[i][j] >getAvg()):
                image[i][j] = 255
            else:
                image[i][j] = 0
    displayImage()

def imageto1array(image):
    image1 = []
    for i in range(height):
        for j in range(width):
            image1.append(image[i][j])
    return image1

def quick_sort(array, start, end):
    if start >= end: return  # 원소가 1개인 경우
    pivot = start  # 피벗은 첫 요소
    left, right = start + 1, end

    while left <= right:
        # 피벗보다 작은 데이터를 찾을 때까지 반복
        while left <= end and array[left] <= array[pivot]:
            left += 1
        # 피벗보다 큰 데이터를 찾을 때까지 반복
        while right > start and array[right] >= array[pivot]:
            right -= 1
        if left > right:  # 엇갈린 경우
            array[right], array[pivot] = array[pivot], array[right]
        else:  # 엇갈리지 않은 경우
            array[right], array[left] = array[left], array[right]
    # 분할 이후 왼쪽 부분과 오른쪽 부분에서 각각 정렬 수행
    quick_sort(array, start, right - 1)
    quick_sort(array, right + 1, end)

def GetMediumNum():
    image2 = []
    image2 = imageto1array(image)
    quick_sort(image2, 0, height*width-1)
    print(height/2,width/2)
    return image2[int(height/2*width/2)]

def mediumbtn():
    mediumNum = GetMediumNum()
    for i in range(height):
        for j in range(width):
            if(image[i][j] >mediumNum):
                image[i][j] = 255
            else:
                image[i][j] = 0
    print(mediumNum)
    displayImage()

def rotate90btn():
    global image
    result = [[0] * height for _ in range(width)]
    for i in range(height):
        for j in range(width):
            result[j][height-i-1] = image[i][j]

    image = result
    displayImage()

# 180도 회전
def rotate180btn():
    global image
    rotated_image = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for k in range(width):
            rotated_image[height - i - 1][width - k - 1] = image[i][k]  # 180도 회전

    image = rotated_image
    displayImage()

# 270도 회전
def rotate270btn():
    global image
    result = [[0] * height for _ in range(width)]
    for i in range(height):
        for j in range(width):
            result[width-j-1][i] = image[i][j]

    image = result
    displayImage()

def flipImage():
    global image
    flipped_image = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for k in range(width):
            flipped_image[i][k] = image[height - i - 1][k]  # 상하반전

    image = flipped_image
    displayImage()

def mirrorImage():
    global image
    mirrored_image = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for k in range(width):
            mirrored_image[i][k] = image[i][width - k - 1]  # 좌우반전

    image = mirrored_image
    displayImage()
## 변수
window, canvas, paper = None, None, None
filename = ""
height, width = 0, 0
image = []

## 메인
window = Tk()
window.geometry('700x900')
window.title('영상처리 Alpha')

brightbtn = Button(window, text='밝게',command = brightbtn)
darkbtn = Button(window, text='어둡게',command = darkbtn)
reversebtn = Button(window,text='반전',command = reversebtn)
dark127btn=Button(window,text='흑백127',command=dark127btn)
darkAvgbtn=Button(window,text='흑백avg',command=darkAvgbtn)
mediumbtn=Button(window,text='중앙값',command= mediumbtn)
rotate90btn=Button(window,text='90도 회전',command= rotate90btn)
rotate180btn=Button(window,text='180도 회전',command= rotate180btn)
rotate270btn=Button(window,text='270도 회전',command= rotate270btn)
flipbtn = Button(window,text='상하반전',command= flipImage)
mirrorbtn = Button(window,text='좌우반전',command=mirrorImage)



brightbtn.pack()
darkbtn.pack()
reversebtn.pack()
dark127btn.pack()
darkAvgbtn.pack()
mediumbtn.pack()
rotate90btn.pack()
rotate180btn.pack()
rotate270btn.pack()
flipbtn.pack()
mirrorbtn.pack()

filename = 'jinwoo1.RAW'
# 파일 크기 알아내기
fSize = os.path.getsize(filename) # Byte 단위
height = width = int(math.sqrt(fSize))


print(height,width)


# 메모리 확보 (영상 크기)
image = [ [0 for _ in range(width)] for _ in range(height)]
# 파일 --> 메모리 로딩
rfp = open(filename, 'rb')
for i in range(height) :
    for k in range(width) :
        image[i][k] = ord(rfp.read(1))

rfp.close()
displayImage()



window.mainloop()