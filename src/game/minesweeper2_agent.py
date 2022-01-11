from collections import deque

from object.board import Board
from object.board import adj_loc
from models.torch.torch_dqn import TorchDQNAgent


class Minesweeper2Agent(Board, TorchDQNAgent):
    """
    지뢰찾기 레벨 선택, 보드 출력, 사용자 입력, 메인 알고리즘, 결과 출력 등 게임에 관한 모든 것을 담당하는 클래스
    """
    def __init__(self, level):
        self.level = level
        self.board_info = {1: (9, 9, 10), 2: (16, 16, 40), 3: (16, 30, 99)}
        self.time = 0
        self.click = 0
        self.reward = 0  # 강화학습용
    
    # def select_level(self):
    #     while True:
    #         try:
    #             level = int(input("Select game level. 1. Beginner 2. Intermediate 3. Expert: "))
    #             if 1 <= level <= 3:
    #                 return level
    #             else:
    #                 raise
    #         except:
    #             os.system('clear')
    #             print("Wrong input.\n")

    def generate_board(self):
        height, width, n_bomb = self.board_info[self.level]
        super(Minesweeper2Agent, self).__init__(height, width, n_bomb)
    
    # def command(self):
    #     while True:
    #         print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
    #         self.display_board()
    #         print("Row: 0 ~ %d Column: 0 ~ %d Action: 1. left click 2. right click 3. chord" % (self.height - 1, self.width - 1))
    #         try:
    #             row, col, act = map(int, input("Enter your input such as 'row column action': ").split())
    #             if 0 <= row < self.height and 0 <= col < self.width and 1 <= act <= 3:
    #                 self.click += 1
    #                 return row, col, act
    #             else:
    #                 raise
    #         except:
    #             # os.system('clear')
    #             print("Wrong input.\n")
    
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
        self.reward -= 100

        # os.system('clear')
        # print("GAME OVER\n")
        # print(("Remaining Flags: %d" % self.remain_flag).ljust(20), "Time: %d\n" % self.time)
        
        # self.display_board_game_over()
        
        # print("Time: %f" % self.time)
        # print("Clicks: %d\n" % self.click)

        # sys.exit(0)  # Force termination
    
    def victory(self):
        self.reward += 100

        # os.system('clear')
        # print("VICTORY!!\n")
        # print(("Remaining Flags: %d" % 0).ljust(20), "Time: %d\n" % self.time)

        # self.display_board_victory()
        
        # print("Time: %f" % self.time)
        # print("Clicks: %d\n" % self.click)

    def run(self):
        """Minesweeper 2 메인 알고리즘"""
        # os.system('clear')
        # print("Minesweeper 2.0\n\nⓒ  2021 Kyeongjin Mun, Seungwon Lee All Rights Reserved.\n")
        # self.level = self.select_level()
        
        self.generate_board()

        # os.system('clear')
        
        # 0-index 사용
        while self.remain_block:
            # state 전처리 필요
            state = None
            act = self.predict(state)
            # row, col, act = self.command()
            # step
            pass
            
            # Should convert act(0 ~ row * col * 3 - 1) to (row, col, cmd)
            # 0 ~ row * col * 3 - 1 사이의 act 값을 (row, col, cmd)로 매핑해줘야함
            # self.convert_act()
            
            cur = self.blocks[row][col]
            
            # 첫 시도에 게임 오버 방지
            if not self.init_loc:
                self.init_loc = (row, col)
                self.randomize_bomb()
                self.calculate_bomb_distance()
            
            """
            여기 밑에 있는 예외 처리 케이스는 실제 강화학습할 때는 의미가 없는 action이라 판단하여 모두 제거 예정
            """
            
            if act == 1:
                # 열린 칸 좌클릭 예외 처리
                if cur.opened:
                    # os.system('clear')
                    # print("You can left click closed block only.\n")
                    continue
                    
                # 깃발 꽂힌 칸 좌클릭 예외 처리
                if cur.flaged:
                    # os.system('clear')
                    # print("You can left click non-flaged block only.\n")
                    continue

                self.left_click(row, col)
            
            elif act == 2:
                # 열린 칸 우클릭 예외 처리
                if cur.opened:
                    # os.system('clear')
                    # print("You can right click closed block only.\n")
                    continue
                self.right_click(row, col)
            
            else:
                # 잠긴 칸 동시클릭 예외 처리
                if not cur.opened:
                    # os.system('clear')
                    # print("You can chord opened block only.\n")
                    continue
                
                # 깃발 숫자와 칸에 적힌 숫자가 다를 때 예외 처리
                if self.count_adj_flag(row, col) != cur.n_adj_bomb:
                    # os.system('clear')
                    # print("You can only chord when the number of flags matches the block number.\n")
                    continue
                
                self.chord(row, col)
            
            # os.system('clear')
            self.reward -= 1
        
        self.victory()