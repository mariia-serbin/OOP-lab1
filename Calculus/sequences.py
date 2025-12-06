"""!
@file sequences.py
@brief Module for working with mathematical sequences.
@details Contains the `Sequence` class for representing, evaluating, and analyzing numerical and symbolic sequences.
         Provides methods to evaluate sequence elements, check monotonicity, determine boundedness, approximate limits,
         compute symbolic limits using SageMath, and export results to JSON. Supports sequences based on any list
         implementation derived from `BaseList` (default is `ArrayList`).
@author
Maria Serbin
@date
06.12.2025
"""

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
        """!
        @brief Returns the sequence expression.
        @return The mathematical expression of the sequence.
        @par Example:
        @code
        expr = seq.get_expression()
        @endcode
        """
        return self.expression

    def set_expression(self, expr: str):
        """!
        @brief Sets a new expression for the sequence.
        @param expr New mathematical expression.
        @par Example:
        @code
        seq.set_expression("1/n^2")
        @endcode
        """
        self.expression: str = expr

    def get_variable(self)-> str:
        """!
        @brief Returns the variable used in the sequence expression.
        @return The variable name as a string.
        @par Example:
        @code
        var_name = seq.get_variable()
        @endcode
        """
        return self.variable

    def set_variable(self, var: str):
        """!
        @brief Sets a new variable for the sequence expression.
        @param var Variable name as a string.
        @par Example:
        @code
        seq.set_variable("k")
        @endcode
        """
        self.variable: str = var

    # -------------------- Рівень B --------------------
    def evaluate(self, n: float) -> float:
        """!
        @brief Evaluates the sequence at a specific value.
        @param n Value of the sequence variable.
        @return Numerical value of the sequence element.
        @par Example:
        @code
        val = seq.evaluate(5)
        @endcode
        """
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
        """!
        @brief Checks whether the sequence is monotonic.
        @param is_increasing If True, checks increasing; if False, checks decreasing; if None, checks any monotonicity.
        @return True if monotonic, False otherwise.
        @par Example:
        @code
        seq.is_monotonic()
        seq.is_monotonic(True)  # check increasing
        @endcode
        """
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
        """!
        @brief Checks if the sequence is bounded in a given range.
        @param start Starting value of evaluation.
        @param stop Ending value of evaluation.
        @param step Step size for evaluation.
        @return Tuple (is_bounded, max_value, min_value)
        @par Example:
        @code
        seq.is_bounded(1, 100, 1)
        @endcode
        """
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
        """!
        @brief Approximates the limit of the sequence numerically.
        @param eps Tolerance for convergence.
        @param n0 Starting index for evaluation.
        @param iterate Number of iterations.
        @param overflow Maximum value to consider as infinite.
        @return Approximated limit or None if it cannot be determined.
        @par Example:
        @code
        seq.approximate_limit()
        @endcode
        """
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
        """!
        @brief Computes the symbolic limit of the sequence using SageMath.
        @return Symbolic limit computed by SageMath.
        @par Example:
        @code
        seq.sym_limit()
        @endcode
        """
        code = f"""
from sage.all import *
{self.variable} = var('{self.variable}')
print(limit({self.expression}, {self.variable}, oo))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def export_to_json(self, path: str = r'C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\results.json'):

        """!
        @brief Exports sequence information to a JSON file.
        @param path File path for saving the JSON file.
        @par Example:
        @code
        seq.export_to_json("results.json")
        @endcode
        """
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
