from util.logger import Logger
from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class _Option:
    description: str
    action: Callable


class CLI:
    """Makes it easy to present a menu of multiple options to the user,
    to get a valid input from the user and to execute the chosen option.
    Also allows creating nested menus by creating multiple objects of this class.
    """

    # This class variable makes it possible to quit the entire application
    # from any submenu.
    _quit_all = False

    def __init__(self):
        self.get_prompt = lambda: ""  # A function that returns the prompt message.
        self.options = []
        self._back_opt = True  # Whether to give the option to go "up" from a submenu.
        self._quit_opt = True  # Whether to give the option to quit the entire application.
        self._once = False  # Whether to immediately leave the submenu after any option has been executed.

    def static_prompt(self, prompt: str):
        """Set a prompt that does not change."""
        self.get_prompt = lambda: prompt
        return self

    def dynamic_prompt(self, function: Callable[[], str]):
        """Set a prompt that gets dynamically computed by a function."""
        self.get_prompt = function
        return self

    def no_back(self):
        """Disable the option to go 'up' from a submenu."""
        self._back_opt = False
        return self

    def no_quit(self):
        """Disable the option to go quit the entire application."""
        self._quit_opt = False
        return self

    def once(self):
        """Immediately leave the menu after any option has been executed."""
        self._once = True
        return self

    def add(self, description: str, action: Callable):
        """Add an option to the menu.

        description -- A description of what the action does.
        action -- Either a function that gets executed when this option is
                  chosen or a CLI object that acts as a submenu when this
                  option is chosen.
        """
        self.options.append(_Option(description, action))
        return self

    def run(self):
        """Display the menu to the user and execute the chosen option."""
        back = False
        ran_once = False
        while not CLI._quit_all and not back and not (ran_once and self._once):
            print("\n\n", self.get_prompt(), "\n", sep="")
            for i, option in enumerate(self.options):
                print(f"({i+1}) {option.description}")
            if self._back_opt:
                print("(b) Back")
            if self._quit_opt:
                print("(q) Quit")
            response = input("\n> ")

            if response == "b" and self._back_opt:
                back = True
            elif response == "q" and self._quit_opt:
                CLI._quit_all = True
            elif response.isdigit():
                try:
                    option = int(response) - 1  # Option indices are printed as 1-based, we need 0-based.
                except ValueError:
                    logger.Error("String should have represented an integer but it has not.")
                    raise
                if option < len(self.options):
                    self.options[option].action()
                    ran_once = True
                else:
                    print(f"\nError: {response} is not an available option.")
            else:
                print(f"\nError: {response} is not an available option.")

    def __call__(self):
        self.run()

    @staticmethod
    def input(prompt):
        """A wrapper for input() with formatting that is consistent with the rest of this class."""
        return input(f"\n\n{prompt}\n\n> ")


if __name__ == "__main__":
    # An example of how this class could be used.

    # Plain function to execute
    def greet_user():
        name = CLI.input("What is your name?")
        print(f"\n\nHello, {name}!")

    # A forced sequence of menus
    def sequence():
        seq_prompt = "You have to go through this sequence whether you like it or not."
        CLI().no_back().no_quit().once().static_prompt(seq_prompt).add("Finish step 1", lambda: None).run()
        CLI().no_back().no_quit().once().static_prompt(seq_prompt).add("Finish step 2", lambda: None).run()
        CLI().no_back().no_quit().once().static_prompt(seq_prompt).add("Finish step 3", lambda: None).run()

    # Main menu
    cli = (CLI().static_prompt("Main menu")
                .no_back()
                .add("Greet me", greet_user)
                .add("Sub menu", cli_sub1 := CLI())
                .add("Forced sequence", sequence))

    # Submenu
    cli_sub1.static_prompt("You are now one level deeper in the menu.") \
            .add("Go deeper", cli_sub2 := CLI())

    # Sub-sub-menu
    cli_sub2.static_prompt("You are now even deeper in the menu.") \
            .add("Go deeper", cli_sub3 := CLI())

    # Sub-sub-sub-menu
    cli_sub3.static_prompt("You reached the deepest point in the menu.")

    cli.run()
