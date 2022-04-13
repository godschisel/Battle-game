import random


def attack():
    return random.randint(5, 10)


class Character:
    def __init__(self) -> None:
        self.points = 0
        self.life = random.randint(10, 20)
        self.start_life = self.life
        self.defense = random.randint(5, 10)

    def make_attack(self, other, bonus_attack = 0):
        result = other.get_hit(attack() + bonus_attack)
        if result:
            self.points += 1
        return result

    def get_hit(self, attack_points):
        diff = self.defense - attack_points
        if diff < 0:
            self.life += diff
            self.points -= 1
            return True
        return False

    def get_points(self):
        return self.points

    def get_life(self):
        return self.life


class Game:
    def __init__(self) -> None:
        self.character = Character()
        self.name = ''
        self.intro()
        self.opponent = Character()
        print('-' * 10)
        self.print_opponent_stats('intro')
        print('-' * 10)
        print()

        character_status = 0
        opponent_status = 0
        o_no_change = 0
        ch_no_change = 0
        both_no_change = 0
        o_winning = 0
        bonus_attack = 0

        while self.opponent.get_life() > 0 and self.character.get_life() > 0:
            if self.opponent.get_life() <= 0:
                print('YOU WIN!')
            if self.character.get_life() <= 0:
                print("YOU ARE DEFEATED!")

            o_s = opponent_status
            ch_s = character_status
            input('Make a move!')
            character_status += self.character_attack(bonus_attack)
            input('Cover yourself!')
            opponent_status += self.opponent_attack()
            print()
            if o_s == opponent_status:
                o_no_change += 1

            if ch_s == character_status:
                ch_no_change += 1

            if o_s == opponent_status and ch_s == character_status:
                both_no_change += 1
            else:
                both_no_change = 0

            if opponent_status == o_s + 1 and ch_s == character_status:
                o_winning  += 1
            else:
                o_winning = 0


            change_offset = 2

            # if char and opponent both missed attack 'change-offset'-times
            if both_no_change > change_offset:
                attack_change = 4
                life_change = 2
                inp = input(f'This is taking too long! Do you want to make a risky maneuver? (+{attack_change} attack, '
                            f'-{life_change} life) \nY/N? ')

                if inp.lower() == 'y' or inp.lower() == '':     # y, Y, ENTER
                    character_status = 0
                    opponent_status = 0

                    ch_no_change = 0
                    o_no_change = 0

                    both_no_change = 0
                    o_winning = 0

                    start_life = self.character.start_life
                    self.character.life -= life_change
                    life = self.character.get_life()
                    print(f'Your life is: {life}/{start_life}.')
                    bonus_attack = attack_change
                    print()
                else:
                    print('Nevermind... I want to beat him with my honor.')

            # if opponent is successful and char is missing attacks

            elif o_winning > change_offset:
                print(f'{both_no_change}, {(change_offset + 1)}, {o_no_change}, {ch_no_change}, {change_offset}; {opponent_status}')
                # todo: if Y then +5 life to next fight
                inp = input('Your opponent seem to be too strong. Yield? (Y/N)')
                if inp.lower() == 'y' or inp.lower() == '':  # y, Y, ENTER
                    break
                else:
                    print('You are suddenly filled with godly courage. (+5 defense) ')
                    self.character.defense += 5
                    character_status = 0
                    opponent_status = 0

                    ch_no_change = 0
                    o_no_change = 0

                    both_no_change = 0
                    o_winning = 0
            else:
                bonus_attack = 0
        self.outro()

    def opponent_attack(self):
        start_life = self.character.start_life
        life_before = self.character.get_life()
        result = self.opponent.make_attack(self.character)
        if result:
            life = self.character.get_life()
            if life > 0:
                print(f'Opponent attacked you for {life_before - life} points. Your life is: {life}/{start_life}.')
            elif life == 0:
                print(f'Opponent attacked you for {life_before - life} points. Your life is: 0/{start_life}. You are '
                      f'dead.')
            else:
                print(f'Opponent attacked you for {life_before - life} points. Your life is: 0/{start_life}. He '
                      f'destroyed you. You are dead.')
            return 1
        else:
            print('He missed.')
            return 0

    def character_attack(self, bonus_attack):
        life_before = self.opponent.get_life()
        result = self.character.make_attack(self.opponent, bonus_attack)
        if result:
            print(f'You hit him for {life_before - self.opponent.get_life()}.')
            return 1
        else:
            print('You missed :( ')
            return 0

    def print_my_stats(self):
        start_life = self.character.start_life
        defense = self.character.defense
        life = self.character.get_life()
        name = self.name
        print(f'{name}: Life:{life}/{start_life}, Defense:{defense}')

    def stat_lower_higher(self, stat1, stat2):
        stat3 = 'same'
        if stat1 < stat2:
            stat3 = 'higher'
        if stat1 > stat2:
            stat3 = 'lower'
        return stat3

    def print_opponent_stats(self,io):
        defense = self.opponent.defense
        life = self.opponent.get_life()
        character_life = self.character.get_life()
        character_defense = self.character.defense
        opponent_defense = self.stat_lower_higher(character_defense, defense)
        opponent_life = self.stat_lower_higher(character_life, life)
        if io == 'intro':
            print(f'YOUR OPPONENT has {opponent_life} life than you and defense {opponent_defense} than you.')
        if io == 'outro':
            print(f'YOUR OPPONENT: Life:{life}, Defense:{defense}')

    def intro(self):
        print("Welcome to battle arena.")
        self.name = input("What is your name?\n")
        self.print_my_stats()

    def outro(self):
        print('-' * 10)
        self.print_my_stats()
        print('-' * 10)
        self.print_opponent_stats('outro')
        print('-' * 10)
        print('GAME OVER')


if __name__ == "__main__":
    g = Game()
