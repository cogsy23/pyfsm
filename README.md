# Introduction

So there are already heaps of these around GitHub and Pypi...
So here's another one!

The main focus of this FSM implementation is event driven automation processes
with an emphasis on a clean and concise, declerative syntax for defining the
FSM.

# Basics

```python
import fsm

# define an FSM with nodes
state = fsm.FSM()
state.node('STATE_A')  # first node added is the default state
state.node('STATE_B')

# add some edges
state.edge('STATE_A', 'signal_x', 'STATE_B')
state.edge('STATE_B', 'signal_y', 'STATE_A')

# execute some transitions
state('signal_x')
state('signal_y')
```

## Transition callbacks

Callbacks can be triggered when entering/exiting each state as well as on
specific edges.  Callbacks can have 0 or 3 parameters if they need info about the
transistion.


```python
# with state info
def f(current_state, signal, next_state):
    pass

# without state info
def g():
	pass

# for all transitions in/out of a node
state.edge('STATE_B', fexit=f, fenter=g)

# on a specific edge
state.edge('STATE_B', 'signal_y', 'STATE_A', fedge=f)
```

# Timed FSM

Often you'll want to use timeout events to drive your FSM, as well as other
signals.  While you can already specify 'timeout' edges with the basic FSM and
provide the signal from your own timer code, the TimedFSM provides a
convenient default timer implementation.

The TimedFSM adds an optional 'timeout' attribute for each node.  The timer
starts when entering the node and emits the 'timeout' signal after it expires.

The timer resets if another transition occurs before the timeout.

```python
state = fsm.TimedFSM()
state.node('STATE_A')
state.node('STATE_B', timeout=10.0)  # optional 10 second timeout for STATE_B
state.node('STATE_C')

state.edge('STATE_A', 'signal_x', 'STATE_B')
state.edge('STATE_B', 'signal_y', 'STATE_A')
state.edge('STATE_B', 'timeout', 'STATE_C')  # define 'timeout' edge

state.start()
```

In this example, STATE_B -> STATE_C will occur if signal_y doesn't happen
first.

The timer requires a thread to poll the clock which can either be started in
the background with

    state.start()

or run in the current thread with

    state.run()
