import random

from prettytable import PrettyTable

class Player:
    def __init__(self, name, chips):
        self.name = name # 플레이어 이름
        self.chips = chips # 플레이어가 가진 칩 수
        self.card = None #플레이어의 카드
        self.bet = 0 # 플레이어의 배팅 금액

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"{self.name}플레이어님, {self.chips}만큼의 칩을 가지고 있습니다. 배팅 금액: "))
                if 0 < bet <= self.chips:
                    self.bet = bet # 배팅 금액 설정
                    self.chips -= bet # 칩에서 배팅 금액만큼 차감
                    break
                else:
                    print("올바른 배팅 금액이 아닙니다. 소유하고 있는 금액 내에서 배팅하세요")
            except ValueError:
                print("올바른 type을 입력하세요.")

    
    def receive_card(self, card):
        self.card = card # 카드 받기

   
    def reveal_card(self):
        print(f"{self.name}'s card: {self.card}") #카드 공개


def deal_cards(deck, players):
    random.shuffle(deck) # 덱 섞기
    for player in players:
        player.receive_card(deck.pop()) # 각 플레이어에게 카드 한 장씩 나눠주기

def determine_winner(players):
    highest_card = -1 # 최고 카드 초기화
    winners = []
    for player in players:
        
        # 새로운 최고 카드를 가진 플레이어로 리스트 업데이트
        if player.card > highest_card:
            highest_card = player.card
            winners = [player]
            
        # 최고 카드가 같은 플레이어 추가
        elif player.card == highest_card:
            winners.append(player)
    return winners


def display_game_state(players, round_number):
    table = PrettyTable() 
    table.field_names = ["Player", "Chips", "Bet", "Card"] 
    for player in players:
        table.add_row([player.name, player.chips, player.bet, player.card if player.card is not None else "Hidden"])
    print(f"\nRound {round_number}") 
    print(table) 


def main():
    deck = list(range(1, 14)) # 카드 덱 생성 (1부터 13까지의 숫자 카드)
    
    while True:
        try:
            num_players = int(input("플레이할 인원 수를 입력하세요: "))
            if num_players > 1:
                break
            else:
                print("최소 2명 이상의 플레이어가 참여해야합니다.")
        except ValueError:
            print("올바른 type을 입력하세요.")
    
    # 플레이어 생성
    players = [Player(f"Player {i+1}", 100) for i in range(num_players)]
    
    round_number = 1
    
    while all(player.chips > 0 for player in players): # 모든 플레이어가 칩을 가지고 있는 동안 게임 진행
        
        deal_cards(deck, players)
        
        display_game_state(players, round_number) # 현재 상태 표시
 
        for i, player in enumerate(players):
            other_players_cards = ', '.join(f"{p.name}: {p.card}" for j, p in enumerate(players) if i != j)
            print(f"{player.name} sees other players' cards: {other_players_cards}")
        
        for player in players:
            player.place_bet() # 각 플레이어 배팅
        
        display_game_state(players, round_number) # 배팅 후 상태 표시
        
       
        for player in players:
            player.reveal_card() # 카드 공개
        
        
        winners = determine_winner(players) # 승자 결정
        
        if len(winners) == 1:
            winner = winners[0]
            pot = sum(player.bet for player in players) # 모든 배팅 금액 합산
            winner.chips += pot # 승자가 모든 배팅 금액 가져가기
            print(f"{winner.name} wins the round and takes the pot of {pot} chips!")
        else:
            print("It's a tie! No chips are exchanged.")
            for player in players:
                player.chips += player.bet # 배팅 금액 돌려주기
        
     
        for player in players:
            player.bet = 0 # 배팅 금액 초기화

        round_number += 1
    
   
    winners = [player for player in players if player.chips > 0]
    if len(winners) == 1:
        print(f"\n{winners[0].name} wins the game!") # 최종 승자 출력
    else:
        print("\nIt's a tie among the remaining players!") # 무승부 출력

# 메인 함수 실행
if __name__ == "__main__":
    main()