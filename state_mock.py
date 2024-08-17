import random
import time

class State:
    """Duck type"""
    current_state = 'dummy'

    @classmethod
    def possible_transitions(cls) -> list[str]:
        """Returns a list of possible transitions"""
        pass

    @classmethod
    def transition(cls, t: str) -> None:
        """Applies the specified transition to the current state and executes the action on the target state"""
        pass

    @classmethod
    def error_code(cls) -> int:
        pass

class BatteryState:
    # Transitions
    REPLACED = 'REPLACED'
    GONE_BAD = 'GONE_BAD'
    USED = 'USED'

    # States
    NORMAL_STATE = 'BATTERY_NORMAL'
    LOW_STATE = 'BATTERY_LOW'
    FAULTY_STATE = 'BATTERY_FAULTY'

    _STATE_MAP = {
        LOW_STATE: {
            'ERROR_CODE': 101,
            'TRANSITIONS': {
                REPLACED: NORMAL_STATE,
                GONE_BAD: FAULTY_STATE,
            },
        },
        NORMAL_STATE: {
            'ERROR_CODE': 100,
            'TRANSITIONS': {
                USED: LOW_STATE,
                GONE_BAD: FAULTY_STATE,
            },
        },
        FAULTY_STATE: {
            'ERROR_CODE': 101,
            'TRANSITIONS': {
                REPLACED: NORMAL_STATE,
            },
        },
    }

    # set initial state 
    current_state = LOW_STATE
    print(f'INITIAL STATE: {current_state}')
    
    @classmethod
    def possible_transitions(cls) -> list[str]:
        """Returns a list of possible transitions"""
        return list(cls._STATE_MAP[cls.current_state]['TRANSITIONS'].keys())

    @classmethod
    def transition(cls, t: str) -> None:
        """Applies the specified transition to the current state and executes the action on the target state"""
        print(f'{cls} CURRENT STATE: {cls.current_state}')
        print(f'{cls} APPLYING TRANSITION: {t}')
        new_state = cls._STATE_MAP[cls.current_state]['TRANSITIONS'][t]
        print(f'{cls} CURRENT STATE: {new_state}')
        cls.current_state = new_state

    @classmethod
    def error_code(cls) -> int:
        ec = cls._STATE_MAP[cls.current_state]['ERROR_CODE']
        print(f'{cls} ERROR CODE: {ec}')
        return ec


# general function to set PLC error code
def set_error_code(code: int) -> None:
    # implement loginc to set PLC error code
    pass

# state management
class StateManagement:
    tracked_states = list()

    @classmethod
    def register_state(cls, state: State) -> None:
        """Register a state to track"""
        cls.tracked_states.append(state)
        print(f'registered {state}')

    @classmethod
    def transition(cls) -> None:
        for state in cls.tracked_states:
            t = random.choice(state.possible_transitions())
            state.transition(t)
            er = state.error_code()
            if er is not None:
                set_error_code(er)



# top-level process
PERIOD = 10000 # milliseconds
PERIOD_SECS = PERIOD / 1e3
if __name__ == '__main__':
    StateManagement.register_state(BatteryState)
    while True:
        time.sleep(PERIOD_SECS)
        StateManagement.transition()
        