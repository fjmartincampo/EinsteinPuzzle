def printsolution(results):
    if not results:
        print("No solution was found.")
        return

    # Sorting the houses and categories for consistent output
    houses = sorted(results.keys())
    categories = list(results[houses[0]].keys())

    headers = ["Attribute"] + [f"House {h}" for h in houses]
    rows = [[cat] + [results[h][cat] for h in houses] for cat in categories]

    # Compute the maximum width for each column
    colw = [max(len(str(row[i])) for row in [headers] + rows) for i in range(len(headers))]

    # Formatting the rows
    def render_row(row):
        return " | ".join(f"{str(val):<{colw[i]}}" for i, val in enumerate(row))

    # Creating a line separator based on column widths
    line_separator = "-+-".join("-" * w for w in colw)

    # Printing the solution in a formatted table
    print("\n" + "=" * len(line_separator))
    print("SOLUTION TO THE EINSTEIN PUZZLE")
    print("=" * len(line_separator))
    print(render_row(headers))
    print(line_separator)
    for row in rows:
        print(render_row(row))
    print("=" * len(line_separator) + "\n")