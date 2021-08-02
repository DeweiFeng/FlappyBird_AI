import os
import pickle
import neat
import numpy as np
import bird
# load the winner
with open('winner', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)


env = bird.Bird()
observation = env.reset()

while True:
    output = net.activate(observation)
    action = np.argmax(output)
    observation, reward, going = env.step(action)
