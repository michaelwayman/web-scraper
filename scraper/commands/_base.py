""" Interface for a Command. """

from abc import abstractmethod


class BaseCommand:
    """ Command interface. """

    help = ''

    def __init__(self):
        pass

    def add_arguments(self, parser):
        """ CLI args for this command.
        Args:
            parser (ArgumentParser): Parser the developer can configure for his/her needs.
        Note:
            parser args get passed to `execute()`.
        """
        pass

    @abstractmethod
    def execute(self, args):
        """ Command is triggered by calling this.
        Args:
            args (obj): namespace containing the argument for this command AND the Schireson program.
        """
        pass
