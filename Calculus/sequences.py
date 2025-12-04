from lists import *
import math
import json
import work_with_sage
from typing import Optional, Tuple, Any, Type


class Sequence:
    """Клас для послідовностей"""
    def __init__(self, expression: str,
                 variable: str = "n",
                 list_type: Type[ArrayList] = ArrayList):
        self.expression: str = expression
        self.variable: str = variable
        self.list_type: Type[ArrayList] = list_type

    # -------------------- Рівень A --------------------
    def get_expression(self) -> str:
        return self.expression

    def set_expression(self, expr: str):
        self.expression: str = expr

    def get_variable(self)-> str:
        return self.variable

    def set_variable(self, var: str):
        self.variable: str = var

    # -------------------- Рівень B --------------------
    def evaluate(self, n: float) -> float:
        """Чисельна оцінка елемента послідовності"""

        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = {self.variable: n}
        result: float = eval(self.expression, safe_globals, safe_locals)

        return result

    def _is_increasing(self, n: int = 1000, steps: int = 10) -> bool:
        for i in range(steps):
            if self.evaluate(n + i + 1) - self.evaluate(n + i) < 0:
                return False

        return True

    def _is_decreasing(self, n: int = 1000, steps: int = 10) -> bool:
        for i in range(steps):
            if self.evaluate(n + i + 1) - self.evaluate(n + i) > 0:
                return False

        return True

    def is_monotonic(self, is_increasing: Optional[bool] = None) -> bool:
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

    def is_bounded(self, start: float = 100, stop: float = 300, step: float = 1) -> Tuple[bool, Optional[float], Optional[float]]:
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


    def approximate_limit(self, eps: float = 1e-6,
                          n0: float= 1000,
                          iterate: int = 1000,
                          overflow: float = 1e6) -> Optional[float]:
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
    def sym_limit(self) -> Any:
        code = f"""
from sage.all import *
{self.variable} = var('{self.variable}')
print(limit({self.expression}, {self.variable}, oo))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def export_to_json(self, path: str = r'C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\results.json'):
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
