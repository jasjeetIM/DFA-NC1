#!/usr/bin/python
# Author: Jasjeet Dhaliwal
# Simulates equivalence of DFA and NC1
# Requirements: Python (tested on Python 2.7)


class DFA:
  """Deterministic Finite Automaton"""
  def __init__(self, Q, sigma, delta, s, F):
    """DFA = (Q, sigma, delta, s, F)"""
    self.Q = Q
    self.sigma = sigma
    self.delta = delta
    self.s = s
    self.F = F
    self.curr_s = -1
     
  def delta_fn(self, in_val):
    """Transition Function """
    if ((self.curr_s, in_val) not in self.delta.keys()):
        print "Transition from %d on input %s not defined\n" % (self.curr_s, in_val)
        self.curr_s = -1
    else:
      self.curr_s = self.delta[(self.curr_s, in_val)]
    return self.curr_s
    
  def accepted(self):
    """Check if in final"""
    return self.curr_s in self.F
    
  def reset(self):
    """Go to start state """
    self.curr_s = self.s;
    
  def run_DFA(self, input_string):
    """Simulate DFA"""
    self.reset()
    for inp in input_string:
        state = self.delta_fn(inp)
        if state == -1:
          return

    if self.accepted():
      print "DFA accepted input"
    else:
      print "DFA rejected input"
    return
   
  def get_config(self):
    """Get the configuration of the DFA"""
    return (self.Q, self.sigma, self.delta, self.s, self.F)





class fn:
  """Utility class for composing functions"""
  def __init__(self, inp, Q, sigma, delta, s, F):
    self.curr_s = -1 
    self.input = [inp]
    self.Q = Q
    self.sigma = sigma
    self.delta = delta
    self.s = s
    self.F = F

  def compose_as_outer(self, f):
    """Form a composition of the current funtion and f"""
    self.input = self.input + f.input
    return self

  def delta_fn(self, in_val):
    """Transition Function """
    if ((self.curr_s, in_val) not in self.delta.keys()):
        print "Transition from %d on input %s not defined\n" % (self.curr_s, in_val)
        self.curr_s = -1
    else:
      self.curr_s = self.delta[(self.curr_s, in_val)]
    return self.curr_s
  
  def accepted(self):
    """Check if in final"""
    return self.curr_s in self.F
  
  def reset(self):
    """Go to start state"""
    self.curr_s = self.s

  def eval(self):
    """Evaluate the given function on the input"""
    self.reset()
    for inp in self.input:
        state = self.delta_fn(inp)
        if state == -1:
          return
    if self.accepted():
      return True
    else:
      return False 




class gate:
  """Wrapper class for simulating gates in a circuit"""
  def __init__(self, fn):
      self.function = fn
    
  def compose_as_outer(self, g):
    return gate(self.function.compose_as_outer(g.function))

  def eval(self):
    return self.function.eval()




class NC1:
  """Simulate a NC1 circuit for a fixed input size"""
  def __init__(self, input_string, Q, sigma, delta, s, F ):      
      #Build bottom gates
      gate_list = []
      for inp in input_string:
        func = fn(inp, Q, sigma, delta, s, F)
        g= gate(func)
        gate_list.append(g)
      
      #Build circuit upto the top gate one level at a time
      new_list = []
      old_list = gate_list
      while len(old_list) != 0:
        gate_1 = self.pop_gate(old_list)
        gate_2 = self.pop_gate(old_list)
        #One gate left
        if not gate_2:
          new_list.append(gate_1)
          if len(old_list) == 0:
            if len(new_list) == 1:
              break
            else:
              old_list = new_list
              new_list = []

        #Atleast 2 gates left so compose them
        else:
          new_list.append(gate_1.compose_as_outer(gate_2))
          if len(old_list) == 0:
            if len(new_list) == 1:
              break
            else:
              old_list = new_list
              new_list = []
      
      self.top_gate = new_list[0] 
      self.output = False 

  def accepted(self):
    return self.output
    
  def pop_gate(self, gate_list):
    if len(gate_list) > 0:
      return gate_list.pop(0)
    else:
      return None

  def eval_top(self): 
    """Evaluate the top gate"""
    self.output = self.top_gate.eval()
    if self.accepted():
      print "NC1 accepted input"
    else:
      print "NC1 rejected input"
    return


def build_DFA():
  """Build a transition function and state set"""

  #Edit Q, sigma, delta, s, F to change behavior

  #MUST use int states
  Q = {0, 1, 2, 3}

  #MUST use string alphabets 
  sigma = {'alpha', 'beta', 'gamma', 'phi'}

  #MUST use a dictionary with (state, alphabet) as key
  #and state as value
  delta = dict();
  delta[(0, 'alpha')] = 1
  delta[(0, 'beta')] = 2
  delta[(0, 'gamma')] = 3
  delta[(0, 'phi')] = 0
  delta[(1, 'alpha')] = 1
  delta[(1, 'beta')] = 2
  delta[(1, 'gamma')] = 3
  delta[(1, 'phi')] = 0
  delta[(2, 'alpha')] = 1
  delta[(2, 'beta')] = 2
  delta[(2, 'gamma')] = 3
  delta[(2, 'phi')] = 0
  delta[(3, 'alpha')] = 1
  delta[(3, 'beta')] = 2
  delta[(3, 'gamma')] = 3
  delta[(3, 'phi')] = 0

  #Have only 1 start state
  s = 0

  #Define set of Final/Accepting states
  F = {3,2}

  dfa = DFA(Q, sigma, delta, s, F)
  return dfa


def main():
  """Build and simulate DFA, followed by the reduction of 
     the DFA to an NC1 circuit """
  dfa = build_DFA()
  #Edit the input string in place here 
  #Example of Accept
  input_string = ['alpha', 'beta', 'beta', 'gamma', 'phi', 'gamma']
  #Example of Reject
  #input_string = ['alpha', 'beta', 'beta', 'gamma', 'phi', 'phi']
  #Run DFA
  dfa.run_DFA(input_string)

  #Convert to NC1 circuit and output answer
  nc1 = NC1(input_string, *dfa.get_config())
  nc1.eval_top()

if __name__ == "__main__":
  main()
