# 필수 초기화
import pygame
import random

import bg_colors
from bg_colors import custom
from resources import ImageResources
from mineSweeper import MineSweeper

pygame.init()

# 화면 크기
screen = pygame.display.set_mode((310, 512))

# 아이콘 설정
#icon = ImageResources('icon.png')
# pygame.display.set_icon(icon.sprite)

# FPS
clock = pygame.time.Clock()

# 화면 타이틀
pygame.display.set_caption("지뢰찾기")

# 게임 폰트
game_font = pygame.font.Font(None, 25)

# 게임 배경 및 이미지
mineBoard = ImageResources('mineBoard.png')
resetButton = ImageResources('ResetButton.png')
widthVariable = ImageResources('setVariable.png')
heightVariable = ImageResources('setVariable.png')
minesVariable = ImageResources('setVariable.png')

#지뢰판의 너비 및 높이
rectLength = 30 #정사각형 길이 (지뢰 발판용)
mineBase = MineSweeper(15, 15, 30)
screen = pygame.display.set_mode((rectLength * mineBase.width + (mineBase.width-1), rectLength * mineBase.height + (mineBase.height-1) + 50))

#리셋 버튼 위치
resetButton.setPosition(1, rectLength * mineBase.height + mineBase.height)
#지뢰 개수, 넓이 설정 UI 띄우기
widthVariable.setPosition(115,rectLength * mineBase.height + rectLength - 10)
heightVariable.setPosition(115,rectLength * mineBase.height + rectLength + 10)
minesVariable.setPosition(255, rectLength * mineBase.height + rectLength - 10)
#갱신할 떄 도와줄 속성들
newWidth = 0
newHeight = 0
newMines = 0

#마우스 클릭 검사
def MouseOnMine(xPos, yPos):
    if(xPos >= 0 and xPos < mineBase.width) and (yPos >= 0 and yPos < mineBase.height):
        mineBase.ClickArea(xPos, yPos)
        if (mineBase.GetGameOver()):
            #모든 지뢰 보여주기
            for i in range(mineBase.height):
                for j in range(mineBase.width):
                    mineBase.ClickArea(j,i)

# 화면 그리기
def drawImage():
    screen.fill(custom(128,128,128))

    for i in range(mineBase.height):
        for j in range(mineBase.width):
            pygame.draw.rect(screen, custom(64,64,64),(j*rectLength + j,i*rectLength + i,rectLength,rectLength))

            #숫자 그리기
            mineBoard.setPosition(j * rectLength + j, i * rectLength + i)
            if(mineBase.GetAreaClicked()[i][j] == 1):   #클릭한 위치에 표시
                mineBoard.setClipping(30 * (mineBase.GetArea(j,i) + 1),0,rectLength,rectLength)
                screen.blit(mineBoard.sprite,mineBoard.getPosition(),mineBoard.sprite_clip)
            elif (mineBase.GetAreaClicked()[i][j] == 2):
                mineBoard.setClipping(300, 0, rectLength,rectLength)
                screen.blit(mineBoard.sprite,mineBoard.getPosition(),mineBoard.sprite_clip)

    #리셋
    screen.blit(resetButton.sprite,resetButton.getPosition())

    #너비 및 높이 조절 텍스트
    setBoardWidth = game_font.render("width : "+ str(mineBase.width + newWidth),True,bg_colors.custom(50,50,128))
    screen.blit(setBoardWidth, (140,rectLength * mineBase.height + rectLength - 10))
    setBoardHeight = game_font.render("height : "+str(mineBase.height + newHeight), True, bg_colors.custom(128,50,50))
    screen.blit(setBoardHeight, (140, rectLength * mineBase.height + rectLength + 10))
    setMineCount = game_font.render("mines : "+str(mineBase.mines + newMines), True,bg_colors.custom(102, 80, 30))
    screen.blit(setMineCount, (280,rectLength * mineBase.height + rectLength - 10))

    #가변값
    #너비
    widthVariable.setClipping(0,0,20,20)
    screen.blit(widthVariable.sprite, widthVariable.getPosition(),widthVariable.sprite_clip)
    widthVariable.setClipping(20,0,20,20)
    screen.blit(widthVariable.sprite, (230,widthVariable.getPosition()[1]),widthVariable.sprite_clip)
    #높이
    heightVariable.setClipping(0,0,20,20)
    screen.blit(heightVariable.sprite, heightVariable.getPosition(),heightVariable.sprite_clip)
    heightVariable.setClipping(20,0,20,20)
    screen.blit(heightVariable.sprite, (230,rectLength * mineBase.height + rectLength + 10),heightVariable.sprite_clip)
    #지뢰
    minesVariable.setClipping(0,0,20,20)
    screen.blit(minesVariable.sprite,(255,rectLength * mineBase.height + rectLength - 10),minesVariable.sprite_clip)
    minesVariable.setClipping(20,0,20,20)
    screen.blit(minesVariable.sprite,(370,rectLength * mineBase.height + rectLength - 10),minesVariable.sprite_clip)

# 게임 진행 루프
running = True
while running:
    # 초당 지정된 프레임 횟수동안 동작
    dt = clock.tick(60)

    set_speed = 3
    # 키보드 이벤트
    for event in pygame.event.get():
        # 화면 창을 닫을 때
        if event.type == pygame.QUIT:
            running = False

        # 마우스 체크
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousePosX = int(pygame.mouse.get_pos()[0] / rectLength)
            mousePosY = int(pygame.mouse.get_pos()[1] / rectLength)

            mouseOptX = pygame.mouse.get_pos()[0]
            mouseOptY = pygame.mouse.get_pos()[1]

            #지뢰 밟기
            if(pygame.mouse.get_pressed()[0]):
                MouseOnMine(mousePosX, mousePosY)

                #리셋버튼
                if ((mouseOptX > resetButton.getPosition()[0] and mouseOptY > resetButton.getPosition()[1])
                        and (mouseOptX < resetButton.getPosition()[0] + resetButton.getSize()[0])
                        and (mouseOptY < resetButton.getPosition()[1] + resetButton.getSize()[1])):
                    # 너비나 높이값이 바뀌면 화면 갱신
                    if newWidth != 0 or newHeight != 0:
                        mineBase.width += newWidth
                        mineBase.height += newHeight
                        screen = pygame.display.set_mode(   #화면 갱신
                            (rectLength * mineBase.width + (mineBase.width-1),
                             rectLength * mineBase.height + (mineBase.height-1) + 50))
                        newWidth = 0
                        newHeight = 0
                    #버튼 위치 갱신
                    resetButton.setPosition(1, rectLength * mineBase.height + mineBase.height)
                    widthVariable.setPosition(115,rectLength * mineBase.height + rectLength - 10)
                    heightVariable.setPosition(115,rectLength * mineBase.height + rectLength + 10)
                    #지뢰수 갱신
                    mineBase.SetMines(mineBase.mines + newMines)
                    newMines = 0
                    #찐 리셋
                    mineBase.ResetGame(mineBase.width, mineBase.height)

                #설정 변경

                #너비 변경
                if ((mouseOptX > widthVariable.getPosition()[0]) and (mouseOptX < widthVariable.getPosition()[0] + widthVariable.sprite_clip.w)
                and (mouseOptY > widthVariable.getPosition()[1]) and (mouseOptY < widthVariable.getPosition()[1] + widthVariable.sprite_clip.h)):
                    newWidth -= 1
                if ((mouseOptX > widthVariable.getPosition()[0] + 115) and (mouseOptX < widthVariable.getPosition()[0] + widthVariable.sprite_clip.w + 115)
                and (mouseOptY > widthVariable.getPosition()[1]) and (mouseOptY < widthVariable.getPosition()[1] + widthVariable.sprite_clip.h)):
                    newWidth += 1
                #높이 변경
                if ((mouseOptX > heightVariable.getPosition()[0]) and (mouseOptX < heightVariable.getPosition()[0] + heightVariable.sprite_clip.w)
                and (mouseOptY > heightVariable.getPosition()[1]) and (mouseOptY < heightVariable.getPosition()[1] + heightVariable.sprite_clip.h)):
                    newHeight = newHeight - 1
                if ((mouseOptX > heightVariable.getPosition()[0] + 115) and (mouseOptX < heightVariable.getPosition()[0] + heightVariable.sprite_clip.w + 115)
                and (mouseOptY > heightVariable.getPosition()[1]) and (mouseOptY < heightVariable.getPosition()[1] + heightVariable.sprite_clip.h)):
                    newHeight = newHeight + 1
                #지뢰수 변경
                if ((mouseOptX > minesVariable.getPosition()[0]) and (mouseOptX < minesVariable.getPosition()[0] + minesVariable.sprite_clip.w)
                and (mouseOptY > minesVariable.getPosition()[1]) and (mouseOptY < minesVariable.getPosition()[1] + minesVariable.sprite_clip.h)):
                    newMines = newMines - 1
                if ((mouseOptX > minesVariable.getPosition()[0] + 115) and (mouseOptX < minesVariable.getPosition()[0] + minesVariable.sprite_clip.w + 115)
                and (mouseOptY > minesVariable.getPosition()[1]) and (mouseOptY < minesVariable.getPosition()[1] + minesVariable.sprite_clip.h)):
                    newMines = newMines + 1

            #깃발 꽂기
            elif(pygame.mouse.get_pressed()[2]):
                if(mousePosX >= 0 and mousePosX < mineBase.width) and (mousePosY >= 0 and mousePosY < mineBase.height):
                    mineBase.ClickSafeMine(mousePosX,mousePosY)

    # 게임 데이터 업데이트
    drawImage()

    # 갱신
    pygame.display.update()

pygame.time.delay(1000)
pygame.quit()