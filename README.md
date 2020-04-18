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
state = fsm.FSM(['STATE_A', 'STATE_B'])

# add some edges
state.add('STATE_A', 'signal_x', 'STATE_B')
state.add('STATE_B', 'signal_y', 'STATE_A')

# execute some transitions
state('signal_x')
state('signal_y')
```

## Edge callbacks

Each edge can include a callback function like so

```python
f(current_state, signal, next_state):
    pass

state.add('STATE_B', 'signal_y', 'STATE_A', fedge=f)
```
