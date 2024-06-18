import random
from prettytable import PrettyTable

class Player:
    def __init__(self, name, chips):
        self.name = name  # 플레이어 이름
        self.chips = chips  # 플레이어가 가진 칩 수
        self.visible_card = None  # 플레이어가 볼 수 있는 카드
        self.hidden_card = None  # 플레이어가 볼 수 없는 카드
        self.bet = 0  # 플레이어의 배팅 금액

    def place_bet(self):
        while True:
            try:
                bet = int(input(f"{self.name}플레이어님, {self.chips}만큼의 칩을 가지고 있습니다. 배팅 금액: "))
                if 0 < bet <= self.chips:
                    self.bet = bet  # 배팅 금액 설정
                    self.chips -= bet  # 칩에서 배팅 금액만큼 차감
                    break
                else:
                    print("올바른 배팅 금액이 아닙니다. 소유하고 있는 금액 내에서 배팅하세요")
            except ValueError:
                print("올바른 type을 입력하세요.")

    def receive_cards(self, visible_card, hidden_card):
        self.visible_card = visible_card  # 볼 수 있는 카드 받기
        self.hidden_card = hidden_card  # 볼 수 없는 카드 받기

    def reveal_cards(self):
        print(f"{self.name}'s visible card: {self.visible_card}, hidden card: {self.hidden_card}")  # 카드 공개

    def total_card_value(self):
        return self.visible_card + self.hidden_card  # 카드 합산 값 반환

def deal_cards(deck, players):
    random.shuffle(deck)  # 덱 섞기
    for player in players:
        visible_card = deck.pop()  # 볼 수 있는 카드
        hidden_card = deck.pop()  # 볼 수 없는 카드
        player.receive_cards(visible_card, hidden_card)  # 카드 나눠주기

def determine_winner(players):
    highest_value = -1  # 최고 카드 값 초기화
    winners = []
    for player in players:
        total_value = player.total_card_value()
        # 새로운 최고 카드 값을 가진 플레이어로 리스트 업데이트
        if total_value > highest_value:
            highest_value = total_value
            winners = [player]
        # 최고 카드 값이 같은 플레이어 추가
        elif total_value == highest_value:
            winners.append(player)
    return winners

def display_game_state(players, round_number):
    table = PrettyTable()
    table.field_names = ["Player", "Chips", "Bet", "Visible Card", "Hidden Card"]
    for player in players:
        table.add_row([player.name, player.chips, player.bet, player.visible_card, "Hidden" if player.hidden_card is not None else ""])
    print(f"\nRound {round_number}")
    print(table)

def reveal_other_players_visible_cards(players, current_player):
    other_players_cards = ', '.join(f"{p.name}: {p.visible_card}" for p in players if p != current_player)
    print(f"{current_player.name} sees other players' visible cards: {other_players_cards}")

def main():
    deck = list(range(1, 14)) * 4  # 카드 덱 생성 (1부터 13까지의 숫자 카드 4세트)
    
    while True:
        try:
            num_players = int(input("플레이할 인원 수를 입력하세요: "))
            if num_players > 1:
                break
            else:
                print("최소 2명 이상의 플레이어가 참여해야합니다.")
        except ValueError:
            print("올바른 type을 입력하세요.")
    
    # 플레이어 객체를 생성하고 초기 칩 수를 100으로 설정
    players = [Player(f"Player {i+1}", 100) for i in range(num_players)]
    
    round_number = 1
    
    while all(player.chips > 0 for player in players):  # 모든 플레이어가 칩을 가지고 있는 동안 게임 진행
        deal_cards(deck, players)
        
        display_game_state(players, round_number)  # 현재 상태 표시
        
        for player in players:
            reveal = input(f"{player.name}님, 상대의 카드를 보려면 'r'을 입력하세요: ")
            if reveal.lower() == 'r':
                reveal_other_players_visible_cards(players, player)
        
        for player in players:
            player.place_bet()  # 각 플레이어 배팅
        
        display_game_state(players, round_number)  # 배팅 후 상태 표시
        
        for player in players:
            player.reveal_cards()  # 카드 공개
        
        winners = determine_winner(players)  # 승자 결정
        
        if len(winners) == 1:
            winner = winners[0]
            pot = sum(player.bet for player in players)  # 모든 배팅 금액 합산
            winner.chips += pot  # 승자가 모든 배팅 금액 가져가기
            print(f"{winner.name} wins the round and takes the pot of {pot} chips!")
        else:
            print("It's a tie! No chips are exchanged.")
            for player in players:
                player.chips += player.bet  # 배팅 금액 돌려주기
        
        for player in players:
            player.bet = 0  # 배팅 금액 초기화

        round_number += 1
    
    winners = [player for player in players if player.chips > 0]
    if len(winners) == 1:
        print(f"\n{winners[0].name} wins the game!")  # 최종 승자 출력
    else:
        print("\nIt's a tie among the remaining players!")  # 무승부 출력

# 메인 함수 실행
if __name__ == "__main__":
    main()