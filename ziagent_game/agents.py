import random as r
from collections import defaultdict

from ziagent_game.common import *

class Agent(object):
    """
    Object class for agents.
    Agents are made of:
        id
        total payoff -- winnings from all games
        games played -- list of game id, move, payoff
        the number of times they swerved
        the number of times they stayed straight
        T/F if the agent is in a rut
    """
    instances = []

    def __init__(self, memory=0, rut_percentage=100):
        self.total_payoff = 0
        self.games_played = []

        self.memory = memory
        self.swerve = 0
        self.straight = 0
        self.rut = False
        self.rut_percentage = rut_percentage

        self.get_id()

    def __repr__(self):
        'Str representation of the game.'
        values = (self.id, self.total_payoff, len(self.games_played))
        return 'agent %s: total_payoff %s, games_played %s' % values

    def am_i_in_a_rut(self, rut_percentage):
        """
            Checks to see if the agent is in a rut.
            First it looks at n games that is twice the memory.
            Then it pulls out the dominate strategy. 
            Then finds out what percentage that strategy is played.
            If that is greater than the rut_percentage, then the agent
            is in a rut.
        """
        if self.memory == 0 or not rut_percentage:
            self.rut == False
            return

        if TimeTick.now > self.memory*2:       
            games_to_consider = self.games_played[-self.memory*2:]
            moves = []
            for g in games_to_consider:
                moves.append(g[1])

            # Find # of games used to play dominate strategy
            d = max(moves.count(0),moves.count(1))
            if d/len(moves)*100 > rut_percentage:
                self.rut = True
            else:
                self.rut = False
        else:
            self.rut = False

    def generate_move(self):
        """
        Generates move for the agent based off of:
        * memory
        * agent's rut status
        * number of games played
        """
        self.move = None
        self.am_i_in_a_rut(self.rut_percentage)

        if not self.rut:
            # We don't take memory into consideration until player 
            # is able to randomly choose a few times.
            if self.memory and len(self.games_played) > self.memory:
                games_to_consider = self.games_played[-self.memory:]
                
                # For each game, calculate which play gives a 
                # higher payoff.
                swerve = 0
                straight = 0
                for g in games_to_consider:
                    # Add up payoffs
                    if g[1] == 0:
                        swerve += g[2]
                    else:
                        straight += g[2]

                if swerve > straight:
                    self.move = move_choices[0]
                elif swerve < straight:
                    self.move = move_choices[1]
                # If we are here, then swerve & straight are the same

        if not self.move:
            self.move = r.choice(move_choices)

        # Add to swerve / straight counts to determine what 
        # route the agent is playing. 
        if self.move == move_choices[0]:
            self.swerve += 1
        else:
            self.straight += 1

        return self.move

    def update_agent_values(self):
        'Updates values for agent at the end of the runs.'
        self.__class__.instances.append((self.id, self.memory, 
                                         self.swerve, self.straight, 
                                         self.total_payoff, 
                                         self.games_played))
    

    def get_id(self):
        'Generats id for the agent.'
        self.id = get_id(self.__class__)
