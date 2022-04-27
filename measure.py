'''
This module defines the Measurement class. Every measurement has
a value and an uncertainty. All basic math operators are overloaded
to properly propagate uncertainty and return a new Measurement.
'''

import numpy as np
import matplotlib.pyplot as plt

class Measurement:
    def __init__(self, val, unc):
        '''
        Initialization function. Set value and uncertainty.
        '''
        self.val = val
        self.unc = unc

    def __str__(self):
        '''
        Define string representation of a Measurement
        '''
        return (str(self.val) + ' +- ' + str(self.unc))

    def __eq__(self, other):
        '''
        Check for equality between both the value and the uncertainty
        '''
        return self.val == other.val and self.unc == other.unc

    def __add__(self, other):
        '''
        Overload add to also calculate uncertainty and return
        a Measurement.
        '''
        if hasattr(other, 'val'):
            newval = self.val + other.val
            newunc = (self.unc**2 + other.unc**2)**.5
            return Measurement(newval, newunc)
        else:
            newval = self.val + other
            newunc = self.unc
            return Measurement(newval, newunc)

    def __radd__(self, other):
        '''
        Refer right addition back to the add function.
        '''
        return Measurement.__add__(self, other)

    def __sub__(self, other):
        '''
        Overload subtract to also calculate uncertainty and return
        a Measurement.
        '''
        if hasattr(other, 'val') and hasattr(self, 'val'):
            newval = self.val - other.val
            newunc = (self.unc**2 + other.unc**2)**.5
            return Measurement(newval, newunc)
        elif hasattr(other, 'val') and not hasattr(self, 'val'):
            newval = self - other.val
            newunc = other.unc
            return Measurement(newval, newunc)
        elif not hasattr(other, 'val') and hasattr(self, 'val'):
            newval = self.val - other
            newunc = self.unc 
            return Measurement(newval, newunc)

    def __rsub__(self, other):
        '''
        Refer right subtraction back to the subtract function.
        '''
        return Measurement.__sub__(other, self)

    def __mul__(self, other):
        '''
        Overload multiply to also calculate uncertainty and return
        a Measurement.
        '''       
        if hasattr(other, 'val'):
            newval = self.val * other.val
            newunc = newval * ( self.unc**2 /  self.val**2 +
                               other.unc**2 / other.val**2)**.5
            return Measurement(newval, newunc)
        else:
            newval = self.val * other
            newunc = self.unc * other
            return Measurement(newval, newunc)

    def __rmul__(self, other):
        '''
        Refer right multiplication back to the add function.
        '''
        return Measurement.__mul__(self, other)

    def __truediv__(self, other):
        '''
        Overload division to also calculate uncertainty and return
        a Measurement.
        '''
        if   hasattr(other, 'val') and hasattr(self, 'val'):
            newval = self.val / other.val
            newunc = newval *  ( self.unc**2 /  self.val**2 +
                                other.unc**2 / other.val**2)**.5
            return Measurement(newval, newunc)           
        elif hasattr(other, 'val') and not hasattr(self, 'val'):
            newval = self / other.val
            newunc = self / other.val**2 * other.unc
            return Measurement(newval, newunc)
        elif not hasattr(other, 'val') and hasattr(self, 'val'):
            newval = self.val / other
            newunc = self.unc / other
            return Measurement(newval, newunc)

    def __rtruediv__(self, other):
        '''
        Refer right division back to the add function.
        '''
        return Measurement.__truediv__(other, self)

    def __pow__(self, other):
        '''
        Overload power to also calculate uncertainty and return
        a Measurement.
        '''
        if not hasattr(self, 'val'):
            a    = self
            unca = 0.
        if not hasattr(other, 'val'):
            b    = other
            uncb = 0.
        if hasattr(self, 'val'):
            a    = self.val
            unca = self.unc
        if hasattr(other, 'val'):
            b    = other.val
            uncb = other.unc
        newval = a**b
        newunc = (unca**2*b**2*a**(2*b-2) + uncb**2*a**(2*b)*np.log(a)**2)**.5
        return Measurement(newval, newunc) 
                      
    def __rpow__(self, other):
        '''
        Refer right power back to the add function.
        '''
        return Measurement.__pow__(other, self)

    

