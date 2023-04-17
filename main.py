import argparse
import logging
import math
import random
import time

import pandas as pd

import outputter

class Participant:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash((self.id, self.name, self.email))

    def __str__(self):
        return f'{self.name} ({self.id})'


def main(args):
    print(f'args = {args}')

    df = pd.read_csv(args.file, sep=',')
    df.rename(columns={'Tijdstempel': 'timestamp', 'Geef je naam op': 'name', 'Geef je email adres op': 'email',
                       'Welk thema vind jij het interessantst?': 'preferences'}, inplace=True)

    number_of_rounds = args.rounds
    number_of_topics = args.topics
    number_of_preferences = args.preferences
    number_of_generations = args.generations

    # Fill list of participants and preferences per topic
    participants = set()
    topic_preferences = [set() for _ in range(number_of_topics)]  # topic per line containing preferred participants
    for i, row in df.iterrows():
        for preference in row['preferences'].split(','):
            participant = Participant(i, row['name'], row['email'])
            participants.add(participant)
            topic_preferences[int(preference) - 1].add(participant)

    for i, preferences in enumerate(topic_preferences):
        print(f'Topic {i + 1} got {len(preferences)} preferences')

    print('Starting generations...')
    gen_count = 0
    solution = generate_solution(participants, topic_preferences, number_of_topics, number_of_rounds,
                                 number_of_preferences)
    score, min_score = verify_solution(participants, solution, topic_preferences, number_of_preferences)
    best_score = score
    best_min_score = min_score
    print(f'Generation {gen_count} {(score, min_score)}')
    while gen_count < number_of_generations:
        start = time.time()
        solution = generate_solution(participants, topic_preferences, number_of_topics, number_of_rounds,
                                     number_of_preferences)
        score, min_score = verify_solution(participants, solution, topic_preferences, number_of_preferences)
        # TODO zet if best_min_score and best_score etc
        gen_count += 1
        print(f'Generation {gen_count} {(score, min_score)} in {time.time() - start}s')
    print(f'Solution found after {gen_count + 1} generation{"s" if gen_count > 0 else ""}:')
    outputter.pretty_print(solution)
    # outputter.pretty_print_per_participant(participants, solution)
    # outputter.solution_to_emails(participants, solution)


def generate_solution(participants, topic_preferences, number_of_topics, number_of_rounds, number_of_preferences):
    # topic per line containing assigned participants (sum)
    past_topic_assignments = [[] for _ in range(number_of_topics)]
    # round per line, topic per line containing assigned participants
    assignments = [[] for _ in range(number_of_rounds)]

    try:
        for i in range(number_of_rounds):
            # topic per line containing assigned participants (round)
            round_assignments = generate_round(participants, topic_preferences, past_topic_assignments,
                                               number_of_topics)
            assignments[i] = round_assignments
            past_topic_assignments = [past_topic_assignments[i] + round_assignments[i] for i in range(number_of_topics)]
    except ValueError:
        # Impossible combination found
        generate_solution(participants, topic_preferences, number_of_topics, number_of_rounds, number_of_preferences)

    return assignments


def generate_round(all_participants, topic_preferences, past_topic_assignments, number_of_topics):
    chosen_participants = set()
    number_of_participants_per_topic = math.floor(len(all_participants) / number_of_topics)
    round_assignments = []

    # Greedy assign even number of participants per topic
    for i in range(number_of_topics):
        topic_assignments = get_greedy_topic_assignments(i, all_participants, chosen_participants,
                                                         past_topic_assignments, topic_preferences,
                                                         number_of_participants_per_topic)
        chosen_participants.update(topic_assignments)
        round_assignments.append(topic_assignments)

    # Randomly assign the remaining participants
    for participant in [x for x in all_participants if x not in chosen_participants]:
        round_assignments[get_random_new_topic_for(participant, past_topic_assignments)].append(participant)

    return round_assignments


def get_greedy_topic_assignments(topic, all_participants, chosen_participants, past_topic_assignments,
                                 topic_preferences, size):
    remaining_preferred_participants = [x for x in all_participants
                                        if x not in chosen_participants
                                        and x not in past_topic_assignments[topic]
                                        and x in topic_preferences[topic]]
    if len(remaining_preferred_participants) >= size:
        return random.sample(remaining_preferred_participants, size)

    random_other_participants = [x for x in all_participants
                                 if x not in chosen_participants
                                 and x not in past_topic_assignments[topic]
                                 and x not in remaining_preferred_participants]
    return remaining_preferred_participants + random.sample(random_other_participants,
                                                            size - len(remaining_preferred_participants))


def get_random_new_topic_for(participant, past_topic_assignments):
    # get a random topic the participant has not followed yet
    return random.choice(
        [topic for topic, assignments in enumerate(past_topic_assignments) if participant not in assignments])


def verify_solution(participants, assignments, topic_preferences, number_of_preferences):
    participant_scores = {p: 0 for p in participants}
    for r in assignments:
        for t, topic in enumerate(r):
            for participant in topic:
                if participant in topic_preferences[t]:
                    participant_scores[participant] += 1
    return sum(participant_scores.values()), min(participant_scores.values())


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    argParser.add_argument('-f', '--file', type=str, help='path to preferences sheet', required=True)
    argParser.add_argument('-r', '--rounds', type=int, help='number of rounds', required=True)
    argParser.add_argument('-p', '--preferences', type=int, help='minimal number of preferred topics per participant',
                           required=True)
    argParser.add_argument('-t', '--topics', type=int, help='number of topics', required=True)
    argParser.add_argument('-g', '--generations', type=int, default=1000, help='number of topics', required=True)
    args = argParser.parse_args()

    if args.preferences > args.rounds:
        logging.error('Number of minimal preferences is higher than the number of rounds - no solution')
        exit(-1)
    if args.rounds > args.topics:
        logging.error('Number of rounds is higher than the number of topics - no solution')
        exit(-2)

    main(args)
