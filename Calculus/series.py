from lists import ArrayList
import math
import json
import work_with_sage

class Series:
    """
    @class Series
    @brief Class for numerical series: convergence checking and Taylor expansions.

    @details
    This class provides tools to work with numerical series defined by a general expression.
    It allows:
      - Evaluating individual terms
      - Approximate convergence checking via partial sums
      - Computing Taylor series expansions via SageMath
      - Exporting results to JSON
    """

    def __init__(self, expression, variable="n", list_type=ArrayList):
        self._expression = expression
        self._variable = variable
        self._list_type = list_type

    # -------------------- Рівень A --------------------
    def get_expression(self):
        """
        @brief Returns the expression of the series.
        @return String representing the series expression.
        """
        return self._expression

    def set_expression(self, expr):
        """
        @brief Sets a new expression for the series.
        @param expr String expression representing the new series term.
        """
        self._expression = expr

    def get_variable(self):
        """
        @brief Returns the variable name used in the series expression.
        @return String representing the variable name.
        """
        return self._variable

    def set_variable(self, var):
        """
        @brief Sets a new variable name for the series expression.
        @param var String representing the new variable name.
        """
        self._variable = var

    # -------------------- Рівень B --------------------
    def term(self, n):
        """
        @brief Computes the nth term of the series.

        @param n Index of the term to evaluate (integer, n >= 1).
        @return Float representing the value of the nth term.

        @details
        Evaluates the expression safely using a restricted environment with only math
        functions available. Returns the numeric value corresponding to the nth term.
        """

        safe_globals = {"__builtins__": None, "math": math}
        safe_locals = {self._variable: n}
        return eval(self._expression, safe_globals, safe_locals)

    def is_convergent(self, eps=1e-6, max_iter=10000):
        """
        @brief Approximates convergence of the series using partial sums.

        @param eps Threshold for convergence: if the absolute value of a term falls below eps,
                   the series is considered approximately convergent.
        @param max_iter Maximum number of terms to evaluate (default: 10000).

        @return Boolean indicating approximate convergence: True if convergent, False otherwise.

        @details
        Iterates over terms of the series, summing them sequentially. Convergence is assumed
        when the absolute value of a term becomes smaller than eps. This provides only a
        numerical approximation and may not detect all divergent series.
        """
        s = 0
        for n in range(1, max_iter + 1):
            term_value = self.term(n)
            s += term_value
            if abs(term_value) < eps:
                return True
        return False

    # -------------------- Рівень C --------------------
    def taylor_series(self, x='x', order=5):
        """
        @brief Computes the Taylor series expansion of a function using SageMath.

        @param x Symbolic variable to expand around (default: 'x').
        @param order Order of the Taylor series expansion (default: 5).
        @return String or SageMath object representing the Taylor expansion.

        @details
        Generates a SageMath script to compute the Taylor series expansion of the series
        expression (interpreted as a function of the symbolic variable x) around 0. The
        method communicates with a SageMath server via the SageRemote interface.

        @note
        The method requires SageMath to be available remotely.
        """
        code = f"""
from sage.all import *
{self._variable} = var('{self._variable}')
{x} = var('{x}')
f = {self._expression}
taylor(f, {x}, 0, {order})
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def export_to_json(self, path=r'C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\series_results.json', order=5):
        """
        @brief Exports series data to a JSON file.

        @param path Path to the output JSON file.
        @param order Order of the Taylor series to compute and include.

        @details
        The JSON file will include:
          - The series expression
          - The variable name
          - Boolean indicating approximate convergence
          - Taylor series expansion up to the specified order

        @note
        Uses is_convergent and taylor_series methods internally to gather data.
        """
        data = {
            "expression": self._expression,
            "variable": self._variable,
            "convergent": self.is_convergent(),
            "taylor_series": self.taylor_series(order=order)
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
