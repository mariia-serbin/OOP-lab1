from lists import ArrayList
import math
import json
import work_with_sage


class Sequence:
    """Клас для послідовностей"""
    def __init__(self, expression, variable="n", list_type = ArrayList):
        self.expression = expression
        self.variable = variable
        self.list_type = list_type

    # -------------------- Рівень A --------------------
    def get_expression(self):
        return self.expression

    def set_expression(self, expr):
        self.expression = expr

    def get_variable(self):
        return self.variable

    def set_variable(self, var):
        self.variable = var

    # -------------------- Рівень B --------------------
    def evaluate(self, n):
        """Чисельна оцінка елемента послідовності"""

        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = {self.variable: n}
        result = eval(self.expression, safe_globals, safe_locals)

        return result

    def _is_increasing(self, n=1000, steps = 10):
        for i in range(steps):
            if self.evaluate(n + i + 1) - self.evaluate(n + i) < 0:
                return False

        return True

    def _is_decreasing(self, n=1000, steps = 10):
        for i in range(steps):
            if self.evaluate(n + i + 1) - self.evaluate(n + i) > 0:
                return False

        return True

    def is_monotonic(self, is_increasing = None):
        if is_increasing is None:
            if self._is_increasing() or self._is_decreasing():
                return True
        elif is_increasing:
            if self._is_increasing():
                return True
        elif not is_increasing:
            if self._is_decreasing():
                return True

        return False

    def is_bounded(self, start = 100, stop = 300, step = 1):
        results = self.list_type()
        for i in range(int((stop - start) / step)):
            x = start + i * step
            value = self.evaluate(x)
            if math.isfinite(value):
                results.add(value)
            else:
                continue

        max_value = results.max()
        min_value = results.min()

        if max_value is None or min_value is None:
            return False, None, None
        return True, max_value, min_value


    def approximate_limit(self, eps = 1e-6, n0= 1000, iterate = 1000, overflow = 1e6):
        n = n0
        prev = self.evaluate(n)
        for i in range(0, iterate):
            n += 1
            curr = self.evaluate(n)
            if curr > overflow and curr > prev:
                return float('inf')
            if curr < -overflow and curr < prev:
                return float('-inf')

            if abs(curr - prev) < eps:
                return curr

            prev = curr

        return None
  # -------------------- Рівень C --------------------
    def sym_limit(self):
        code = f"""
from sage.all import *
{self.variable} = var('{self.variable}')
print(limit({self.expression}, {self.variable}, oo))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def export_to_json(self, path = r'C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\results.json'):
        data = {
            "expression": self.expression,
            "variable": self.variable,
            "approx_limit": self.approximate_limit(),
            "monotonic": self.is_monotonic(),
            "bounded": self.is_bounded(),
            "sym_limit": self.sym_limit()
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
