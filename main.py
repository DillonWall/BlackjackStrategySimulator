import random

class StepType:
    NONE = 0
    MULT = 1
    ADD = 2
    RESET = 3

class Step:
    def __init__(self, step_type, amount = 0):
        self._type = step_type
        self._amount = amount
    
    def get_type(self):
        return self._type

    def get_amount(self):
        return self._amount

class Strategy:    
    def __init__(self, init_bet):
        self._original_bet = init_bet
        self._streak = 0
        self._step_list_ahead = []
        self._step_list_behind = []
    
    def add_step_to_strategy_when_ahead(self, step):
        self._step_list_ahead.append(step)

    def add_step_to_strategy_when_behind(self, step):
        self._step_list_behind.append(step)

    def mod_bet(self, bet, step):
        if (step.get_type() == StepType.MULT):
            return bet * step.get_amount()
        if (step.get_type() == StepType.ADD):
            return bet + step.get_amount()
        if (step.get_type() == StepType.RESET):
            self._streak = 0
            return self._original_bet

    def get_next_bet(self, current_bet):
        if (self._streak == 0):
            return self._original_bet
        elif (self._streak > 0):
            arr_len = len(self._step_list_ahead)
            if (self._streak >= arr_len):
                current_step = self._step_list_ahead[arr_len - 1]
                return self.mod_bet(current_bet, current_step)
            else:
                current_step = self._step_list_ahead[self._streak]
                return self.mod_bet(current_bet, current_step)
        elif (self._streak < 0):
            arr_len = len(self._step_list_behind)
            if (-self._streak >= arr_len):
                current_step = self._step_list_behind[arr_len - 1]
                return self.mod_bet(current_bet, current_step)
            else:
                current_step = self._step_list_behind[-self._streak]
                return self.mod_bet(current_bet, current_step)

    def lost(self):
        if (self._streak > 0):
            self._streak = 0
        else:
            self._streak -= 1

    def won(self):
        if (self._streak < 0):
            self._streak = 0
        else:
            self._streak += 1

#----------Main----------#

#----PUBLIC-VARIABLES----#
_win_rate = .49             # Chance of winning a hand
_init_money = 20.00         # Money to start with each day
_init_bet = 0.50            # Dollar amount to bet initially
_iterations = 200           # Plays per day
_num_days = 30000           # Number of days to simulate
_quiting_amount = 5.00      # Minimum amount of money to stop playing for the day
_maxing_amount = 30.00      # Maximum amount of money to stop playing for the day
#------------------------#

_time_when_highest = 0
_total_of_highest = 0
_times_left = 0
_times_maxed = 0
_total_ended = 0


_bet = _init_bet
_money = _init_money
_highest = _init_money
_strategy = Strategy(_init_bet)

random.seed()

#-----STRATEGY-SETUP-----#
_strategy.add_step_to_strategy_when_ahead(Step(StepType.ADD, 0.25))

_strategy.add_step_to_strategy_when_behind(Step(StepType.MULT, 2))
_strategy.add_step_to_strategy_when_behind(Step(StepType.MULT, 2))
_strategy.add_step_to_strategy_when_behind(Step(StepType.ADD, 0.50))
# _strategy.add_step_to_strategy_when_behind(Step(StepType.RESET))
#------------------------#

#main loop
for day in range(_num_days):
    for i in range(_iterations):
        if _bet > _money or _money <= _quiting_amount:
            #print('Ran out of money!!!')
            _times_left += 1
            break

        if _money >= _maxing_amount:
            _times_maxed += 1
            break
        
        if random.random() < _win_rate:
            _strategy.won()
            _money += _bet
        else:
            _strategy.lost()
            _money -= _bet

        _bet = _strategy.get_next_bet(_bet)

        if (_money > _highest):
            _highest = _money
            _time_when_highest = i
    
    _total_ended += _money
    _total_of_highest += _highest
    _highest = _init_money
    _money = _init_money


# print('Ended with $' + str(_money))
# print('Highest money at one time: $' + str(_highest))
# print('You should have quit on turn: ' + str(_time_when_highest))
print('Your average of highest money was: $' + str(_total_of_highest / _num_days))
print('You left the table ' + str(_times_left) + ' times due to low money')
print('You left the table ' + str(_times_maxed) + ' times due to reaching your cashout point')
print('Your average end amount was: $' + str(_total_ended / _num_days))