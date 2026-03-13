from difflib import get_close_matches


def suggest_command(user_input, available_commands):
    matches = get_close_matches(user_input, available_commands, n=1, cutoff=0.5)
    return matches[0] if matches else None
