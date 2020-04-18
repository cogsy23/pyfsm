import logging
import fsm

# enable DEBUG logging for the FSM
logging.basicConfig(format='%(asctime)-15s %(name)8s: %(message)s')
logging.getLogger('fsm.fsm').setLevel(logging.DEBUG)


def pump_on(state, signal, next_state):
    print("PUMP_ON")


def pump_off(state, signal, next_state):
    print("PUMP_OFF")


state = fsm.FSM()
state.node('IDLE')
state.node('PUMP_ON')

state.edge('IDLE', 'level_high', 'PUMP_ON', fedge=pump_on)
state.edge('IDLE', 'timeout', 'PUMP_ON', fedge=pump_on)

state.edge('PUMP_ON', 'level_low', 'IDLE', fedge=pump_off)
state.edge('PUMP_ON', 'timeout', 'IDLE', fedge=pump_off)

state('level_high')
state('level_low')
state('timeout')
