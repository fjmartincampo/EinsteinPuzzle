from gurobipy import *

def solve():
    houses = list(range(1, 6))
    categories = {
        'Nationality': ['British', 'Swedish', 'Danish', 'Norwegian', 'German'],
        'Color': ['Red', 'Green', 'White', 'Yellow', 'Blue'],
        'Beverage': ['Tea', 'Coffee', 'Milk', 'Beer', 'Water'],
        'Tobacco': ['Pall Mall', 'Dunhill', 'Blend', 'BlueMaster', 'Prince'],
        'Pet': ['Dogs', 'Birds', 'Cats', 'Horses', 'Fish']
    }

    model = Model("EinsteinPuzzle")

    # Binary variable: x[cat, val, h] = 1 if house h has the attribute val
    x = {}
    for h in houses:
        for cat, values in categories.items():
            for val in values:
                x[h, cat, val] = model.addVar(vtype=GRB.BINARY, name=f"x_{h}_{cat}_{val}")

    # Each house must have exactly one attribute of each category
    for h in houses:
        for cat, values in categories.items():
            model.addConstr(quicksum(x[h, cat, val] for val in values) == 1)

    # Each attribute must be assigned to exactly one house
    for cat, values in categories.items():
        for val in values:
            model.addConstr(quicksum(x[h, cat, val] for h in houses) == 1)

    # Constraints
    # Clue 1: The British live in the red house
    for h in houses:
        model.addConstr(x[h, 'Nationality', 'British'] == x[h, 'Color', 'Red'])

    # Clue 2: The Swedish have dogs
    for h in houses:
        model.addConstr(x[h, 'Nationality', 'Swedish'] == x[h, 'Pet', 'Dogs'])

    # Clue 3: The Danish drinks tea
    for h in houses:
        model.addConstr(x[h, 'Nationality', 'Danish'] == x[h, 'Beverage', 'Tea'])

    # Clue 4: The green house is just to the left of the white house
    for h in range(1, 5):
        model.addConstr(x[h, 'Color', 'Green'] == x[h + 1, 'Color', 'White'])

    model.addConstr(x[5, 'Color', 'Green'] == 0)

    # Clue 5: The owner of the green house drinks coffee
    for h in houses:
        model.addConstr(x[h, 'Color', 'Green'] == x[h, 'Beverage', 'Coffee'])

    # Clue 6: The person who smokes Pall Mall raises birds
    for h in houses:
        model.addConstr(x[h, 'Tobacco', 'Pall Mall'] == x[h, 'Pet', 'Birds'])

    # Clue 7: The owner of the yellow house smokes Dunhill
    for h in houses:
        model.addConstr(x[h, 'Color', 'Yellow'] == x[h, 'Tobacco', 'Dunhill'])

    # Clue 8: The man in the center house drinks milk
    model.addConstr(x[3, 'Beverage', 'Milk'] == 1)

    # Clue 9: The Norwegian lives in the first house
    model.addConstr(x[1, 'Nationality', 'Norwegian'] == 1)

    # Clue 10: The person who smokes Blend lives next to the person who has Cats
    for h in houses:
        adj = []
        if h > 1:
            adj.append(x[h-1, 'Pet', 'Cats'])
        if h < 5:
            adj.append(x[h+1, 'Pet', 'Cats'])
        model.addConstr(x[h, 'Tobacco', 'Blend'] <= quicksum(adj))

    # Clue 11: The person who has Horses lives next to the person who smokes Dunhill
    for h in houses:
        adj = []
        if h > 1:
            adj.append(x[h-1, 'Tobacco', 'Dunhill'])
        if h < 5:
            adj.append(x[h+1, 'Tobacco', 'Dunhill'])
        model.addConstr(x[h, 'Pet', 'Horses'] <= quicksum(adj))

    # Clue 12: The person who smokes BlueMaster drinks Beer
    for h in houses:
        model.addConstr(x[h, 'Tobacco', 'BlueMaster'] == x[h, 'Beverage', 'Beer'])

    # Clue 13: The German smokes Prince
    for h in houses:
        model.addConstr(x[h, 'Nationality', 'German'] == x[h, 'Tobacco', 'Prince'])

    # Clue 14: The Norwegian lives next to the blue house
    for h in houses:
        adj = []
        if h > 1:
            adj.append(x[h-1, 'Color', 'Blue'])
        if h < 5:
            adj.append(x[h+1, 'Color', 'Blue'])
        model.addConstr(x[h, 'Nationality', 'Norwegian'] <= quicksum(adj))

    # Clue 15: The person who smokes Blend has a neighbor who drinks Water
    for h in houses:
        adj = []
        if h > 1:
            adj.append(x[h-1, 'Beverage', 'Water'])
        if h < 5:
            adj.append(x[h+1, 'Beverage', 'Water'])
        model.addConstr(x[h, 'Tobacco', 'Blend'] <= quicksum(adj))

    # Hide Gurobi output and optimize the model
    model.Params.OutputFlag = 0
    model.optimize()

    # If the model is solved to optimality, extract the results
    if model.status == GRB.OPTIMAL:
        results = {h: {} for h in houses}
        for cat, values in categories.items():
            for val in values:
                for h in houses:
                    if x[h, cat, val].X > 0.5:
                        results[h][cat] = val
                        
        return results
    return None