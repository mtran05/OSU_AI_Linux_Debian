import os
os.environ["KERAS_BACKEND"] = "tensorflow"

import sys
sys.path.append("C:\\Users\\qttra\\OneDrive\\Documents\\GitHub\\OSU_AI")

import keras
from keras import layers
import numpy as np
import tensorflow as tf
import random
import datetime
import matplotlib.pyplot as plt
import pyautogui

from songSelect import chooseSong
from screenshot import getState
from stepClicking import getStep

"""----------------------"""

# Configuration parameters for the whole setup
gamma = 0.99  # Discount factor for past rewards
epsilon = 1.0  # Epsilon greedy parameter
epsilon_min = 0.1  # Minimum epsilon greedy parameter
epsilon_max = 1.0  # Maximum epsilon greedy parameter
epsilon_interval = (
    epsilon_max - epsilon_min
)  # Rate at which to reduce chance of random action being taken
batch_size = 8  # Size of batch taken from replay buffer
max_steps_per_episode = 10000
max_episodes = 2  # Limit training episodes, will run until solved if smaller than 1

# Main model (continue training if exists)
main = "../Models/Clicking/osu_ai-main.keras"

"""----------------------"""

num_actions = 2 # ! DO NOT CHANGE (2 possible actions: no click or click)

def create_q_model():
    return keras.Sequential(    # TODO: Need better architecture
        [
            # Convolutions on the frames on the screen
            layers.Conv2D(64, 5, strides=3, activation="relu", input_shape=(60, 80, 4)),
            layers.Conv2D(128, 5, strides=2, activation="relu"),
            layers.Conv2D(128, 3, strides=1, activation="relu"),
            layers.Conv2D(128, 3, strides=1, activation="relu"),
            layers.Flatten(),
            layers.Dense(512, activation="relu"),
            layers.Dense(2, activation="linear"),
        ]
    )

if (os.path.isfile(main)):
    model = keras.models.load_model(main)
    model_target = keras.models.load_model(main)
    print("\n\n\n\nREUSING MODEL\n\n\n\n")
else: 
    # The first model makes the predictions for Q-values which are used to
    # make a action.
    model = create_q_model()

    # Build a target model for the prediction of future rewards.
    # The weights of a target model get updated every 10000 steps thus when the
    # loss between the Q-values is calculated the target Q-value is stable.
    model_target = create_q_model()

# TODO: Open Tosu and OSU! after loading model, so we can start training right away without waiting model to load

"""------------------------"""

# ? May want to consider >> RMSProp << ?
# LR Scheduler
optimizer = keras.optimizers.Adam(learning_rate=0.00025, clipnorm=1.0)

# Experience replay buffers for clicking (action = 0)
state_history_0 = []
state_next_history_0 = []
rewards_history_0 = []
done_history_0 = []

# Experience replay buffers for no clicking (action = 1)
state_history_1 = []
state_next_history_1 = []
rewards_history_1 = []
done_history_1 = []

episode_accuracy_history = []
episode_reward_history = []
episode_count = 0
frame_count = 0
# Number of frames to take random action and observe output
epsilon_random_frames = 50000
# Number of frames for exploration
epsilon_greedy_frames = 1000000.0
# Maximum replay length
# Note: The Deepmind paper suggests 1000000 however this causes memory issues
max_memory_length = 100000
# Train the model after 4 actions
update_after_actions = 4
# How often to update the target network
update_target_network = 10000
# Using huber loss for stability
loss_function = keras.losses.Huber()

while True:
    state = getState()
    episode_reward = 0
    episode_accuracy = 0

    for timestep in range(1, max_steps_per_episode):
        # print(timestep) # Debugging
        frame_count += 1

        # Use epsilon-greedy for exploration
        if frame_count < epsilon_random_frames or epsilon > np.random.rand(1)[0]:
            # Take random action
            action = np.random.choice(num_actions)
        else:
            # Predict action Q-values
            # From environment state
            action_probs = model(state, training=False)
            # Take best action
            action = keras.ops.argmax(action_probs[0]).numpy()  # * Choose index 0 (action 0) or index 1 depending on which index has the highest Q-value

        # Decay probability of taking random action
        epsilon -= epsilon_interval / epsilon_greedy_frames
        epsilon = max(epsilon, epsilon_min)
        # print(f"Epsilon: {epsilon}") # ! Debugging Only

        # Apply the sampled action in our environment
        state_next, reward, done, accuracy = getStep(action)

        # Cumulative reward & Accuracy of the episode (beat map)
        episode_reward += reward
        episode_accuracy = accuracy

        # Save actions and states in replay buffers
        if (action == 0):
            state_history_0.append(state)
            state_next_history_0.append(state_next)
            done_history_0.append(done)
            rewards_history_0.append(reward)
        elif (action == 1):
            state_history_1.append(state)
            state_next_history_1.append(state_next)
            done_history_1.append(done)
            rewards_history_1.append(reward)
        
        # Next state
        state = state_next
        
        # Update every fourth frame and once batch size is large enough (as specified above as hyperparameter)
        if frame_count % update_after_actions == 0 and len(done_history_0) > int(batch_size/2) and len(done_history_1) > int((batch_size - batch_size/2)):
            # Random Seed
            seed = int(np.random.choice(range(100)))    # Convert to `int` since random.Random(seed) doesn't support `int-32`
            
            # Get indices of samples for replay buffers
            indices_0 = np.random.choice(range(len(done_history_0)), size=int(batch_size/2))
            indices_1 = np.random.choice(range(len(done_history_1)), size=int((batch_size - batch_size/2)))

            # Using list comprehension to sample from replay buffer
            state_sample = [state_history_0[i] for i in indices_0] + [state_history_1[i] for i in indices_1]
            state_next_sample = [state_next_history_0[i] for i in indices_0] + [state_next_history_1[i] for i in indices_1]
            rewards_sample = [rewards_history_0[i] for i in indices_0] + [rewards_history_1[i] for i in indices_1]
            action_sample = [0 for i in indices_0] + [1 for i in indices_1]
            done_sample = [float(done_history_0[i]) for i in indices_0] + [float(done_history_1[i]) for i in indices_1]
            
            # Order list & Shuffle using seed
            order = list(range(batch_size))
            random.Random(seed).shuffle(order)
            
            # Finish pre-processing
            state_sample = np.array([state_sample[i] for i in order])
            state_next_sample = np.array([state_next_sample[i] for i in order])     # shape (8, 60, 80, 4)
            rewards_sample = [rewards_sample[i] for i in order]
            action_sample = [action_sample[i] for i in order]
            done_sample = keras.ops.convert_to_tensor(
                [done_sample[i] for i in order]
            )

            # Build the updated Q-values for the sampled future states
            # Use the target model for stability
            future_rewards = model_target.predict(state_next_sample)    # shape (8, 2)
            
            # Q value = reward + discount factor * expected future reward
            updated_q_values = rewards_sample + gamma * keras.ops.amax(     # shape (8,)
                future_rewards, axis=1  # (8,)
            )

            # If final frame set the last value to -1
            updated_q_values = updated_q_values * (1 - done_sample) - done_sample

            # Create a mask so we only calculate loss on the updated Q-values
            masks = keras.ops.one_hot(action_sample, num_actions)

            with tf.GradientTape() as tape:
                # Train the model on the states and updated Q-values
                q_values = model(state_sample)

                # Apply the masks to the Q-values to get the Q-value for action taken
                q_action = keras.ops.sum(keras.ops.multiply(q_values, masks), axis=1)
                
                # Calculate loss between new Q-value and old Q-value
                loss = loss_function(updated_q_values, q_action)

            # Back-propagation
            grads = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(grads, model.trainable_variables))

        if frame_count % update_target_network == 0:
            # update the the target network with new weights
            model_target.set_weights(model.get_weights())
            # Log details
            print(f"\nAccuracy: {episode_accuracy:.2f} at episode {episode_count}, frame count {frame_count}\n")

        # Limit the state and reward history
        if len(rewards_history_0) > max_memory_length:
            del rewards_history_0[:1]
            del state_history_0[:1]
            del state_next_history_0[:1]
            del done_history_0[:1]
        elif len(rewards_history_1) > max_memory_length:
            del rewards_history_1[:1]
            del state_history_1[:1]
            del state_next_history_1[:1]
            del done_history_1[:1]

        # ! START OF DEBUGGING AREA !
        
        print(f"Points: {reward}")
        
        # ! END OF DEBUGGING AREA !
        
        if done:
            break
        
    # ! START OF DEBUGGING AREA !
    
    print(f"====================\nEpisode {episode_count}-th is Done!")
    print(f"Total points: {episode_reward}")
    print(f"Final accuracy: {episode_accuracy}\n====================")
    
    # TODO: Log the beat map accuracy out along with the map name within a log.txt file in Logs folder
    
    # ! END OF DEBUGGING AREA !

    # Update episodes cumulative reward
    episode_reward_history.append(episode_reward)
    if len(episode_reward_history) > 300:
        del episode_reward_history[:1]
    
    # Update episodes accuracy
    episode_accuracy_history.append(episode_accuracy)
    if len(episode_accuracy_history) > 300:
        del episode_accuracy_history[:1]

    episode_count += 1

    if episode_accuracy > 90:  # Condition to consider the task solved (accuracy for one map over 90%)
        print(f"\n!!!Solved at episode {episode_count}!!!\n")
        break

    if (
        max_episodes > 0 and episode_count >= max_episodes
    ):  # Maximum number of episodes reached
        print(f"Stopped at episode {episode_count}!")
        break
    
    # Choose a new song upon finishing one
    chooseSong()

# Save model after training
if (os.path.isfile(main)):
    model.save(main)
else:
    model.save(f"../Models/Clicking/osu_ai-{datetime.date.today()}.keras")