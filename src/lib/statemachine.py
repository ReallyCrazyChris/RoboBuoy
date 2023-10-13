class StateMachine(object):
    """the brain - manages states"""
    def __init__(self):
        self.states = {}
        self.activeState = None

    def addState(self, state):
        """Adds a new state"""
        self.states[state.name] = state
        return state

    def transitionTo(self,data):
        """
        Does whatever the current state instructs
        and changes to new state if needed.
        """
        if self.activeState is not None:
            self.activeState.action(data)
        new_state_name = self.activeState.transitionTo(data)
        if new_state_name is not None:
            self.setState(new_state_name)

    def setState(self, new_state_name):
        """Changes states and performs appropriate exit and entry actions."""
        if self.activeState is not None:
            self.activeState.end()
        self.activeState = self.states[new_state_name]
        self.activeState.__start__()


class State(object):
    """An abstract state."""
    def __init__(self, name):
        self.name = name

    def __start__(self):
        """Perform these actions when this state is first entered."""
        self.start()

    def action(self,statename):
        """Perform these actions when in this state."""
        pass

    def transitionTo(self,statename):
        """Check these conditions to see if state should be changed."""
        pass

    def start(self):
        """Perform these actions when this state is first entered."""
        pass

    def end(self):
        """Perform these actions when this state is exited."""
        pass