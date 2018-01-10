from flask import request

#Decorator will add arg to missing_args if conditions aren't met
class append_missing():
    def __init__(self):
        self.missing_args = []
        self.available_args = {}

    def confirm(self):
        def wrapper(f):
            if f(request.args.get(f.__name__)):
                self.available_args[f.__name__] = request.args.get(f.__name__)
            else:
                self.missing_args.append(f.__name__)
        return wrapper
