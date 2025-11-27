from lists import ArrayList
import math
import json
import work_with_sage

class Series:
    """Клас для числових рядів: збіжність і розклади Тейлора"""

    def __init__(self, expression, variable="n", list_type=ArrayList):
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
    def term(self, n):
        """Обчислює n-й член ряду"""
        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = {self.variable: n}
        return eval(self.expression, safe_globals, safe_locals)

    def is_convergent(self, eps=1e-6, max_iter=10000):
        """Приблизна перевірка збіжності через часткові суми"""
        s = 0
        for n in range(1, max_iter + 1):
            term_value = self.term(n)
            s += term_value
            if abs(term_value) < eps:
                return True
        return False

    # -------------------- Рівень C --------------------
    def taylor_series(self, x='x', order=5):
        """Розклад у ряд Тейлора через SageMath"""
        code = f"""
from sage.all import *
{self.variable} = var('{self.variable}')
{x} = var('{x}')
f = {self.expression}
taylor(f, {x}, 0, {order})
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def export_to_json(self, path=r'C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\series_results.json', order=5):
        data = {
            "expression": self.expression,
            "variable": self.variable,
            "convergent": self.is_convergent(),
            "taylor_series": self.taylor_series(order=order)
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
