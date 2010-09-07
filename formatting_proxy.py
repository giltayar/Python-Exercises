"""\
Used in alert formatting. Allows administrators to set a format string that formats alerts 
nicely with all the parameters given by the program.
The added value over simple formatting is that if the administrator tries to use a parameter 
that isn't provided for that alert, it is handled gracefully, and also any parameters
that the administrator didn't specify in the format string are still shown, using a generic
format.

See the unit tests for more details on how this behaves.
"""
