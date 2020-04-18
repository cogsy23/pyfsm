import logging
import threading
import time

log = logging.getLogger(__name__)


class FSMException(Exception):
    pass


class FSM(object):
    def __init__(self):
        self.current_state = None
        self._transitions = {}
        self._lock = threading.RLock()

    def node(self, state):
        self._transitions[state] = {}
        if self.current_state is None:
            self.current_state = state

    def edge(self, state, signal, next_state, fedge=None):
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


class TimedFSM(FSM):
    def __init__(self):
        super(TimedFSM, self).__init__()
        self._timeouts = {}
        self.timestamp = None
        self._running = False

    def node(self, state, timeout=None):
        super(TimedFSM, self).node(state)
        self._timeouts[state] = timeout

    def start(self):
        if self._running:
            return

        self._t = threading.Thread(target=self.run)
        self._t.start()

    def cancel(self):
        self._running = False
        self._t.join()
        self._t = None

    def run(self):
        # initial timeout
        self.set_timeout(self._timeouts[self.current_state])

        self._running = True
        while self._running:
            time.sleep(0.1)  # simple polling, not hugely accurate
            with self._lock:
                if self.timestamp is None:
                    continue

                if time.time() > self.timestamp:
                    self.timestamp = None
                    self('timeout')

    def set_timeout(self, delay):
        ''' Set the timeout event to trigger delay seconds from now'''
        with self._lock:
            if delay is None:
                self.timestamp = None
            else:
                self.timestamp = time.time() + delay

    def __call__(self, signal):
        with self._lock:
            s = super(TimedFSM, self).__call__(signal)
            self.set_timeout(self._timeouts[s])
            return s
