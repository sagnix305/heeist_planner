# csp/backtracking.py


def backtracking_search(
    variables,
    domains,
    constraint_checker
):
    """
    Solves a CSP using backtracking search.
    """

    def backtrack(assignment):

        # ----------------------------------
        # Base Case
        # ----------------------------------

        if len(assignment) == len(variables):

            return assignment.copy()


        # ----------------------------------
        # Select unassigned variable
        # ----------------------------------

        unassigned = [
            variable
            for variable in variables
            if variable not in assignment
        ]

        variable = unassigned[0]


        # ----------------------------------
        # Try each value
        # ----------------------------------

        for value in domains[variable]:

            assignment[variable] = value


            # Check constraints
            valid, message = constraint_checker(
                assignment
            )


            if valid:

                result = backtrack(
                    assignment
                )

                if result is not None:

                    return result


            # ----------------------------------
            # Backtrack
            # ----------------------------------

            del assignment[variable]


        return None


    return backtrack({})