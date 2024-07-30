import random


def create_random_teams(population, group_size):
    """
    Randomly divides a list of IDs or names into groups.

    Args:
    population (list): The list of IDs or names to divide into teams.
    group_size (int): The maximum size of each team.

    Returns:
    list of lists: A list containing the groups.
    """
    # Shuffle the list to randomize
    random.shuffle(population)

    # Split the list into groups
    teams = [population[i:i + group_size] for i in range(0, len(population), group_size)]

    return teams


def main():
    # Example usage:
    population = ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace']
    group_size = 3
    teams = create_random_teams(population, group_size)
    print(teams)


if __name__ == '__main__':
    main()
    main()
