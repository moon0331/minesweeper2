"""
Minesweeper2Agent 테스트 파일

주석을 모두 한글로 바꿨기 때문에 출력문 또한 한글로 바꿀 예정
"""

import os
import sys
from collections import deque
from random import randint


def adj_loc(x, y, xmax, ymax):
    adj_loc = [
        (x-1, y-1), (x-1, y),   (x-1, y+1),
        (x,   y-1),             (x,   y+1),
        (x+1, y-1), (x+1, y),   (x+1, y+1)
    ]

    for x, y in adj_loc:
        if 0<=x<xmax and 0<=y<ymax:
            yield x, y


class Board:
    # size를 height, width로 분리
    def __init__(self, height, width, n_bomb):
        self.height = height
        self.width = width
        self.n_bomb = n_bomb

        self.bomb_loc = set()
        self.blocks = None
        self.init_loc = None

        self.miss_block = None

        self.remain_flag = n_bomb  # 남은 깃발 수는 폭탄 수에서부터 시작되며 0보다 작아질 수 있음
        self.remain_block = height * width - n_bomb  # 남은 블럭 수가 0이 되면 승리
        
        self._generate() # 보드 생성

    def randomize_bomb(self):
        self.bomb_loc = set()
        while len(self.bomb_loc) < self.n_bomb:
            x = randint(0, self.height - 1)
            y = randint(0, self.width - 1)
            if (x, y) != self.init_loc:
                self.bomb_loc.add((x, y))
        
        for r, c in self.bomb_loc:
            self.blocks[r][c]._set_bomb()

    def _generate(self):
        height, width = self.height, self.width
        self.blocks = [[Block((row, col)) for col in range(width)] for row in range(height)]

    def calculate_bomb_distance(self):
        height, width = self.height, self.width
        bomb_distance = [[0 for _ in range(width)] for _ in range(height)]
        for r, c in self.bomb_loc:
            for adj_r, adj_c in adj_loc(r, c, height, width):
                bomb_distance[adj_r][adj_c] += 1

        for r in range(height):
            for c in range(width):
                self.blocks[r][c].n_adj_bomb = bomb_distance[r][c]

    def display_board(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                print(cur.mark, end=' ')
            print()
        print()

    def display_board_game_over(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                if cur.flaged:
                    print("▶", end=' ') if cur.has_bomb else print("X", end=' ')
                else:
                    if cur == self.miss_block:
                        print("!", end=' ')
                    else:
                        print("*", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()

    def display_board_victory(self):
        print(' ', end=' ')
        for i in range(self.width):
            print("%d" % i, end=' ')
        print()

        for row in range(self.height):
            print("%d" % row, end=' ')
            for col in range(self.width):
                cur = self.blocks[row][col]
                print("▶", end=' ') if cur.has_bomb else print(cur.mark, end=' ')
            print()
        print()


class Block:

    def __init__(self, loc, has_bomb=False):
        self.loc = loc
        self.has_bomb = has_bomb
        self.n_adj_bomb = 0
        self.selected = False

        self.opened = False
        self.flaged = False
        self.mark = '■'

    def _set_bomb(self):
        self.has_bomb = True


class Minesweeper2Agent(Board):
    """
    지뢰찾기 레벨 선택, 보드 출력, 사용자 입력, 메인 알고리즘, 결과 출력 등 게임에 관한 모든 것을 담당하는 클래스
    """
    def __init__(self, level=1):
        self.level = level
        self.board_info = {1: (9, 9, 10), 2: (16, 16, 40), 3: (16, 30, 99)}
        self.time = 0
        self.click = 0
    
    def select_level(self):
        while True:
            try:
                level = int(input("Select game level. 1. Beginner 2. Intermediate 3. Expert: "))
                if 1 <= level <= 3:
                    return level
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input.\n")

    def generate_board(self):
        height, width, n_bomb = self.board_info[self.level]
        super(Minesweeper2Agent, self).__init__(height, width, n_bomb)
    
    def command(self):
        while True:
            print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
            self.display_board()
            print("Row: 0 ~ %d Column: 0 ~ %d Action: 1. left click 2. right click 3. chord" % (self.height - 1, self.width - 1))
            try:
                row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
                if 0 <= row < self.height and 0 <= col < self.width and 1 <= act <= 3:
                    self.click += 1
                    return row, col, act
                else:
                    raise
            except:
                os.system('clear')
                print("Wrong input.\n")
    
    def count_adj_flag(self, row, col):
        adj_flag = 0
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            if self.blocks[adj_r][adj_c].flaged:
                adj_flag += 1
        return adj_flag

    def left_click(self, row, col):
        cur = self.blocks[row][col]
        if cur.has_bomb:
            self.miss_block = cur
            self.game_over()
        
        else:
            q = deque([(row, col)])
            vis = [[0] * self.width for _ in range(self.height)]
            vis[row][col] = 1

            while q:
                r, c = q.popleft()
                cur = self.blocks[r][c]
                
                if not cur.opened:
                    cur.opened = True
                    cur.mark = '%d' % cur.n_adj_bomb if cur.n_adj_bomb else '□'
                    self.remain_block -= 1
                
                if not self.blocks[r][c].n_adj_bomb:
                    for adj_r, adj_c in adj_loc(r, c, self.height, self.width):
                        if not vis[adj_r][adj_c]:
                            q.append((adj_r, adj_c))
                            vis[adj_r][adj_c] = 1

    def right_click(self, row, col):
        cur = self.blocks[row][col]
        cur.flaged = not cur.flaged

        if cur.flaged:
            self.remain_flag -= 1
            cur.mark = '▶'
        else:
            self.remain_flag += 1
            cur.mark = '■'
    
    def chord(self, row, col):
        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            cur = self.blocks[adj_r][adj_c]
            if cur.has_bomb != cur.flaged:
                self.miss_block = cur
                self.game_over()

        for adj_r, adj_c in adj_loc(row, col, self.height, self.width):
            cur = self.blocks[adj_r][adj_c]
            if not cur.flaged and not cur.opened:
                self.left_click(adj_r, adj_c)
    
    def game_over(self):
        os.system('clear')
        print("GAME OVER\n")
        print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
        
        self.display_board_game_over()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

        sys.exit(0)  # 게임 오버 시 run 함수 강제 종료
    
    def victory(self):
        os.system('clear')
        print("VICTORY!!\n")
        print(("Remaining Flags: %d" % 0).ljust(20), "Time: %d\n" % self.time)

        self.display_board_victory()
        
        print("Time: %f" % self.time)
        print("Clicks: %d\n" % self.click)

    def run(self):
        """Minesweeper 2 메인 알고리즘"""
        os.system('clear')
        print("Minesweeper 2.0\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        self.level = self.select_level()
        self.generate_board()
        os.system('clear')
        
        # 0-index
        while self.remain_block:
            row, col, act = self.command()
            cur = self.blocks[row][col]
            
            # 첫 시도 게임 오버 방지
            if not self.init_loc:
                self.init_loc = (row, col)
                self.randomize_bomb()
                self.calculate_bomb_distance()
            
            if act == 1:
                # 열린 칸 좌클릭 예외 처리
                if cur.opened:
                    os.system('clear')
                    print("You can left click closed block only.\n")
                    continue
                    
                # 깃발 꽂힌 칸 좌클릭 예외 처리
                if cur.flaged:
                    os.system('clear')
                    print("You can left click non-flaged block only.\n")
                    continue

                self.left_click(row, col)
            
            elif act == 2:
                # 열린 칸 우클릭 예외 처리
                if cur.opened:
                    os.system('clear')
                    print("You can right click closed block only.\n")
                    continue
                self.right_click(row, col)
            
            else:
                # 잠긴 칸 동시클릭 예외 처리
                if not cur.opened:
                    os.system('clear')
                    print("You can chord opened block only.\n")
                    continue
                
                # 깃발 숫자와 칸에 적힌 숫자가 다를 때 예외 처리
                if self.count_adj_flag(row, col) != cur.n_adj_bomb:
                    os.system('clear')
                    print("You can only chord when the number of flags matches the block number.\n")
                    continue
                
                self.chord(row, col)
            
            os.system('clear')
        
        self.victory()


if __name__ == '__main__':
    minesweeper2_agent = Minesweeper2Agent()
    minesweeper2_agent.run()