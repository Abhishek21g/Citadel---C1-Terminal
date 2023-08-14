import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

import gamelib
import random
import math

class UltimateChessWarfareAlgo(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        self.support_spawn_points = None
        self.scored_on_locations = []

    def on_game_start(self, config):
        self.config = config
        self.support_spawn_points = config["supportSpawnPoints"]

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        
        self.build_defenses(game_state)
        self.build_reactive_defense(game_state)
        self.execute_offensive_strategy(game_state)
        
        game_state.submit_turn()

    def build_defenses(self, game_state):
        # Build defenses using tactical formations
        self.build_tactical_formations(game_state)
        
        # Upgrade Walls for better durability
        wall_locations = [[2, 12], [25, 12], [3, 12], [24, 12]]
        game_state.attempt_upgrade(wall_locations)

    def build_tactical_formations(self, game_state):
        # Build defensive and supportive structures in specific formations
        formation_1 = [[3, 11], [24, 11]]
        formation_2 = [[8, 11], [19, 11]]
        support_formation = [[13, 2], [14, 2], [13, 3], [14, 3]]
        
        for location in formation_1:
            game_state.attempt_spawn("Turret", location)
        for location in formation_2:
            game_state.attempt_spawn("Wall", location)
        for location in support_formation:
            game_state.attempt_spawn("Support", location)

    def build_reactive_defense(self, game_state):
        # Build additional Turrets based on enemy breaches
        for location in self.scored_on_locations:
            build_location = [location[0], location[1] + 1]
            game_state.attempt_spawn("Turret", build_location)

    def execute_offensive_strategy(self, game_state):
        # Deploy various units with adaptive tactics
        self.deploy_interceptors(game_state)
        self.deploy_demolishers(game_state)
        self.deploy_scouts(game_state)

    def deploy_interceptors(self, game_state):
        # Deploy Interceptors to counter enemy units
        interceptor_spawn_location = random.choice(self.support_spawn_points)
        game_state.attempt_spawn("Interceptor", interceptor_spawn_location, 10)

    def deploy_demolishers(self, game_state):
        # Deploy Demolishers with flanking tactics
        demolisher_spawn_location = [13, 0]
        game_state.attempt_spawn("Demolisher", demolisher_spawn_location, 10)

    def deploy_scouts(self, game_state):
        # Deploy Scouts with scouting and harassment tactics
        scout_spawn_location = random.choice(self.support_spawn_points)
        game_state.attempt_spawn("Scout", scout_spawn_location, 1000)

    def on_action_frame(self, turn_string):
        state = gamelib.GameState(self.config, turn_string)
        events = state.get_events()
        breaches = events["breach"]
        
        for breach in breaches:
            location = breach[0]
            self.scored_on_locations.append(location)
        
        self.scored_on_locations = list(set(self.scored_on_locations))

if __name__ == "__main__":
    algo = UltimateChessWarfareAlgo()
    algo.start()
