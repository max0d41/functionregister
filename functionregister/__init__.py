import bisect


class FunctionRegister(object):
    def __init__(self):
        self.functions = dict()
        self.functions_by_priority = list()

    def add(self, func, name=None, prefix=None, postfix=None, priority=None, overwrite=False, **kwargs):
        if name is None:
            name = '{}.{}'.format(func.__module__, func.__name__)
        if prefix is not None:
            name += '@'+prefix
        if postfix is not None:
            name += '@'+postfix
        if not overwrite and name in self.functions:
            raise RuntimeError('function already exists: {}'.format(name))
        func = self.decorate_function(func, name, **kwargs)
        if isinstance(func, (list, tuple)):
            func, stored_func = func
            self.functions[name] = stored_func
        else:
            self.functions[name] = func
        bisect.insort(self.functions_by_priority, (priority, func))
        return func

    def register(self, name=None, prefix=None, postfix=None, priority=None, overwrite=False, **kwargs):
        if callable(name):
            return self.add(name, None, prefix, postfix, priority, **kwargs)
        else:
            return lambda func: self.add(func, name, prefix, postfix, priority, **kwargs)

    def decorate_function(self, func, name, **kwargs):
        """This function can have two different return values.
        1. A callable (the original function or anything other)
        2. A list or tuple containing two callables. The first callable is returned by the
           add or register function, the second one is stored in this class.
        """
        raise NotImplementedError()

    def get_function(self, name):
        if name not in self.functions:
            raise KeyError('Function "%s" does not exists' % name)
        return self.functions[name]

    def iter_functions(self):
        for priority, func in self.functions_by_priority:
            yield func
