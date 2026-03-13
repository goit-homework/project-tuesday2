def command(name, *, description, usage=None, min_args=0):
    """Decorator to register a command handler with error handling and args validation."""
    def decorator(func):
        def wrapper(self, args):
            if len(args) < min_args:
                return f"Usage: {usage or name}"
            try:
                return func(self, args)
            except (ValueError, KeyError, IndexError) as e:
                return f"Error: {e}"
        wrapper._is_command = True
        wrapper._command_name = name
        wrapper._description = description
        wrapper._usage = usage or name
        return wrapper
    return decorator


class Command:
    """Represents a bot command with handler and description."""

    def __init__(self, handler, description, usage):
        self.handler = handler
        self.description = description
        self.usage = usage
