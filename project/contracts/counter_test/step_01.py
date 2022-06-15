from pyteal import *
from pyteal_helpers import program

def approval():
  # All global variables should be prefixed with `global_`
  # Also, define their data type as a comment for better tracking
  
  global_owner = Bytes("owner") # byteslice – Indicates a string or an array of int
  global_counter = Bytes("counter") # int

  # Create the custom operation event names

  op_increment = Bytes("inc")
  op_decrement = Bytes("dec")

  # Create the custom operation callbacks

  increment = Seq(
    App.globalPut(global_counter, App.globalGet(global_counter) + Int(1)),
    Approve(),
  )

  decrement = Seq(
    App.globalPut(global_counter, App.globalGet(global_counter) - Int(1)),
    Approve(),
  )

  return program.event(
    # The `init` event allows us to initialize the global variables on the 
    # first creation of the smart contract
    #
    # `Seq` triggers a list of functions sequentially
    init=Seq(
      App.globalPut(global_owner, Txn.sender()),
      App.globalPut(global_counter, Int(0)),
      Approve(),
    ),
    # The `no_op` is the ideal place to place custom operations.
    #
    # The `Cond` function executes the first condition that gets satisfied.
    # If no conditions gets satisfied, then an error is thrown
    no_op=Cond(
      [Txn.application_args[0] == op_increment, increment],
      [Txn.application_args[0] == op_decrement, decrement],
    ),
  )

def clear():
  return Approve()