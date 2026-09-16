# csp/constraints.py


def check_constraints(assignment):
    """
    Checks whether the current assignment
    satisfies all CSP constraints.

    Returns:
        (True, "All constraints satisfied!")
        or
        (False, "Reason for violation")
    """

    # ----------------------------------
    # Constraint 1: Escape
    # ----------------------------------

    if "Escape" in assignment:

        if assignment["Escape"] != "Driver":

            return (
                False,
                "Only the Driver can handle the Escape task."
            )


    # ----------------------------------
    # Constraint 2: Vault
    # ----------------------------------

    if "Vault" in assignment:

        if assignment["Vault"] != "Safecracker":

            return (
                False,
                "Only the Safecracker can open the Vault."
            )


    # ----------------------------------
    # Constraint 3: Disguise
    # ----------------------------------

    if "Disguise" in assignment:

        if assignment["Disguise"] != "Disguise Expert":

            return (
                False,
                "Only the Disguise Expert can handle Disguise."
            )


    # ----------------------------------
    # Constraint 4:
    # One person = One task
    # ----------------------------------

    assigned_people = list(assignment.values())

    if len(assigned_people) != len(set(assigned_people)):

        # Find the person assigned more than once

        duplicate_person = None

        for person in assigned_people:

            if assigned_people.count(person) > 1:

                duplicate_person = person
                break

        return (
            False,
            f"{duplicate_person} cannot perform two tasks "
            "simultaneously."
        )


    # ----------------------------------
    # Constraint 5: Security
    # ----------------------------------

    if "Security" in assignment:

        if assignment["Security"] != "Security Expert":

            return (
                False,
                "Security must be handled by the Security Expert "
                "when the alarm level is HIGH."
            )


    # ----------------------------------
    # Constraint 6:
    # Hacker cannot handle Vault + Cameras
    # ----------------------------------

    if "Vault" in assignment and "Cameras" in assignment:

        if (
            assignment["Vault"] == "Hacker"
            and assignment["Cameras"] == "Hacker"
        ):

            return (
                False,
                "The Hacker cannot handle both Vault and "
                "Cameras simultaneously."
            )


    # ----------------------------------
    # All constraints satisfied
    # ----------------------------------

    return (
        True,
        "All constraints satisfied!"
    )