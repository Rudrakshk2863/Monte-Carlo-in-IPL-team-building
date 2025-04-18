from __future__ import unicode_literals
import numpy as np
import pandas as pd
import random

# getting the data into a readable format

player_data = pd.read_csv(r'C:\Users\Rudraksh\OneDrive\Desktop\ipl_players.txt', delimiter=" ")
player_data.to_csv('ipl_players.csv')
df = pd.read_csv(r'C:\Users\Rudraksh\PycharmProjects\pythonProject\ipl_players.csv')
df = df.iloc[:, 1:]
df.to_csv('ipl_players_cleaned.csv', index=False)
df['BasePrice(Pi)'] = player_data['BasePrice(Pi)'].str.replace("crore", "", regex=True)
df['BasePrice(Pi)'] = df['BasePrice(Pi)'].astype(float)
# print(df)

# now i have to do the metropolis part
# lets make a list for base price and corresponding skill rating and player

base_prices = []
players = []
skill = []
for i, j, k in zip(df['BasePrice(Pi)'], df['Player'], df['SkillRating(Si)']):
    bp = i
    base_prices.append(bp)
    pp = j
    sr = k
    players.append(pp)
    skill.append(sr)

# now these arrays can be used in computation

def metropolis(Max_budget, player_list, price_list, skill_ratings, iterations=1000000):
    """ Uses Metropolis-like algorithm to find an optimal IPL team within a budget. """

    # Initialize a random team within budget
    while True:
        current_team_indices = random.sample(range(len(player_list)), 11)
        current_team_price = sum(price_list[i] for i in current_team_indices)
        if current_team_price >= Max_budget:
            print("Team budget exceeded")
            break  # Start with a valid team

    current_team_skill = sum(skill_ratings[i] for i in current_team_indices)

    for _ in range(iterations):
        # Select a player to swap out
        swap_out = random.choice(current_team_indices)
        available_replacements = [i for i in range(len(player_list)) if i not in current_team_indices]

        # Select a replacement that does not exceed budget
        random.shuffle(available_replacements)
        for swap_in in available_replacements:
            new_team_indices = current_team_indices.copy()
            new_team_indices.remove(swap_out)
            new_team_indices.append(swap_in)

            new_price = sum(price_list[i] for i in new_team_indices)
            new_skill = sum(skill_ratings[i] for i in new_team_indices)

            if new_price <= Max_budget:  # Only consider swaps within budget
                # Accept if skill improves, or with a small probability (adaptive)
                accept_probability = 0.05 + 0.00005 * (new_skill / max(skill_ratings))  # Higher for good players
                if new_skill > current_team_skill or np.random.rand() < accept_probability:
                    current_team_indices, current_team_price, current_team_skill = new_team_indices, new_price, new_skill
                break  # Stop checking after finding the first valid replacement and then loop repeats for N iterations
    final_players = [player_list[i] for i in current_team_indices]
    final_prices = [price_list[i] for i in current_team_indices]
    final_skills = [skill_ratings[i] for i in current_team_indices]

    return final_players, final_skills, final_prices, current_team_skill, current_team_price


# Run the function with a budget of 50 crores and 60 crores
final_team, final_team_skill, final_team_prices, total_skill, total_price = metropolis(60, players, base_prices, skill)

# Print the results

print("Final Team:", final_team)
print("Skill Ratings:", final_team_skill)
print("Prices:", final_team_prices)
print(f"Total Skill: {total_skill}")
print(f"Total Price: {total_price}")

'''
def metropolis(Max_budget, player_list, price_list, skill_ratings, iterations = 10000):
    final_team = []
    final_team_prices = []
    final_team_skill = []
    total_skill = 0
    total_price = 0
    for _ in range(iterations):
        random_nos = random.sample(range(0, len(player_list)), 11)  # first lets make a team of 11 random players
        for i in random_nos:   # calculate the parameters necessary
            plyrs = player_list[i]
            rokda = price_list[i]
            total_skill += skill_ratings[i]
            total_price += price_list[i]
            final_team_prices.append(rokda)
            final_team.append(plyrs)
            final_team_skill.append(skill_ratings[i])
            while total_price <= Max_budget:   # random swaps
                print("In budget")
                rand_swap_index_1 = np.random.randint(0, len(final_team))
                rand_swap_index_2 = np.random.randint(0, len(players))
                final_team[rand_swap_index_1] = player_list[rand_swap_index_2]
                final_team_prices[rand_swap_index_1] = price_list[rand_swap_index_2]
                total_price = sum(final_team_prices)
                final_team_skill[rand_swap_index_1] = skill_ratings[rand_swap_index_2]
                total_skill2 = sum(final_team_skill)
                if total_skill2 >= total_price:
                    print("optimised a lil bit")
                    total_skill = total_skill2
                else:
                    print("failed to optimise trying again...")

            else:
                print("out of budget")
                break
    return final_team, final_team_skill, final_team_prices, total_skill, total_price

final_team, final_team_skill, final_team_prices, total_skill, total_price = metropolis(50, players, base_prices, skill)
print(final_team)
print(final_team_skill)
print(final_team_prices)
print(total_skill, 'skill')
print(total_price, 'price')
'''



