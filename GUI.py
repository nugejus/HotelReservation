import tkinter as tk
from abc import ABC, abstractmethod

class GUI(ABC, tk.Tk):
    """
    An abstract base class for GUI-related functionality, inheriting from tk.Tk.
    Classes that inherit from this must implement the 'terminate' method.
    """

    @abstractmethod
    def terminate(self) -> None:
        """
        Abstract method to terminate the GUI application.
        Subclasses are required to override and implement this method
        for proper shutdown or cleanup operations.
        """
        pass
