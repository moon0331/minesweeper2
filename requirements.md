앞으로 진행해야 할 일
====================

## Minesweeper v2.0 구현
Reference: https://minesweeper.online/ko/

# 1. 게임판 출력(완료)

# 2. 좌클릭
## 2.1. 지뢰를 클릭한 경우
게임 패배
## 2.2. 숫자를 클릭한 경우
recursive하게 지뢰가 없는 검증된 칸(?)을 열어야하는데 아직 정확한 메커니즘에 대해 감을 못 잡아서 정확한 확인 필요함

# 3. 우클릭
깃발 표시 한번더 우클릭하면 깃발 취소

기존 Windows 지뢰찾기에는 ?로 표시하는 기능이 있었던것 같은데 일단은 보류

# 4. 좌우 동시클릭(chord)
주위 8칸을 기준으로 표시된 숫자와 깃발 개수가 같으면 해당 칸을 check
## 4.1. 모두 맞게 표시할 경우
깃발을 제외한 나머지 모든 칸을 open
## 4.2. 하나라도 잘못 표시할 경우
지뢰를 터뜨리고 게임 패배

# 5. 지뢰를 터뜨려서 게임이 종료될 경우 해당 게임에서의 모든 지뢰 위치를 표시함
print_board 함수 불러와서 적절히 처리하면 되니깐 별로 어려운건 없어보임

# 6. 남은 깃발 수 및 타이머 표시
CLI이기 때문에 console clear를 이용해서 구현하거나 아니면 보류하고 GUI에 넘기기

# 7. 모든 지뢰를 맞게 표시한 경우 게임 승리
또는 모든 칸을 다 연 경우? 이건 버전에 따라 다름 확인 요망 

# 8. 게임 종료 시 게임 결과와 함께 클릭 수와 소요 시간 출력
minesweeper.online에서는 불필요한 클릭 수까지 체크하는데 이건 너무 어려울것 같아서 포기함

# 9. 기타
지뢰찾기를 성공적으로 모두 구현할 경우 X nimmt!까지 구현해볼 예정