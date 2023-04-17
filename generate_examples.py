import datetime
import random


def get_unique_preferences(topics, number_of_preferences):
    chosen = []
    for i in range(number_of_preferences):
        chosen.append(random.choice([x for x in topics if x not in chosen]))
    return chosen


if __name__ == '__main__':
    number_of_participants = 123
    number_of_topics = 10
    number_of_preferences = 5

    # topics = range(1, number_of_topics + 1)
    topics = [k for i in range(1, number_of_topics + 1) for k in i * [i]]

    with open('./examples/random_names.txt') as f:
        random_names = f.read().splitlines()

    for i in range(number_of_participants):
        random_name = random.choice(random_names)
        print(f'{datetime.datetime.now()},'  # timestamp
              f'{random_name},'  # name 
              f'{random_name.replace(" ", "")}@email.com,'  # email
              f'"{",".join(map(str, get_unique_preferences(topics, number_of_preferences)))}"')  # preferences
