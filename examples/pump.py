import logging
import fsm

logging.basicConfig(format='%(asctime)-15s %(name)8s: %(message)s')
logging.getLogger('fsm.fsm').setLevel(logging.DEBUG)


def pump_on(state, signal, next_state):
    print("PUMP_ON")


def pump_off(state, signal, next_state):
    print("PUMP_OFF")


state = fsm.FSM(['IDLE', 'PUMP_ON'])

state.add('IDLE', 'level_high', 'PUMP_ON', fedge=pump_on)
state.add('IDLE', 'timeout', 'PUMP_ON', fedge=pump_on)

state.add('PUMP_ON', 'level_low', 'IDLE', fedge=pump_off)
state.add('PUMP_ON', 'timeout', 'IDLE', fedge=pump_off)

state('level_high')
state('level_low')
state('timeout')
