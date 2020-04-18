import logging
import threading

log = logging.getLogger(__name__)


class FSMException(Exception):
    pass


class FSM(object):
    def __init__(self, states):
        self.current_state = states[0]
        self._transitions = dict([(s, {}) for s in states])
        self._lock = threading.Lock()

    def add(self, state, signal, next_state, fedge=None):
        if state not in self._transitions:
            raise FSMException("Unkown state: {:s}".format(state))
        if next_state not in self._transitions:
            raise FSMException("Unkown state: {:s}".format(next_state))

        self._transitions[state][signal] = (next_state, fedge)

    def __call__(self, signal):
        with self._lock:
            cur_transitions = self._transitions[self.current_state]

            if signal not in cur_transitions:
                return self.current_state

            next_state, fedge = cur_transitions[signal]

            log.debug("{:s}({:s}) -> {:s}".format(
                self.current_state, signal, next_state))

            if fedge:
                fedge(self.current_state, signal, next_state)

            self.current_state = next_state

            return self.current_state
