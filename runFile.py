from test_env import Plane
from qLearning import QLearningTable
from DQN import DeepQNetwork
from pg import PolicyGradient

def update():
    for episode in range(100):
        # initial observation
        observation = env.reset()
        totalReward = 0
        #DQN
        step = 0
        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            # #QLearning
            # action = RL.choose_action(str(observation))
            #DQN
            action = RL.choose_action(observation)
            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            totalReward += reward

            # #QLearning
            # # RL learn from this transition
            # RL.learn(str(observation), action, reward, str(observation_))
            #
            # # swap observation
            # observation = observation_
            #
            # # break while loop when end of this episode
            # if done:
            #     break

            #DQN
            RL.store_transition(observation, action, reward, observation_)

            if (step > 200) and (step % 5 == 0):
                RL.learn()

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                break
            step += 1

        print(totalReward)

    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Plane()
    # RL = QLearningTable(actions=list(range(env.n_actions)))
    RL = DeepQNetwork(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      e_greedy=0.9,
                      replace_target_iter=200,
                      memory_size=2000,
                      # output_graph=True
                      )
    RL = PolicyGradient(env.n_actions, env.n_features,
                      learning_rate=0.01,
                      reward_decay=0.9,
                      # output_graph=True
                      )
    env.after(100, update)
    env.mainloop()
    #DQN
    RL.plot_cost()