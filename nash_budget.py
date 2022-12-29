import cvxpy as cp

def Nash_budget(total: float, subjects: list[str], preferences: list[list[str]]):
    """
    Input:
    Total budget
    A list of subject
    A list of agents with preferences for each subject

    Output: 
    Prints the budget divided to each subject. The budget will be fair for groups (i.e: for each subset k of the agents, the sum for k is k*(budget/n))
    """
    
    allocations = cp.Variable(len(subjects)) # List of cvxpy Variables for each subject
    budgets = [total/len(preferences) for i in preferences] # This is a list of C/n budget for each agent
    
    # Get preferences from agent as variables
    preferencesVariables = [cp.Expression()]*len(preferences)
    for index, agent in enumerate(preferences):
        preferencesVariables[index] = allocations[subjects.index(agent[0])]
        for i in range(1, len(agent)):
            preferencesVariables[index] += allocations[subjects.index(agent[i])]
        
    sum_of_logs = cp.sum([cp.log(u) for u in preferencesVariables]) # create sum of logs of the agent's variables
    positivity_constraints = [v >= 0 for v in allocations] # positivity constraint for each individual variable
    sum_constraint = [cp.sum(allocations)==total] # equation constraint for sum of all variables should be equal to total budget

    problem = cp.Problem(cp.Maximize(sum_of_logs), constraints = positivity_constraints+sum_constraint)
    problem.solve()

    for index, variable in enumerate(allocations):
        print("Subject", subjects[index], "get", variable.value)

    for index, agentPreferences in enumerate(preferences):
        print("Agent", index, "pays:", end=" ")
        for subject in agentPreferences:
            print(allocations[subjects.index(subject)].value * budgets[index] / preferencesVariables[index].value, "to subject ", subject)

def main():
    Nash_budget(500, ['a', 'b', 'c', 'd'], [['a', 'b'], ['a', 'c'], ['a', 'd'], ['b', 'c'], ['a']])


if __name__ == "__main__":
    main()
