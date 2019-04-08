#!/usr/bin/env python

from error_handling import ExtendEnvironmentError

class Environment(object):
    """A environment is a sequence of frames, where each frame
    is a table of bindings that associate variables and values.
    
    Except for the initial environment set up 
    when the evaluator starts up, all other environments 
    should be created by extending some existing environment.
    So only the attribute `enclosing_environment` of the initial
    environment is None.
    """
    def __init__(self, variables = tuple(), values = tuple(), enclosing_environment = None):
        '''Use `variable` and `values` to construct first frame, and get following frames from enclosing environment.
        '''
        self.first_frame = dict(zip(variables, values))
        if enclosing_environment == None:
            self.frames = [self.first_frame]
        else:
            self.frames = [self.first_frame] + enclosing_environment.frames

    def set_binding(self, variable, value):
        '''If `variable` is unbound in the environment, signals an error, 
        otherwise changes the binding of `variable` to `value`.
        '''
        for frame in self.frames:
            if variable in frame:
                frame[variable] = value
                return 
        else:
            raise NameError("Unbound variable {}".format(variable))
        #sys.exit("Unbound variable {} in environment.set_variable_value".format(variable)) 

    def get_binding(self, variable):
        '''Return the value that is bound to the symbol `variable` in the environment,
        or signals an error if `variable` is Unbound
        '''
        for frame in self.frames:
            if variable in frame:
                return frame[variable]
        else:
            raise NameError("Unbound variable {}".format(variable))
        #sys.exit("Unbound variable {} in environment.set_variable_value".format(variable)) 

    def extend_environment(self, variables, values):
        """Create an new environment that uses current environment as
        enclosing_environment, and uses `variables` and `values` to
        create the first frame of the new environment.
        
        `variable`: iterable
        `value`: iterable
        """
        if len(variables) != len(values):
            raise ExtendEnvironmentError("Length of variables is not equal to length of values")
        else:
            return Environment(variables, values, self)

    def define_binding(self, variable, value):
        '''Adds to the first frame in the environment a new binding that 
        associates `variable` with `value`
        '''
        self.first_frame[variable] = value
