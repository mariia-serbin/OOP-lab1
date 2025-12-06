"""!
@file function.py
@brief Implements the Function class for numerical and symbolic computations.

@details
This file contains the `Function` class which allows:
- numerical evaluation of mathematical expressions,
- monotonicity and boundedness checks,
- numerical limit approximation,
- symbolic differentiation (full and partial),
- symbolic integration,
- symbolic limit calculation using SageMath,
- gradient computation,
- plotting using Matplotlib,
- exporting results to JSON.
@author
Maria Serbin
@date
06.12.2025
"""

import math
import json
import work_with_sage
from lists import ArrayList
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional, Dict, Union, Tuple, Type

class Function:
    """!
    @class Function
    @brief Represents a mathematical function defined by a string expression.

    @details
    This class provides both numerical and symbolic tools for working with mathematical
    functions of one or multiple variables. A function is internally stored as a string
    expression (for example, "sin(x) + x^2"), and evaluated or manipulated through
    numerical routines (using Python) and symbolic routines (delegated to SageMath).

    The class supports:
    - numerical evaluation of the function,
    - monotonicity checks,
    - boundedness checks,
    - numerical limit approximation as the variable tends to infinity,
    - symbolic differentiation (full and partial),
    - symbolic integration,
    - symbolic limit computation,
    - gradient computation,
    - exporting computed results into JSON.

    Variables used inside the expression must be provided in the constructor or will
    default to ["x"].

    The internal list structure for boundedness analysis can be customized by providing
    a list implementation with `add()`, `max()`, and `min()` methods.
    """

    def __init__(self, expression: str, variables: Optional[List[str]], list_type: Type =ArrayList) -> None:
        self._expression: str = expression
        if variables is None:
            self._variables: List[str] = ["x"]
        else:
            self._variables: List[str] = variables

        self._list_type: Type = list_type

    # -------------------- A --------------------
    def get_expression(self) -> str:
        """!
        @brief Returns the stored function expression.

        @return String representing the function expression.
        """

        return self._expression

    def set_expression(self, expr: str) -> None:
        """!
        @brief Updates the stored function expression.

        @param expr The new expression string.
        """

        self._expression = expr

    def get_variables(self) -> List[str]:
        """!
        @brief Returns the list of variables used in the function.

        @return A list of variable names.
        """

        return self._variables

    def set_variables(self, vars_list: List[str]) -> None:
        """!
        @brief Updates the list of variables used in the function.

        @param vars_list A list of variable names.
        """
        self._variables = vars_list

    # --------------------B--------------------
    def evaluate(self, **kwargs: float) -> float:
        """!
        @brief Numerically evaluates the function for the given variable values.

        @details
        This method substitutes values for the function's variables and evaluates
        the expression in a restricted execution environment (no builtins). Variables
        that are not explicitly provided are assumed to be zero.

        @param kwargs A mapping between variable names and numerical values.

        @return The numerical result of evaluating the function.

        @warning
        The evaluation uses Python's `eval()` in a restricted environment. Although
        controlled, the expression must still be mathematically valid Python code
        (e.g., "math.sin(x)" or "x**2 + 3").
        """

        safe_globals: Dict[str, None] = {"__builtins__": None, "math": math}
        safe_locals: Dict[str, float] = {var: float(kwargs.get(var, 0)) for var in self._variables}
        return eval(self._expression, safe_globals, safe_locals)

    def _is_increasing(self, var: str, start: float = 0, steps: int = 10, h: float =1e-5) -> bool:
        for i in range(steps):
            x1: float = start + i
            x2: float = x1 + h
            vals: Dict[str, float] = {v: 0 for v in self._variables}
            vals[var] = x1
            f1: float = self.evaluate(**vals)
            vals[var] = x2
            f2 = self.evaluate(**vals)
            if f2 - f1 < 0:
                return False
        return True

    def _is_decreasing(self, var: str, start: float = 0, steps: int = 10, h: float = 1e-5) -> bool:
        for i in range(steps):
            x1: float = start + i
            x2:float = x1 + h
            vals: Dict[str, float] = {v: 0 for v in self._variables}
            vals[var] = x1
            f1: float = self.evaluate(**vals)
            vals[var] = x2
            f2 = self.evaluate(**vals)
            if f2 - f1 > 0:
                return False
        return True

    def is_monotonic(self, var: Optional[str] = None, is_increasing: Optional[bool] = None) -> bool:
        """!
        @brief Determines whether the function is monotonic in the given variable.

        @details
        If `var` is not provided and the function has only one variable, that variable is used.
        If `is_increasing` is None, the method detects whether the function is either increasing
        or decreasing. Otherwise, it checks only one of the two directions.

        @param var Variable name to test monotonicity in.
        @param is_increasing
            - True: check strictly for increasing behavior
            - False: check strictly for decreasing
            - None: check whether the function is monotonic in any direction

        @return True if monotonic under the chosen criteria, False otherwise.
        """
        if var is None and len(self._variables) == 1:
            var = self._variables[0]
        if is_increasing is None:
            return self._is_increasing(var) or self._is_decreasing(var)
        elif is_increasing:
            return self._is_increasing(var)
        else:
            return self._is_decreasing(var)

    def is_bounded(self, var: Optional[str] = None, start: float = 0, stop: float = 10000, step: float = 100) -> Tuple[bool, Optional[float], Optional[float]]:
        """!
        @brief Numerically checks whether the function is bounded over a given interval.

        @details
        The method evaluates the function at a discrete set of points on the interval
        [start, stop) using a custom list implementation. Only finite values are considered.

        @param var Variable to vary. If None and the function has a single variable,
        it is used automatically.
        @param start Beginning of the interval.
        @param stop End of the interval.
        @param step Sampling step.

        @return A tuple (is_bounded, max_value, min_value) where:
            - is_bounded: True if both max and min exist,
            - max_value: maximum encountered value or None,
            - min_value: minimum encountered value or None.
        """
        results = self._list_type()
        if var is None and len(self._variables) == 1:
            var = self._variables[0]
        for i in range(int((stop - start)/step)):
            x: float = start + i * step
            vals: Dict[str, float] = {v: 0 for v in self._variables}
            vals[var] = x
            val: float = self.evaluate(**vals)
            if math.isfinite(val):
                results.add(val)
        max_val: Optional[float] = results.max()
        min_val: Optional[float] = results.min()
        if max_val is None or min_val is None:
            return False, None, None
        elif max_val > 1e6:
            return False, None, None
        return True, max_val, min_val

    def approximate_limit(self, var: Optional[str] = None,
                          point: Union[float, str] =float('inf'),
                          n0: int = 1000,
                          iterate: int = 1000,
                          eps: float = 1e-6,
                          step: float = 1,
                          overflow: float=1e6) -> Optional[float]:
        """!
        Numerically approximates the limit of the function as the variable approaches a given point.

        @param var Name of the variable to approach. If None and the function has a single variable, it is set automatically.
        @param point Target point for the limit. Can be a finite number or +/- infinity (float('inf') or float('-inf')).
        @param n0 Starting point for iteration (used for infinite points).
        @param iterate Number of iterations for the approximation.
        @param eps Convergence threshold. If |f(x_next) - f(x_current)| < eps, the limit is considered reached.
        @param step Step size for approaching finite points.
        @param overflow Threshold to detect divergence to infinity.

        @return Approximated limit as a float, float('inf'), float('-inf'), or None if convergence is not reached.

        @details
        The function samples points near the target and checks for stabilization of values.
        For finite points, it evaluates f(point ± h) iteratively.
        For infinite points, it increases or decreases n starting from n0.
        """
        if var is None and len(self._variables) == 1:
            var = self._variables[0]

        vals: Dict[str, float] = {v: 0 for v in self._variables}

        # Handle limit to +infinity
        if point == float('inf'):
            n: int = n0
            vals[var] = n
            prev: float = self.evaluate(**vals)
            for _ in range(iterate):
                n += 1
                vals[var] = n
                curr: float = self.evaluate(**vals)
                if curr > overflow and curr > prev:
                    return float('inf')
                if abs(curr - prev) < eps:
                    return curr
                prev = curr
            return None

        # Handle limit to -infinity
        elif point == float('-inf'):
            n: int = -n0
            vals[var] = n
            prev: float = self.evaluate(**vals)
            for _ in range(iterate):
                n -= 1
                vals[var] = n
                curr: float = self.evaluate(**vals)
                if curr < -overflow and curr < prev:
                    return float('-inf')
                if abs(curr - prev) < eps:
                    return curr
                prev = curr
            return None

        # Handle finite points
        else:
            h: float = step
            prev: float = self.evaluate(**{**vals, var: point - h})
            for i in range(iterate):
                curr: float = self.evaluate(**{**vals, var: point - h / (2 ** i)})
                if abs(curr - prev) < eps:
                    return curr
                prev = curr
            return None

    # -------------------- Рівень C: символьні методи через Sage --------------------
    def sym_limit(self, var=None, point=None):
        """!
        Computes the symbolic limit of the function as the variable approaches a given point.

        @param var Name of the variable to approach. If None and the function has a single variable, it is set automatically.
        @param point Target point for the limit. Can be a finite number or 'oo'/'-oo' for infinity.
                      If None, defaults to +infinity.

        @return Symbolic limit as computed by Sage.

        @details
        This method constructs Sage code to compute the limit of the expression symbolically.
        Supports finite points and ±infinity.
        """
        if var is None and len(self._variables) == 1:
            var = self._variables[0]

        # Default to infinity if point is None
        if point is None:
            point = 'oo'

        # Convert Python float('inf') or float('-inf') to Sage notation
        if point == float('inf'):
            point_sage = 'oo'
        elif point == float('-inf'):
            point_sage = '-oo'
        else:
            point_sage = str(point)

        code = f"""
    from sage.all import *
    {var} = var('{var}')
    f = {self._expression}
    print(limit(f, {var}, {point_sage}))
    """
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def derivative(self, var=None):
        """!
        @brief Computes the symbolic derivative of a single-variable function.

        @details
        If the function uses more than one variable, an exception is raised. The result
        is obtained through SageMath and returned as a string.

        @param var Variable to differentiate with respect to.

        @return A string with the symbolic derivative.

        @throws ValueError If the function has more than one variable.
        """
        if len(self._variables) > 1:
            raise ValueError("Use other methods working with functions with more than one variable.")
        if var is None:
            var = self._variables[0]
        code = f"""
from sage.all import *
{var} = var('{var}')
f = {self._expression}
print(diff(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def partial_derivative(self, var):
        """!
        @brief Computes the symbolic partial derivative with respect to a variable.

        @details
        A SageMath script is generated where all variables are declared symbolically
        and the derivative with respect to the specified one is computed.

        @param var Variable with respect to which the derivative is taken.

        @return A string returned by SageMath containing the derivative.

        @throws ValueError If the requested variable is not present.
        """
        if var not in self._variables:
            raise ValueError(f"Змінної {var} немає у списку змінних")
        code = f"""
from sage.all import *
{var} = var('{var}')
{', '.join(self._variables)} = var('{', '.join(self._variables)}')
f = {self._expression}
print(diff(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def gradient(self):
        """!
        @brief Computes the symbolic gradient vector of the function.

        @details
        Generates a SageMath script that constructs a list of partial derivatives,
        one for each variable defined in the function.

        @return A string representing the gradient vector.
        """
        vars_str = ', '.join(self._variables)
        code = f"""
    from sage.all import *
    {vars_str} = var('{vars_str}')
    f = {self._expression}
    print([{', '.join([f'diff(f, {v})' for v in self._variables])}])
    """
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def integral(self, var=None):
        """!
        @brief Computes the symbolic integral of a single-variable function.

        @details
        Performs symbolic integration using SageMath. Multi-variable functions are
        not supported and will raise an exception.

        @param var Variable of integration.

        @return A string containing the integral computed by SageMath.

        @throws ValueError If the function uses more than one variable.
        """
        if var is None and len(self._variables) == 1:
            var = self._variables[0]
        if len(self._variables) > 1:
            raise ValueError("Інтеграл реалізований тільки для однієї змінної")
        code = f"""
from sage.all import *
{var} = var('{var}')
f = {self._expression}
print(integral(f, {var}))
"""
        sage = work_with_sage.SageRemote()
        return sage.run_code(code)

    def plot(self, var=None, start=0, stop=10, num_points=1000, title=None, xlabel=None, ylabel=None):
        """!
        Plots the function using Matplotlib.

        @param var Variable to plot (if None and the function has a single variable, it is used automatically).
        @param start Start of the range for the variable (default: 0).
        @param stop End of the range for the variable (default: 10).
        @param num_points Number of points to sample in the range (default: 1000).
        @param title Title of the plot (optional).
        @param xlabel Label for the x-axis (optional).
        @param ylabel Label for the y-axis (optional).

        @details
        Generates a plot of the function over the specified range using NumPy to create
        sample points and Matplotlib to visualize the function.
        """
        if var is None and len(self._variables) == 1:
            var = self._variables[0]

        x_vals = np.linspace(start, stop, num_points)
        y_vals = np.array([self.evaluate(**{var: x}) for x in x_vals])

        plt.figure(figsize=(8, 5))
        plt.plot(x_vals, y_vals, label=self._expression)
        plt.grid(True)

        if title:
            plt.title(title)
        if xlabel:
            plt.xlabel(xlabel)
        else:
            plt.xlabel(var)
        if ylabel:
            plt.ylabel(ylabel)
        else:
            plt.ylabel(f"f({var})")

        plt.legend()
        plt.show()

    # -------------------- Експорт --------------------
    def export_to_json(self, path: str =r'results_function.json') -> None:
        """!
        @brief Exports various numerical and symbolic properties of the function to JSON.

        @details
        The exported data includes:
        - function expression,
        - variable list,
        - numerical limit approximation,
        - monotonicity check,
        - boundedness check,
        - symbolic limit,
        - symbolic derivative,
        - gradient vector.

        @param path Path to the JSON file where results will be stored.

        @return None.
        """
        data: Dict[str, Union[str, List[str], bool, Optional[float]]] = {
            "expression": self._expression,
            "variables": self._variables,
            "approx_limit": self.approximate_limit(),
            "monotonic": self.is_monotonic(),
            "bounded": self.is_bounded(),
            "sym_limit": self.sym_limit(),
            "derivative": self.derivative(),
            "gradient": self.gradient()
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
