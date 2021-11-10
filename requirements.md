앞으로 진행해야 할 일
====================

## ※ 긴급 공지
board alias 때문에 작업하기 매우 헷갈림

이에 변수명을 수정하였고 board-block branch에서 이를 잘 검토하여 pull하길 바람

## 현재 문제점
board.py에 정의된 class 이름도 Board이고 Board 내에 있는 인스턴스 변수 이름도 board임.

따라서 전자는 그대로 두되 후자의 이름을 block_table로 바꾸는 것을 요청함
- Board -> Board
- Board.board -> Board.block_table

- - -

## Minesweeper v2.0 구현
Reference: Minesweeper Online(https://minesweeper.online/ko/)

# ~~1. 게임판 출력~~

# 2. 좌클릭
## 2.1. 지뢰를 클릭한 경우
게임 패배
## 2.2. 숫자를 클릭한 경우
recursive하게 지뢰가 없는 검증된 칸(?)을 열어야하는데 아직 정확한 메커니즘에 대해 감을 못 잡아서 정확한 확인 필요함

# ~~3. 우클릭~~
깃발 표시 한번더 우클릭하면 깃발 취소

기존 Windows 지뢰찾기에는 ?로 표시하는 기능이 있었던것 같은데 Minesweeper Online 기준으로는 일단 보류

# 4. 좌우 동시클릭(chord)
주위 8칸을 기준으로 표시된 숫자와 깃발 개수가 같으면 해당 칸을 check
## 4.1. 모두 맞게 표시할 경우
깃발을 제외한 나머지 모든 칸을 open(recursively하게 적용)
## 4.2. 하나라도 잘못 표시할 경우
지뢰를 터뜨리고 게임 패배 and 모든 지뢰 위치 표시

# 5. 남은 깃발 수 및 타이머 표시
CLI이기 때문에 console clear를 이용해서 구현하거나 아니면 보류하고 GUI에 넘기기
그리 어렵지는 않을지도?

# 6. 게임 승리 조건
- 모든 지뢰를 맞게 표시한 경우
- 지뢰를 터뜨리지 않고 모든 칸을 연 경우

지뢰찾기 승리 조건은 버전에 따라 다른데 minesweeper online에서는 2의 기준을 따름

# 8. 게임 종료 시 게임 결과와 함께 클릭 수와 소요 시간 출력
Minesweeper Online에서는 3BV(클리어하는데 필요한 최소 클릭 수)와 불필요한 클릭 수까지 체크하는데 이건 너무 어려울것 같아서 포기함

# 10. 기타
지뢰찾기를 성공적으로 모두 구현할 경우 X nimmt!까지 구현해볼 예정