# csp/solver.py

import json
import os


def get_level_configuration(level_id):

    project_root = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    constraints_file = os.path.join(
        project_root,
        "data",
        "constraints.json"
    )

    try:

        with open(
            constraints_file,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data["levels"].get(str(level_id))

    except FileNotFoundError:

        return None

    except json.JSONDecodeError:

        return None

    except KeyError:

        return None


def validate_player_plan(player_plan, level_id=1):

    level_data = get_level_configuration(level_id)

    if level_data is None:

        return (
            False,
            "Could not load CSP rules for this mission."
        )

    tasks = level_data["tasks"]
    allowed_assignments = level_data[
        "allowed_assignments"
    ]

    errors = []

    # Check every task has an assignment.
    for task in tasks:

        if task not in player_plan:

            errors.append(
                task + " has not been assigned."
            )

    if errors:

        return False, "\n".join(errors)

    # Check whether each selected team member
    # is allowed for that task.
    for task in tasks:

        selected_member = player_plan[task]

        allowed_members = allowed_assignments[task]

        if selected_member not in allowed_members:

            errors.append(
                selected_member
                + " cannot handle "
                + task
                + "."
            )

    # Check whether one person was assigned
    # to multiple tasks.
    if level_data.get("all_different"):

        selected_members = list(
            player_plan.values()
        )

        if len(selected_members) != len(
            set(selected_members)
        ):

            errors.append(
                "One team member cannot perform two tasks."
            )

    if errors:

        return False, "\n".join(errors)

    return (
        True,
        "All mission constraints are satisfied."
    )