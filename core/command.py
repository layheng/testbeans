# generic command class
import shlex
from subprocess import Popen, PIPE


class Command(object):

    def __init__(self, command=None):
        self.command = command

    @staticmethod
    def execute_command(command):

        args = shlex.split(command)
        (response, error) = Popen(args, stdout=PIPE, stderr=PIPE).communicate()
        return response, error
