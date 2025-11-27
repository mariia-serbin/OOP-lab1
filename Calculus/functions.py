import math
import json
import work_with_sage
from lists import ArrayList

class Function:
    """
    Class for functions.
    """
    def __init__(self, expression, variables=["x"], list_type=ArrayList):
        self.expression = expression
        self.variables = variables
        self.list_type = list_type

    # -------------------- A --------------------
    def get_expression(self):
        return self.expression

    def set_expression(self, expr):
        self.expression = expr

    def get_variables(self):
        return self.variables

    def set_variables(self, vars_list):
        self.variables = vars_list

    # --------------------B--------------------
    def evaluate(self, **kwargs):
        """Чисельне обчислення значення функції"""
        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = {var: kwargs.get(var, 0) for var in self.variables}
        return eval(self.expression, safe_globals, safe_locals)

    def _is_increasing(self, var, start=0, steps=10, h=1e-5):
        """Чисельна перевірка, чи зростає функція по одній змінній"""
        for i in range(steps):
            x1 = start + i
            x2 = x1 + h
            vals = {v: 0 for v in self.variables}
            vals[var] = x1
            f1 = self.evaluate(**vals)
            vals[var] = x2
            f2 = self.evaluate(**vals)
            if f2 - f1 < 0:
                return False
        return True

    def _is_decreasing(self, var, start=0, steps=10, h=1e-5):
        for i in range(steps):
            x1 = start + i
            x2 = x1 + h
            vals = {v: 0 for v in self.variables}
            vals[var] = x1
            f1 = self.evaluate(**vals)
            vals[var] = x2
            f2 = self.evaluate(**vals)
            if f2 - f1 > 0:
                return False
        return True

    def is_monotonic(self, var=None, is_increasing=None):
        """Перевірка монотонності функції по змінній"""
        if var is None and len(self.variables) == 1:
            var = self.variables[0]
        if is_increasing is None:
            return self._is_increasing(var) or self._is_decreasing(var)
        elif is_increasing:
            return self._is_increasing(var)
        else:
            return self._is_decreasing(var)

    def is_bounded(self, var=None, start=0, stop=10, step=1):
        """Чисельна перевірка обмеженості функції"""
        results = self.list_type()
        if var is None and len(self.variables) == 1:
            var = self.variables[0]
        for i in range(int((stop - start)/step)):
            x = start + i * step
            vals = {v: 0 for v in self.variables}
            vals[var] = x
            val = self.evaluate(**vals)
            if math.isfinite(val):
                results.add(val)
        max_val = results.max()
        min_val = results.min()
        if max_val is None or min_val is None:
            return False, None, None
        return True, max_val, min_val

    def approximate_limit(self, var=None, n0=1000, iterate=1000, eps=1e-6, overflow=1e6):
        """Чисельне наближення ліміту при x -> inf"""
        if var is None and len(self.variables) == 1:
            var = self.variables[0]
        n = n0
        vals = {v: 0 for v in self.variables}
        vals[var] = n
        prev = self.evaluate(**vals)
        for _ in range(iterate):
            n += 1
            vals[var] = n
            curr = self.evaluate(**vals)
            if curr > overflow and curr > prev:
                return float('inf')
            if curr < -overflow and curr < prev:
                return float('-inf')
            if abs(curr - prev) < eps:
                return curr
            prev = curr
        return None

    # -------------------- Рівень C: символьні методи через Sage --------------------
    def sym_limit(self, var=None):
        if var is None and len(self.variables) == 1:
            var = self.variables[0]
        code = f"""
from sage.all import *
{var} = var('{var}')
print(limit({self.expression}, {var}, oo))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def derivative(self, var=None):
        """Похідна функції однієї змінної"""
        if len(self.variables) > 1:
            raise ValueError("Use other methods working with functions with more than one variable.")
        if var is None:
            var = self.variables[0]
        code = f"""
from sage.all import *
{var} = var('{var}')
f = {self.expression}
print(diff(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def partial_derivative(self, var):
        """Часткова похідна для однієї змінної"""
        if var not in self.variables:
            raise ValueError(f"Змінної {var} немає у списку змінних")
        code = f"""
from sage.all import *
{var} = var('{var}')
{', '.join(self.variables)} = var('{', '.join(self.variables)}')
f = {self.expression}
print(diff(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def gradient(self):
        """Вектор похідних"""
        vars_str = ', '.join(self.variables)
        code = f"""
    from sage.all import *
    {vars_str} = var('{vars_str}')
    f = {self.expression}
    print([{', '.join([f'diff(f, {v})' for v in self.variables])}])
    """
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def integral(self, var=None):
        """Символьний інтеграл для однієї змінної"""
        if var is None and len(self.variables) == 1:
            var = self.variables[0]
        if len(self.variables) > 1:
            raise ValueError("Інтеграл реалізований тільки для однієї змінної")
        code = f"""
from sage.all import *
{var} = var('{var}')
f = {self.expression}
print(integral(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    # -------------------- Експорт --------------------
    def export_to_json(self, path=r'results_function.json'):
        data = {
            "expression": self.expression,
            "variables": self.variables,
            "approx_limit": self.approximate_limit(),
            "monotonic": self.is_monotonic(),
            "bounded": self.is_bounded(),
            "sym_limit": self.sym_limit(),
            "derivative": self.derivative(),
            "gradient": self.gradient()
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
