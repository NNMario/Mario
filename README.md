# Mario
The mario game

### Structure
The game consists of `objects` and `agents`.

* Objects are the environment (like the blocks, coins and other)
* Agents are subjects that are controlled by something
    * Enemies are controlled by simple and stupid AI
    * The player is controlled by keyboard, AI or something else
    
Every agent is decoupled from the thing that controls it.
On creation, the agent receives the **controller** that will 
dictate what action to take, considering the environment
and the agent data.
This way, it is easier to implement different types of AI
independently of any game changes

Inside `game.py`, one can specify the controller for 
the player object
* If the controller is `KeyBoardController`, the actions
will be polled from the pressed keyboard keys
* If the controller is something, it's entirely up to it what 
the next action will be

