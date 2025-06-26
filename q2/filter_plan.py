import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Filter plan",
        description="Given a string, returns a plan for the setup of carbon filters on a street"
    )
    parser.add_argument(
        "input_string",
        help="The string that the plan is being devised for"
    )
    return parser.parse_args()

def filter_plan(input_str: str) -> str:
    """
    Fills any occurences of "?" with an "a" or "b" to avoid 3 of the same characters in a row.

    Strategy:
        - Copy fixed letters 
        - For each "?", build valid candidates by two guarded checks.
        - Pick the first survivor

    Input:
        - input_str (str): A string containing only "a", "b" and "?".

    Output:
        - a string containing only the following characters: "a" and/or "b".

    Assumptions:
        - There is always a solution.
        - Input string contains only the following characters: "a", "b" and "?".
        - Length of string in range: [1...500,000].
    """
    solution = []
    length = len(input_str)
    for i, char in enumerate(input_str):

        if char == "?":
            valid_choices = []
            candidates = ["a", "b"]

            for candidate in candidates:

                # left peek violation: previous 2 chars are both 'candidate'
                if i >= 2 and solution[i-2] == solution[i-1] == candidate:  
                    continue

                # right peek violation: next 2 chars in original string are both 'candidate'
                if i + 2 < length and input_str[i+2] == input_str[i+1] == candidate:
                    continue

                # middle peek violation: surrounding characters are both 'candidate
                if i >=1 and i +1 < length and solution[i-1] == candidate == input_str[i+1]:
                    continue

                valid_choices.append(candidate)
            
            # by problem assumption, atleast one choice survives - pick the first
            choice = valid_choices[0]
            solution.append(choice)

        else:
            # copy fixed 'a' or 'b' straight into the solution
            solution.append(char)

    return "".join(solution)

def main():
    args = parse_args()
    result = filter_plan(args.input_string)
    print(result)

if __name__ == "__main__":
    main()