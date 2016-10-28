from subprocess import Popen, PIPE


class Command(object):
    """
    command line execution utility
    """

    @staticmethod
    def execute_command(command):
        """
        execute command line
        :param command:
        :return: response, error
        """
        (response, error) = Popen(command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return response, error


if __name__ == "__main__":
    (output, error) = Command.execute_command("ls ../features/")
    print(output)