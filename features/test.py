from core.command import Command

command_line = "find -name *.feature"

response, error = Command.execute_command(command_line)

print(response.splitlines())