from random import randrange

class MineSweeper:

    area = []
    areaClicked = []    # (0 : 클릭 안함, 1 : 좌클릭, 2 : 우클릭)
    mines = 20
    height = 10
    width = 10
    gameOver = False

    def __init__(self, w, h, m = mines):
        self.gameOver = False
        self.SetMines(m)
        self.ResetGame(w, h)

    #게임 초기화
    def ResetGame(self, w, h):
        self.area = []
        self.areaClicked = []

        self.width = w
        self.height = h
        self.gameOver = False

        #지뢰판 크기 설정
        for i in range(self.height):
            tmp = []
            tmp2 = []
            for j in range(self.width):
                tmp.append(0)
                tmp2.append(0)
            self.area.append(tmp)
            self.areaClicked.append(tmp2)

        # 지뢰 심기 (지뢰 : -1)
        mineCount = self.mines
        while 0 < mineCount:
            x = randrange(0, self.width)
            y = randrange(0, self.height)
            if not (self.area[y][x] == -1):  # 같은자리에 위치하지 않도록 검사
                self.area[y][x] = -1
                mineCount -= 1

        # 숫자로 지뢰 개수 검사
        for i in range(self.height):
            for j in range(self.width):
                if (self.area[i][j] >= 0):  # 지뢰가 없는 자리
                    self.InputMine(j, i)

    # 지뢰 개수 검사
    def InputMine(self, x, y):
        startI = -1
        if y == 0: startI = 0
        endI = 2
        if y == self.height - 1: endI = 1

        startJ = -1
        if x == 0: startJ = 0
        endJ = 2
        if x == self.width - 1: endJ = 1

        for i in range(startI, endI):
            for j in range(startJ, endJ):
                if (self.area[y + i][x + j] == -1):
                    self.area[y][x] += 1

    # 지뢰 개수 설정
    def SetMines(self, m):
        self.mines = m

    # 발판 넓이 설정
    def GetArea(self):
        return self.area
    def GetArea(self, x, y):
        return self.area[y][x]
    def GetGameOver(self):
        return self.gameOver
    def GetAreaClicked(self):
        return self.areaClicked
    def ClickArea(self, x, y):  #발판 클릭
        if(self.areaClicked[y][x] == 0):
            self.areaClicked[y][x] = 1
            #주변에 0이 있다면
            if self.area[y][x] == 0:    #주변의 0을 채우기
                self.FillZeroStep(x, y)
            #지뢰를 밟으면
            if self.area[y][x] == -1: self.gameOver = True
            else: self.gameOver = False

    # 0자리 채우기
    def FillZeroStep(self, x, y):
        if self.areaClicked[y][x - 1] == 0 and x > 0:    #좌축
            self.areaClicked[y][x - 1] = 1
            if self.area[y][x - 1] == 0: self.FillZeroStep(x - 1, y)
        if self.areaClicked[y - 1][x] == 0 and y > 0:    #상단
            self.areaClicked[y - 1][x] = 1
            if self.area[y - 1][x] == 0: self.FillZeroStep(x, y - 1)
        try:
            if self.areaClicked[y][x + 1] == 0 and x < self.width:    #우축
                self.areaClicked[y][x + 1] = 1
                if self.area[y][x + 1] == 0: self.FillZeroStep(x + 1, y)
        except: 1
        try:
            if self.areaClicked[y + 1][x] == 0 and y < self.height:    #하단
                self.areaClicked[y + 1][x] = 1
                if self.area[y + 1][x] == 0: self.FillZeroStep(x, y + 1)
        except: 1
        return

    # 깃발꽂기
    def ClickSafeMine(self, x, y):
        if(self.areaClicked[y][x] == 2):
            self.areaClicked[y][x] = 0
        elif(self.areaClicked[y][x] == 0):
            self.areaClicked[y][x] = 2
