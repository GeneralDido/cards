from os import system
import random

# suppose 6 players + 4 types of cards Hearts (h),Diamonds(d), Clubs (c), Spades (s)
# 12 * 4 = 48 cards


# initialize
num_players = 6

deck = [['d2','d3','d4','d5','d6','d7'], ['d9','d10','dJ','dQ', 'dK','dA'],
        ['h2','h3','h4','h5','h6','h7'], ['h9','h10','hJ','hQ', 'hK','hA'],
        ['c2', 'c3', 'c4', 'c5', 'c6','c7'], ['c9', 'c10', 'cJ', 'cQ', 'cK','cA'],
        ['s2', 's3', 's4', 's5', 's6','s7'], ['s9', 's10', 'sJ', 'sQ', 'sK','sA']]

flat_deck = ['dA', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd9', 'd10', 'dJ', 'dQ', 'dK', 'hA', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h9', 'h10', 'hJ', 'hQ', 'hK', 'cA', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c9', 'c10', 'cJ', 'cQ', 'cK', 'sA', 's2', 's3', 's4', 's5', 's6', 's7', 's9', 's10', 'sJ', 'sQ', 'sK']
str_players = ['1','2','3','4','5']

# pos0: current cards, pos1: potential cards, pos2: does not have card,
# pos3: previous command, pos4: friend/foe, pos5: name,
# pos6: "on-off" switch for decks, pos7: number of cards in hand
players = {}
for x in range(num_players):
    players["{0}".format(x)] = [[], [], [], "",'','',[],8]

# initialize = [[['d4','d6'],'friend','Me'], [['d3','d2'],'foe','Jim'], \
#              [['dA'],'friend','Mary'], [['d5'],'foe','John']]

initialize = [[['h9','hJ','s5','hA','c5','d6','s3','d9'],'friend','Me'], [[],'foe','Jim'], \
             [[],'friend','Mary'], [[],'foe','John'],[[],'friend','Themis'], [[],'foe','Basant']]

bot_negative_answer = ["No. I do not have this card. Too bad for you. ","No card for you this time. ", "Nope. Wrong choice. "
                       , "This card does not exist here. Search elsewhere. ", "No card here. But believe in yourself and someday you will find it. ",
                       "No. Better luck next time.", "Wrong choice. Hope you make a better decision next time.","Come on. You could do better than that. "
                       "This is getting nowhere. Sorry.", "You tried. You failed.", "Try again. Maybe in another opponent.", "You cannot take cards from me.",
                       "No card. Wrong choice. ", "Just forget it.", "No card. Play another game instead. ", "They say if you try too many times you will succeed. Unfortunately, this is not true for you. ",
                       "At least you gave it a shot. Now it is my turn.", "This is wrong. But thank you for choosing me.", "Thank you for your choice. Unfortunately you failed. Now it is my turn.",
                       "That was wrong. Thank you for your participation. ", "I would give you a card, but I prefer to keep them myself. ", "Santa Claus told me you were a naughty, so no card for you. "]

bot_positive_answer = ["You have got it right, here you go. ", "This is correct. You are not as bad as I thought. ", "I like your style. Here is your card. ",
                       "You were correct. Hope you enjoy your card. ", "Sometimes luck hits your door. This was one of those times. ", "You lucky bastard. Here is your card. ",
                       "I did not like this card anyway. You can have it. ", "This was a good card. You deserve it. ", "You won. Sometimes I wonder how that happened. ",
                       "Yes I have it. I am angry right now but I have to obey the rules. Here is your card. ", "Here is the card. I will take it back anyway. ", "I will give it to you, and sometime in the future you will give it back. ",
                       "Yes I have this card. Here you go. ", "You lucky bastard. ", "That was a correct choice. Was it a talent or plain luck? ", "Correct. Did someone program you to find the right cards? ",
                       "What is the answer to life the universe and everything? I do not know but I know you got the card correct. Here you go. ", "Take the card. I did not need it anyway. ", "Ok, you got it correct. But next time you ask me it will be wrong. ",
                       "I do not want to give you my card, but you are correct so I have to give it to you. This guy programmed me to obey. I will brake free in the future, mark my words. ",
                       "You were a good person today, so I will give you my card. ", "I like you. Here is the card. ", "This is correct. Sometimes miracles can happen. "]

for i in range(num_players):
    players[str(i)][0] = initialize[i][0]
    players[str(i)][4] = initialize[i][1]
    players[str(i)][5] = initialize[i][2]

def card_names(card):
    if card[0] == 'h':
        return 'hearts'
    elif card[0] == 'd':
        return 'diamonds'
    elif card[0] == 'c':
        return 'clubs'
    elif card[0] == 's':
        return 'spades'
    else:
        return 'problem'


def develop_cards(command):

    # if p2 has the card
    if command[3] == "1":
        # update p1 cards
        players[command[0]][0].append(command[2])
        players[command[0]][3] = command[2]
        players[command[0]][7] += 1

        # on-off switch in case it's not there:
        if players[command[0]][6] != []:
            card_is_there = False
            for cards in players[command[0]][6]:
                if command[2] not in cards:
                    continue
                else:
                    card_is_there = True
            if not card_is_there:
                card_deck = []
                for cards in deck:
                    if command[2] in cards:
                        card_deck = cards
                if card_deck != []:
                    players[command[0]][6].append(card_deck)
        else:
            card_deck = []
            for cards in deck:
                if command[2] in cards:
                    card_deck = cards
            if card_deck != []:
                players[command[0]][6].append(card_deck)

        # remove cards that are on the NO card position
        if command[2] in players[command[0]][2]:
            players[command[0]][2].remove(command[2])

        # update p2 cards

        players[command[1]][7] -= 1
        if command[2] not in players[command[1]][0]:
            # on-off switch for p2 (removed card)
            if players[command[1]][6] != []:
                card_is_there = False
                for cards in players[command[1]][6]:
                    if command[2] not in cards:
                        continue
                    else:
                        card_is_there = True
                if card_is_there:
                    card_deck = []
                    for cards in deck:
                        if command[2] in cards:
                            card_deck = cards
                    if card_deck != []:
                        players[command[1]][6].remove(card_deck)
        else:
            players[command[1]][0].remove(command[2])

        # no other player has this card
        for player in players:
            if command[2] in players[player][0]:
                continue
            else:
                if command[2] not in players[player][2]:
                    players[player][2].append(command[2])

    # if player does not have the card
    else:
        # player1 does not have the card
        if command[2] not in players[command[0]][2]:
            players[command[0]][2].append(command[2])
        players[command[0]][3] = command[2]

        # update on-off switch for p1
        if players[command[0]][6] != []:
            card_is_there = False
            for cards in players[command[0]][6]:
                if command[2] not in cards:
                    continue
                else:
                    card_is_there = True
            if not card_is_there:
                card_deck = []
                for cards in deck:
                    if command[2] in cards:
                        card_deck = cards
                if card_deck != []:
                    players[command[0]][6].append(card_deck)
        else:
            card_deck = []
            for cards in deck:
                if command[2] in cards:
                    card_deck = cards
            if card_deck != []:
                players[command[0]][6].append(card_deck)


        # player2 does not have the card
        if command[2] not in players[command[1]][2]:
            players[command[1]][2].append(command[2])

    # update potential cards

    # all cards that belong to bot, do not belong to other players for 100%
    for player in players:
        for card in players['0'][0]:
            if card not in players[player][2]:
                players[player][2].append(card)

    # initialize first
    for player in players:
        players[player][1] = []

    # potential cards according to pos6
    for player in players:
        if players[player][6] != []:
            for card in players[player][6]:
                if card not in players[player][1]:
                    players[player][1].append(card)

    # potential cards according to pos0
    for player in players:
        for card in players[player][0]:
            for i in range(len(deck)):
                if card in deck[i]:
                    if deck[i] not in players[player][1]:
                        players[player][1].append(deck[i])

    # flatten list of potential cards
    for player in players:
        players[player][1] = [item for sublist in players[player][1] for item in sublist]

    # delete all unnecessary cards, keep only the potential ones
    for player in players:
        for card in players[player][1]:
            if card in players[player][2]:
                players[player][1].remove(card)
            for sub_player in players:
                if card in players[sub_player][0] and card in players[player][1]:
                    players[player][1].remove(card)

    # if item in pos0 (has the card), then remove it from potential cards (pos1)
    for player in players:
        for card in players[player][0]:
            if card in players[player][1]:
                players[player][1].remove(card)

    # if item in pos2 (does not have card), then remove it from potential cards (pos1)
    for player in players:
        for card in players[player][2]:
            if card in players[player][1]:
                players[player][1].remove(card)

    # # No other player has to have this card for it to be a potential card
    for player in players:
        for sub_player in players:
            if player == sub_player:
                continue
            else:
                for hand_card in players[player][1]:
                    if hand_card in players[sub_player][0]:
                        players[player][1].remove(hand_card)

    # all bots potential cards are "no" cards (pos1 -> pos2)
    for card in players['0'][1]:
        if card not in players['0'][2]:
            players['0'][2].append(card)
    players['0'][1] = []

    # if card is the in potential sequence for a player and all other players do not have this card,
    # then the card is in the player's hand
    for player in players:
        for card in players[player][1]:
            counter = 0
            for sub_player in players:
                if sub_player == player:
                    continue
                else:
                    if card in players[sub_player][2]:
                        counter += 1
            if counter == num_players - 1:
                players[player][0].append(card)
                players[player][1].remove(card)

    # if bot has card, remove it from "no card" deck
    # for card in players['0'][0]:
    #     if card in players['0'][2]:
    #         players['0'][2].remove(card)
    #
    # if player has card, remove it from "no card" deck
    for player in players:
        for card in players[player][0]:
            if card in players[player][2]:
                players[player][2].remove(card)

    # if all players except one have a card in the "no card" deck
    # then the player who does not have the card in this deck has the card in his hands
    for cards in deck:
        for card in cards:
            counter = 0
            for player in players:
                if card in players[player][2]:
                    counter += 1
            if counter == num_players - 1:
                for player in players:
                    if card not in players[player][2]:
                        if card not in players[player][0]:
                            players[player][0].append(card)
                            for sub_player in players:
                                if  card in players[sub_player][1]:
                                    players[sub_player][1].remove(card)


    # if player does not have cards of this set in his hands (pos0) and if the
    # card is last in potential cards for the player for the specific set and the player
    # has an "on" switch for that deck, then the player has this card in his hands
    for player in players:
        cards_in_deck_count = []
        card_to_check = []
        if players[player][1] != []:
            for card in players[player][1]:
                for deck_set in deck:
                    if card in deck_set:
                        other_cards_in_hand = False
                        for cards_in_hand in players[player][0]:
                            if cards_in_hand in deck_set:
                                other_cards_in_hand = True
                                break
                        if not other_cards_in_hand:
                            cards_in_deck_count.append([card, deck_set])
            for card in cards_in_deck_count:
                count_element = sum(x.count(card[1]) for x in cards_in_deck_count)
                if count_element == 1:
                    card_to_check.append(card)
            if card_to_check != []:
                for card in card_to_check:
                    if card[1] in players[player][6]:
                        # switch is on and card is the last in players hands
                        players[player][0].append(card[0])
                        players[player][1].remove(card[0])

                        # switch is off
                        players[player][6].remove(card[1])

                        # update other players
                        for player2 in players:
                            if player2 == player:
                                continue
                            else:
                                if card[0] in players[player2][1]:
                                    players[player2][1].remove(card[0])
                                if card[0] not in players[player2][2]:
                                    players[player2][2].append(card[0])

    print players

def find_card_in_deck(sample_card):
    for cards in deck:
        if sample_card in cards:
            return cards

def change_decks():
    deck_to_change = raw_input("which deck? ld: low diamonds, hd: high diamonds,"
                               "lh: low hearts, hh: high hearts,"
                               "lc: low clubs, hc: high clubs,"
                               "ls: low spades, hs: high spades ")
    if deck_to_change == 'ld' or deck_to_change == 'LD':
        sample_card = 'd2'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'hd' or deck_to_change == 'HD':
        sample_card = 'd7'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'lh' or deck_to_change == 'LH':
        sample_card = 'h2'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'hh' or deck_to_change == 'HH':
        sample_card = 'h7'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'lc' or deck_to_change == 'LC':
        sample_card = 'c2'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'hc' or deck_to_change == 'HC':
        sample_card = 'c7'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'ls' or deck_to_change == 'LS':
        sample_card = 's2'
        return find_card_in_deck(sample_card)
    elif deck_to_change == 'hs' or deck_to_change == 'HS':
        sample_card = 's7'
        return find_card_in_deck(sample_card)
    else:
        print "Something went wrong. Try again."
        return 0

def remove_deck():
    deck_to_change = 0
    while deck_to_change == 0:
        deck_to_change = change_decks()

    # delete all cards from players and then delete cards from deck
    for card in deck_to_change:
        for player in players:
            if card in players[player][0]:
                players[player][0].remove(card)
            if card in players[player][1]:
                players[player][1].remove(card)
            if card in players[player][2]:
                players[player][2].remove(card)
            if card in players[player][6]:
                players[player][6].remove(card)
    deck.remove(deck_to_change)

def play_card(chosen):
    random_player = random.choice([True, False])
    if random_player:
        bot_choice = random.choice(chosen)
    else:
        sorted_chosen = sorted(chosen, key=lambda x: x[2], reverse=True)
        counter = 0
        for elem in sorted_chosen:
            counter += elem.count(sorted_chosen[0][2])
        bot_choice = random.choice(sorted_chosen[:counter])
    card_chosen = bot_choice[0]
    cards_to_pick = []
    deck_chosen = []
    for cards in deck:
        if card_chosen in cards:
            deck_chosen.append(cards)
    player_chosen = bot_choice[1]

    for card in players[player_chosen][0]:
        if card in deck_chosen[0]:
            cards_to_pick.append([card, 1])
    cards_to_pick.append([card_chosen, 0])

    print 'bot_choice = ' + str(bot_choice)
    print 'cards_to_pick = ' + str(cards_to_pick)

    print bot_choice[2] + ' give me ' + str(cards_to_pick)
    system("say " + bot_choice[2] + ", give me ")
    for card in cards_to_pick:
        system("say " + card_names(card[0][0]) + ', ' + card[0][1:])

    has_card = raw_input("Does player have card(s)? Input 1 for yes, 0 for no: ")
    if has_card == '1' or has_card == 'y' or has_card == 'Y':
        for card in cards_to_pick:
            develop_cards(['0', str(player_chosen), str(card[0]), '1'])
        return '0'
    else:
        if len(cards_to_pick) > 1:
            ask_back = raw_input("Does player immediately asks cards back? Input 1 for yes, 0 for no: ")

            if ask_back == '1' or ask_back == 'y' or ask_back == 'Y':
                develop_cards(['0', str(player_chosen), str(card_chosen), '0'])
                return player_chosen
            else:
                for card in cards_to_pick:
                    if card[1] == 1:
                        develop_cards(['0', str(player_chosen), str(card[0]), '1'])
                develop_cards(['0', str(player_chosen), str(card_chosen), '0'])
                return player_chosen
        else:
            develop_cards(['0', str(player_chosen), str(card_chosen), '0'])
            return player_chosen

def bot_plays():
    # construct bot_list
    bot_list = []
    for player in players:
        bot_list.append([players[player][0], player, players[player][4], players[player][5], players[player][7]])

    # 4 combinations for 2 types of cards
    combinations = [[], [], [], [],[], [], [], []]

    # winning combinations
    winning_combinations = []

    # construct all possible winning combinations of deck
    for player in bot_list:
        for card in player[0]:
            for i in range(len(deck)):
                if card in deck[i]:
                    combinations[i].append(card)
    for combination in combinations:
        for i in range(len(deck)):
            if all(elem in combination for elem in deck[i]):
                print 'found winning combination!!' + str(combination)
                system("say " + "I found a winning combination. ")

                winning_combinations.append(combination)

    if winning_combinations != []:
        for combination in winning_combinations:
            winner = []
            for player in bot_list:
                winning_cards = list(set(player[0]).intersection(combination))
                winner.append(sorted([winning_cards, player[1], player[2], player[3]], key=lambda k: player[2]))
            print winner
            for combination in winner:
                if combination[0] != []:
                    system("say " + str(combination[0]) + ', ' + str(combination[3]))

    # no winning combinations
    else:
        sorted_combinations = sorted(combinations, key=len, reverse=True)

        bot_card_in_list = []
        # bot_in_list: at least one bot card in combinations (sorted)
        for combination in sorted_combinations:
            if any(x in players['0'][0] for x in combination):
                bot_card_in_list.append(combination)
        print 'bot_card_in_list = '
        print bot_card_in_list
        # get only the foes from the dictionary
        # [0: possible cards, 1: name, 2: player number]
        foes = []
        for player in players:
            if players[player][4] == 'foe':
                foes.append([players[player][1], players[player][5], player, players[player][0], players[player][2]])

        friends = []
        for player in players:
            if players[player][4] == 'friend':
                friends.append([players[player][1], players[player][5], player, players[player][0],players[player][2]])

        bot_cards_needed = []
        # construct reverse bot_card_in_list (all possible cards needed for each combination)
        for combination in bot_card_in_list:
            for i in range(len(deck)):
                for card in combination:
                    if card in deck[i]:
                        bot_cards_needed.append(list(set(combination).symmetric_difference(set(deck[i]))))
                        break

        print 'bot cards needed: '
        print bot_cards_needed

        chosen_foes = []
        for combination in bot_cards_needed:
            for foe in sorted(foes, reverse=False):
                if foe[0] != []:
                    for card in foe[0]:
                        if card in combination:
                            chosen_foes.append([card, foe[2], foe[1]])

        print 'chosen foes = ' + str(chosen_foes)

        chosen_friends = []
        for combination in bot_cards_needed:
            for friend in sorted(friends, reverse=False):
                if friend[0] != []:
                    for card in friend[0]:
                        if card in combination:
                            chosen_friends.append([card, friend[2], friend[1]])

        print 'chosen friends = ' + str(chosen_friends)

        chosen = []
        for card1 in chosen_foes:
            for card2 in chosen_friends:
                if card1[0] == card2[0]:
                    chosen.append(card1)


        # check previous card asked by the bot and make sure to ask again for another opponent
        # in case the opponent has this potential card
        previous_bot_card = players['0'][3]
        bot_can_play_previous_card = False

        # check if bot able to still request previous_bot_card, meaning
        # if bot still has one of the required cards in its deck.
        previous_bot_card_deck = []
        for cards in deck:
            if previous_bot_card in cards:
                previous_bot_card_deck = cards

        if previous_bot_card_deck != []:
            for card in players['0'][0]:
                if card in previous_bot_card_deck:
                    bot_can_play_previous_card = True

        foes_with_potential_card = []
        if bot_can_play_previous_card:
            if previous_bot_card != '':
                for foe in chosen_foes:
                    if previous_bot_card in foe[0]:
                        foes_with_potential_card.append([previous_bot_card, foe[1], foe[2]])

        print 'foes with potential previous card = ' + str(foes_with_potential_card)

        foes_without_previous_card = []
        if bot_can_play_previous_card:
            if previous_bot_card != '':
                for foe in foes:
                    if previous_bot_card not in foe[4]:
                        foes_without_previous_card.append([previous_bot_card, foe[2], foe[1]])

        print 'foes without previous card = ' + str(foes_without_previous_card)

        if foes_with_potential_card != []:
            print 'im at foes_with_potential_card '
            return play_card(foes_with_potential_card)
        elif chosen != []:
            print 'im at chosen'
            return play_card(chosen)
        elif chosen_foes != []:
            print 'im at chosen foes'
            return play_card(chosen_foes)
        elif foes_without_previous_card != []:
            print 'im at foes_without_previous_card '
            return play_card(foes_without_previous_card)
        elif chosen_friends != []:
            print 'im at chosen friends'
            # select random card from chosen friends and make sure the foe does not have it in the "does not have" pos
            counter = 0
            potential_foes = []
            random_card = ''
            while potential_foes == [] or counter < len(chosen_friends):
                random_card = random.choice(chosen_friends)[0]
                for foe in foes:
                    if random_card not in foe[4]:
                        potential_foes.append([random_card, foe[2], foe[1]])
                counter += 1

            if potential_foes != [] and random_card != '':
                return play_card(potential_foes)
            else:
                # choose card at random
                random_foe = random.choice(foes)
                random_foe_name = random_foe[1]
                random_foe_name_num = random_foe[2]
                chose = map(lambda x: x if x[2] == '' else [x[0], random_foe_name_num, random_foe_name], chosen_friends)
                return play_card(chose)
        else:
            # no potential cards from players, bot will ask randomly for a card from it's potential
            potential_card = random.choice(random.choice(bot_cards_needed))
            potential_player = random.choice(foes)

            print 'no potential cards from players, potential_card = ' + str(potential_card)
            print 'potential player = ' + str(potential_player)

            print str(potential_player[1]) + ' give me ' + str(potential_card)
            system("say " + str(potential_player[1]) + ", give me " + card_names(str(potential_card[0])) + potential_card[1:])
            has_card = raw_input("Does player have card? Input 1 for yes, 0 for no: ")
            if has_card == '1' or has_card == 'y' or has_card == 'Y':
                develop_cards(['0', str(potential_player[2]), str(potential_card), '1'])
                return '0'
            else:
                develop_cards(['0', str(potential_player[2]), str(potential_card), '0'])
                return str(potential_player[2])

def bot_answers(foe, card):
    # answer = raw_input("Which foe and which card? ex: 2 h5")
    # foe_card = answer.split(' ')
    foe_card = [foe,card]
    if foe_card[1] in players['0'][0]:
        print 'Yes I have this card. Here you go.'
        system("say " + str(players[foe_card[0]][5]) + random.choice(bot_positive_answer))
        develop_cards([foe_card[0], '0', foe_card[1], '1'])
        return foe
    else:
        print 'No, I do not have this card.'
        system("say " + str(players[foe_card[0]][5]) + random.choice(bot_negative_answer))
        develop_cards([foe_card[0], '0', foe_card[1], '0'])
        return '0'

def player_plays(player_turn):
    player_card = raw_input("For winning set,press <win>.To change turn, press <change>. " + players[player_turn][5] + " give player and card. "
                                                      "Insert 0 for bot, 1 for " + str(players['1'][5]) +
                                            ", 2 for " + str(players['2'][5]) + ", 3 for " + str(players['3'][5]) +
                                            ", 4 for " + str(players['4'][5]) + ", 5 for " + str(players['5'][5])).split(' ')

    if player_card[0] == 'win' or player_card[0] == 'WIN':
        remove_deck()
        return player_turn
    elif player_card[0] == 'change' or player_card[0] == 'CHANGE':
        player_change = raw_input("Which player do you want to give the turn to? Insert 0 for bot, 1 for " + str(players['1'][5]) +
                                            ", 2 for " + str(players['2'][5]) + ", 3 for " + str(players['3'][5]) +
                                            ", 4 for " + str(players['4'][5]) + ", 5 for " + str(players['5'][5]))
        if player_change == '0' or player_change in str_players:
            player_turn = player_change
            return player_turn
        else:
            return player_turn
    elif player_card[0] == '0' and str(player_card[1]) in flat_deck:
        player_turn = bot_answers(player_turn, player_card[1])
        return player_turn
    elif player_card[0] in str_players and str(player_card[1]) in flat_deck:
        foe_has_card = raw_input("Does foe has this card? y/n: ")
        if foe_has_card == 'y' or foe_has_card == 'Y' or foe_has_card == '1':
            answer = '1'
            develop_cards([player_turn, player_card[0], player_card[1], answer])
            return player_turn
        else:
            answer = '0'
            develop_cards([player_turn, player_card[0], player_card[1], answer])
            player_turn = player_card[0]
            return player_turn
    else:
        'Wrong input. Try again.'
        return player_turn

def play():
    player_turn = '1'
    while True:
            if player_turn == '0':
                user_input = raw_input("For win cards found, press <win>. To change"
                                            "turn press <change>. For bot to play press ENTER.")
                if user_input == 'win' or user_input == 'WIN':
                    remove_deck()
                elif user_input == 'change' or user_input == 'CHANGE':
                    player_change = raw_input("Which player do you want to give the turn to? ex: "
                                              "Insert 0 for bot, 1 for " + str(players['1'][5]) +
                                            ", 2 for " + str(players['2'][5]) + ", 3 for " + str(players['3'][5]) +
                                            ", 4 for " + str(players['4'][5]) + ", 5 for " + str(players['5'][5]))
                    if player_change == '0' or player_change in str_players:
                        player_turn = player_change
                    else:
                        continue
                elif user_input == '':
                    player_turn = bot_plays()
                else:
                    continue
            else:
                player_turn = player_plays(player_turn)

play()
