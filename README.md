# OOP-lab1
# Computational Math & Sorting System

## Overview
This project is a console-based computational system that provides tools for working with mathematical sequences, series, and functions. Additionally, it includes utilities for various sorting algorithms, symbolic computations, and JSON data export.

The system is designed with a modular structure, where each module handles a specific mathematical or algorithmic domain. It supports both **numerical computation** (executed locally) and **symbolic computation** (facilitated remotely via the SageMathCell service).

A key feature of the project is the implementation of custom list data structures (via a `BaseList` abstraction), allowing users to observe how sorting algorithms behave with different container types (e.g., dynamic arrays vs. linked lists).

## Features

### 1. Sequences
The `Sequence` class provides comprehensive tools for analyzing mathematical sequences:
* **Parsing:** Stores mathematical expressions.
* **Evaluation:** Numerically evaluates sequence terms using safe evaluation methods.
* **Analysis:** Detects monotonicity (increasing/decreasing) and checks for boundedness.
* **Limits:** Calculates numerical approximations of limits and computes symbolic limits via SageMathCell.
* **Export:** Saves sequence properties to a JSON file.

### 2. Series
The `Series` class focuses on infinite series operations:
* **Term Evaluation:** Calculates the $n$-th term.
* **Convergence:** Tests for convergence using numerical partial sums.
* **Expansions:** Computes Taylor series expansions via SageMathCell.
* **Export:** JSON export functionality.

### 3. Functions
The `Function` class handles operations on mathematical functions:
* **Visualization:** Plots functions using `Matplotlib`.
* **Calculus:** Computes symbolic derivatives, partial derivatives, and indefinite integrals (for single-variable functions).
* **Multivariable:** Calculates gradients for multivariable functions.
* **Limits:** Computes symbolic limits.
* **Export:** Exports function metadata to JSON.

### 4. Sorting Algorithms
The system implements multiple sorting algorithms that operate on objects implementing the custom `BaseList` interface:
* Insertion Sort
* Quick Sort
* Count Sort
* Bubble Sort
* Selection Sort
* Merge Sort

### 5. Custom List Implementations
Users can select the underlying data structure for computations at runtime:
* **ArrayList:** A dynamic array implementation.
* **Other:** Additional types (depending on project configuration).

### 6. SageMathCell Integration
Symbolic mathematical operations are offloaded to the [SageMathCell](https://sagecell.sagemath.org/service) service via the `SageRemote` class. Communication is performed via HTTP POST requests with JSON payloads for:
* Limit computation
* Taylor series
* Derivatives and Integrals

---

## Program Structure

The application utilizes a layered menu system for navigation:

* **Main Menu**
    1.  Sequences
    2.  Series
    3.  Functions
    4.  Exit

* **Sequence Menu:** Term evaluation, Numerical/Symbolic limits, Monotonicity, Boundedness, Sorting scenario, JSON export.
* **Series Menu:** Term evaluation, Convergence check, Taylor series, JSON export.
* **Function Menu:** Plotting, Derivatives, Symbolic limits, Integrals, Gradient, JSON export.

---

## Technical Notes

* **Safety:** All numerical expression evaluations utilize a restricted environment (`safe_globals = {"__builtins__": None, "math": math}`) to prevent the execution of unsafe code.
* **Typing:** The project utilizes Python type hints throughout high-level menus and class methods for code clarity and IDE support.
* **Error Handling:** The application includes safe input parsing, exception handling for mathematical errors, and graceful degradation if SageMathCell is unavailable.

---

## Requirements

* **Python 3.10+**
* `matplotlib`
* `requests`
* Internet access (required for SageMathCell symbolic operations)
* Standard libraries: `json`, `math`

## How to Run

1.  Ensure all requirements are installed.
2.  Execute the main script:
    ```bash
    python main.py
    ```
3.  Follow the on-screen instructions to:
    * Select the List type implementation.
    * Choose the Work mode (Sequences, Series, or Functions).

### JSON Export Locations

By default, the system exports data to the following paths (Windows):

* **Sequences:**
    ```text
    C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\results.json
    ```
* **Series:**
    ```text
    C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\series_results.json
    ```
* **Functions:**
    ```text
    results_function.json (in the working directory)
    ```

*Note: Custom paths may be entered manually during the export process.*