
import os
from lists import ArrayList, LinkedList, DoublyLinkedList, LibraryList
from sorting_algorithms import *
from Calculus.sequences import Sequence
from Calculus.series import Series
from Calculus.functions import Function
from typing import Iterator, Optional, Dict


CURRENT_LIST_TYPE = ArrayList

def pause() -> None:
    input("\nPress Enter to continue...")

def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def get_user_list_choice() -> None:
    """
    Selects the internal list implementation type at startup.
    Modifies the global variable CURRENT_LIST_TYPE.
    """
    global CURRENT_LIST_TYPE

    print("\n--- SYSTEM CONFIGURATION ---")
    print("Choose the data structure implementation for this session:")
    print("1. ArrayList (Custom array-based implementation)")
    print("2. LibraryList (Python standard list wrapper)")
    print("3. LinkedList (Singly linked list)")
    print("4. DoublyLinkedList (Doubly linked list)")

    choice: str = input("Select option (default is 1): ").strip()

    if choice == '2':
        CURRENT_LIST_TYPE = LibraryList
        print(">> Configuration set: Using LibraryList.")
    elif choice == '3':
        CURRENT_LIST_TYPE = LinkedList
        print(">> Configuration set: Using LinkedList.")
    elif choice == '4':
        CURRENT_LIST_TYPE = DoublyLinkedList
        print(">> Configuration set: Using DoublyLinkedList.")
    else:
        # Default fallback
        CURRENT_LIST_TYPE = ArrayList
        print(">> Configuration set: Using ArrayList.")

    pause()

def save_result_dialog(obj) -> None:
    """
    Universal dialog to ask for filename and save object.
    """
    while True:
        filename: str = input("\nEnter filename to save (without .json): ").strip()

        if not filename:
            print("Filename cannot be empty. Please try again.")
            continue

        # Автоматично додаємо .json, якщо його немає
        if not filename.endswith(".json"):
            full_path: str = f"{filename}.json"
        else:
            full_path:str = filename

        try:
            print(f"Saving to '{full_path}'...")
            # Викликаємо метод експорту об'єкта
            obj.export_to_json(full_path)
            print(f">> Success! Data saved to {full_path}")
            break
        except Exception as e:
            print(f"Error saving file: {e}")
            break

    pause()

def run_sorting_scenario(sequence_obj: Iterator[int]) -> None:
    """
    Logic:
    1. Ask for N (number of elements).
    2. Generate list based on sequence.
    3. Show menu of sorting algorithms.
    4. Run selected sorting.
    """
    print("\n--- GENERATION AND SORTING ---")

    # 1. Ask for N
    try:
        n_input: str = input("Enter the number of elements (N): ")
        n: int = int(n_input)
    except ValueError:
        print("Invalid input. Please enter an integer.")
        return

    # 2. Generate list (using CURRENT_LIST_TYPE)
    target_list: BaseList = CURRENT_LIST_TYPE()

    for _ in range(n):
        try:
            val: int = next(sequence_obj)
            target_list.add(val)
        except StopIteration:
            break

    # 3. Algorithm selection menu
    print("Choose sorting method:")
    print("1. Insertion Sort")
    print("2. Quick Sort")
    print("3. Count Sort")
    print("4. Bubble Sort")
    print("5. Selection Sort")
    print("6. Merge Sort")

    choice: str = input("Your choice: ")

    # 4. Call appropriate sorting class
    sorter: Optional[SortingAlgorithm] = None

    if choice == "1":
        sorter = InsertionSort()
    elif choice == "2":
        sorter = QuickSort()
    elif choice == "3":
        sorter = CountSort()
    elif choice == "4":
        sorter = BubbleSort()
    elif choice == "5":
        sorter = SelectionSort()
    elif choice == "6":
        sorter = MergeSort()

    if sorter:
        print("Running sorting...")
        sorter.sort(target_list)
        print("Sorting finished.")
    else:
        print("Invalid choice.")

def menu_sequences() -> None:
    """
    Complete menu for working with Sequence.
    """
    print("\n--- NEW SEQUENCE ---")
    expression: str = input("Enter the formula (e.g., 1/n, n**2, math.sin(n)): ")
    variable: str = input("Enter the variable name (default 'n'): ")

    if not variable.strip():
        variable = "n"

    # Create Sequence object
    # assuming ArrayList is imported and available as default list_type
    try:
        seq: Sequence = Sequence(expression, variable)
    except Exception as e:
        print(f"Error creating sequence: {e}")
        return

    while True:
        print("\n=== SEQUENCE MENU ===")
        print(f"Current formula: {seq.get_expression()} (var: {seq.get_variable()})")

        print("1. Evaluate at n")
        print("2. Find Limit (Numerical / Approximate)")
        print("3. Find Limit (Symbolic / SageMath)")
        print("4. Check Monotonicity")
        print("5. Find Min/Max (if bounded)")
        print("6. >> GO TO SORTING (Generate & Sort)")
        print("7. Export to JSON")
        print("8. Back to Main Menu")

        choice: str = input("Your choice: ")

        if choice == '1':
            try:
                n_val = int(input("Enter n: "))
                result = seq.evaluate(n_val)
                print(f"Result for n={n_val}: {result}")
            except ValueError:
                print("Please enter a valid integer.")
            except Exception as e:
                print(f"Calculation error: {e}")

        elif choice == '2':
            print("Calculating approximate limit...")
            limit = seq.approximate_limit()
            print(f"Approximate limit: {limit}")

        elif choice == '3':
            print("Connecting to SageMath...")
            try:
                limit = seq.sym_limit()
                print(f"Symbolic limit: {limit}")
            except Exception as e:
                print(f"SageMath error: {e}")

        elif choice == '4':
            is_mono = seq.is_monotonic()
            print(f"Is monotonic: {is_mono}")

            # Additional detail for better UX
            if is_mono:
                if seq.is_monotonic(True):
                    print("(The sequence is increasing)")
                elif seq.is_monotonic(False):
                    print("(The sequence is decreasing)")

        elif choice == '5':
            print("Checking bounds...")
            is_b: bool
            max_v: Optional[float]
            min_v: Optional[float]
            is_b, max_v, min_v = seq.is_bounded()
            if is_b:
                print(f"Sequence is bounded.")
                print(f"Max: {max_v}")
                print(f"Min: {min_v}")
            else:
                print("Sequence is not bounded (or within the checked range).")

        elif choice == '6':
            # Create a generator that yields values from the sequence
            # This bridges the Sequence class with the run_sorting_scenario function
            def seq_generator(s: Sequence) -> Iterator[int]:
                n: int = 1
                while True:
                    yield s.evaluate(n)
                    n += 1

            # Pass the generator to the sorting scenario
            run_sorting_scenario(seq_generator(seq))

        elif choice == '7':
            path: str = input(r"Enter file path (default: C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\results.json): ")
            if not path.strip():
                # Use default path defined in the class method
                try:
                    seq.export_to_json()
                    print("Saved to default path.")
                except Exception as e:
                    print(f"Error saving: {e}")
            else:
                try:
                    seq.export_to_json(path)
                    print(f"Saved to {path}")
                except Exception as e:
                    print(f"Error saving: {e}")

        elif choice == '8':
            break

        else:
            print("Invalid choice. Please try again.")

def menu_series() -> None:
    """
    Complete menu for working with Series.
    """
    print("\n--- NEW SERIES ---")
    expression: str = input("Enter the formula (e.g., 1/n, 1/(n**2), (-1)**n / n): ")
    variable: str = input("Enter the variable name (default 'n'): ")

    if not variable.strip():
        variable = "n"

    # Create Series object
    try:
        # Assuming ArrayList is the default list_type as per imports
        ser: Series = Series(expression, variable)
    except Exception as e:
        print(f"Error creating series: {e}")
        return

    while True:
        print("\n=== SERIES MENU ===")
        print(f"Current formula: {ser.get_expression()}")

        print("1. Evaluate n-th term")
        print("2. Check Convergence (Approximate)")
        print("3. Taylor Series Expansion (SageMath)")
        print("4. Export to JSON")
        print("5. Back to Main Menu")

        choice: str = input("Your choice: ")

        if choice == '1':
            try:
                n_input: str = input("Enter n (integer): ")
                n: int = int(n_input)
                value = ser.term(n)
                print(f"Term at n={n} is: {value}")
            except ValueError:
                print("Please enter a valid integer.")
            except Exception as e:
                print(f"Calculation error: {e}")

        elif choice == '2':
            # is_convergent()
            print("Checking convergence (numerical approximation)...")
            try:
                is_conv: bool = ser.is_convergent()
                if is_conv:
                    print("Result: The series appears to be CONVERGENT (based on partial sums).")
                else:
                    print("Result: The series appears to be DIVERGENT (or convergence is too slow).")
            except Exception as e:
                print(f"Error during check: {e}")

        elif choice == '3':
            # taylor_series()
            print("Connecting to SageMath for Taylor expansion...")
            var_x: str = input("Enter variable for expansion (default 'x'): ")
            if not var_x.strip():
                var_x = 'x'

            order_input: str = input("Enter expansion order (default 5): ")
            try:
                order: int = int(order_input) if order_input.strip() else 5
                result = ser.taylor_series(x=var_x, order=order)
                print(f"\nTaylor Expansion (order {order}):\n{result}")
            except ValueError:
                print("Order must be an integer.")
            except Exception as e:
                print(f"SageMath error: {e}")

        elif choice == '4':
            # export_to_json
            path: str = input(
                r"Enter file path (default: C:\Users\Maria\Documents\GitHub\OOP-lab1\Calculus\series_results.json): ")
            if not path.strip():
                # Use default path defined in the class method
                try:
                    ser.export_to_json()
                    print("Saved to default path.")
                except Exception as e:
                    print(f"Error saving: {e}")
            else:
                try:
                    ser.export_to_json(path=path)
                    print(f"Saved to {path}")
                except Exception as e:
                    print(f"Error saving: {e}")

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please try again.")

def menu_functions() -> None:
    """
    Complete menu for working with Function.
    """
    print("\n--- NEW FUNCTION ---")
    expression: str = input("Enter the function formula (e.g., sin(x), x**2 + y**2): ")

    # Handling variables input
    vars_input: str = input("Enter variables separated by comma (default 'x'): ")
    if not vars_input.strip():
        variables: List[str] = ["x"]
    else:
        variables = [v.strip() for v in vars_input.split(',')]

    # Create Function object
    try:
        func: Function = Function(expression, variables)
    except Exception as e:
        print(f"Error creating function: {e}")
        return

    while True:
        print(f"\n=== FUNCTION MENU ({func.get_expression()}) ===")
        print("1. Plot Graph (Matplotlib)")
        print("2. Find Derivative (Symbolic / Partial)")
        print("3. Find Limit (Symbolic)")
        print("4. Integral (Single variable only)")
        print("5. Gradient (Multi-variable)")
        print("6. Export to JSON")
        print("7. Check Monotonicity")
        print("8. Check Boundedness")
        print("9. Evaluate at Point")
        print("10. Approximate limit.")
        print("11. Back to Main Menu.")

        choice: str = input("Your choice: ")

        if choice == '1':
            # Check if function has more than one variable
            if len(variables) > 1:
                print("Sorry, but we cannot plot graphs for multi-variable functions.")
            else:
                # Single variable plotting logic
                print("--- Plot Settings ---")
                var_to_plot = variables[0]

                try:
                    start_input: str= input("Start range (default 0): ")
                    start: float = float(start_input) if start_input.strip() else 0.0

                    stop_input: str = input("Stop range (default 10): ")
                    stop: float = float(stop_input) if stop_input.strip() else 10.0

                    print(f"Plotting f({var_to_plot})...")
                    # Using the plot method from your Function class
                    func.plot(var=var_to_plot, start=start, stop=stop, title=f"Plot of {expression}")
                except ValueError:
                    print("Invalid range values. Please enter numbers.")
                except Exception as e:
                    print(f"Error plotting: {e}")

        elif choice == '2':
            # Derivative logic
            try:
                if len(variables) == 1:
                    print("Calculating derivative...")
                    res = func.derivative()
                    print(f"Derivative: {res}")
                else:
                    print(f"Multi-variable function detected: {variables}")
                    var: str = input(f"Enter variable for partial derivative: ")
                    res = func.partial_derivative(var)
                    print(f"Partial Derivative (d/d{var}): {res}")
            except Exception as e:
                print(f"Error calculating derivative: {e}")

        elif choice == '3':
            # Symbolic Limit
            try:
                var: str = variables[0]
                if len(variables) > 1:
                    var = input(f"Choose variable for limit ({', '.join(variables)}): ")

                pt_input: str = input("Enter point (number, 'inf' or '-inf'): ")

                if pt_input == 'inf':
                    point = float('inf')
                elif pt_input == '-inf':
                    point = float('-inf')
                else:
                    try:
                        point = float(pt_input)
                    except ValueError:
                        print("Invalid number. Defaulting to infinity.")
                        point = float('inf')

                print("Calculating symbolic limit...")
                res = func.sym_limit(var=var, point=point)
                print(f"Limit: {res}")
            except Exception as e:
                print(f"Error calculating limit: {e}")

        elif choice == '4':
            # Integral
            try:
                if len(variables) > 1:
                    print("Error: Integration is only supported for single-variable functions in this class.")
                else:
                    print("Calculating indefinite integral...")
                    res = func.integral()
                    print(f"Integral: {res}")
            except Exception as e:
                print(f"Error calculating integral: {e}")

        elif choice == '5':
            # Gradient
            try:
                print("Calculating gradient vector...")
                res = func.gradient()
                print(f"Gradient: {res}")
            except Exception as e:
                print(f"Error calculating gradient: {e}")

        elif choice == '6':
            # Export
            path: str = input(r"Enter file path (default: results_function.json): ")
            if not path.strip():
                try:
                    func.export_to_json()
                    print("Saved to default path.")
                except Exception as e:
                    print(f"Error saving: {e}")
            else:
                try:
                    func.export_to_json(path=path)
                    print(f"Saved to {path}")
                except Exception as e:
                    print(f"Error saving: {e}")


        elif choice == '7':

            # Check Monotonicity

            try:

                var_check = variables[0] if len(variables) == 1 else input(
                    f"Choose variable ({', '.join(variables)}): ")

                direction_input = input(
                    "Check increasing (i), decreasing (d), or both (b)? [b]: ").strip().lower() or 'b'

                if direction_input == 'i':

                    direction = True

                elif direction_input == 'd':

                    direction = False

                else:

                    direction = None

                result = func.is_monotonic(var=var_check, is_increasing=direction)

                print(f"Monotonicity check for {var_check}: {result}")

            except Exception as e:

                print(f"Error checking monotonicity: {e}")


        elif choice == '8':

            # Check Boundedness

            try:

                var_check = variables[0] if len(variables) == 1 else input(
                    f"Choose variable ({', '.join(variables)}): ")

                start = float(input("Start of interval [default 0]: ") or 0)

                stop = float(input("End of interval [default 10000]: ") or 10000)

                step = float(input("Step [default 100]: ") or 100)

                bounded, max_val, min_val = func.is_bounded(var=var_check, start=start, stop=stop, step=step)

                print(f"Bounded: {bounded}, Max: {max_val}, Min: {min_val}")

            except Exception as e:

                print(f"Error checking boundedness: {e}")


        elif choice == '9':

            # Evaluate at Point

            try:

                vals: Dict[str, float] = {}

                for v in variables:
                    vals[v] = float(input(f"Enter value for {v}: "))

                result = func.evaluate(**vals)

                print(f"Function value at given point: {result}")

            except Exception as e:

                print(f"Error evaluating function: {e}")


        elif choice == '10':
            try:
                var_check = variables[0] if len(variables) == 1 else input(
                    f"Choose variable ({', '.join(variables)}): ")
                point_input = input("Enter point (number, 'inf', '-inf') [default 'inf']: ").strip() or 'inf'
                if point_input == 'inf':
                    point = float('inf')
                elif point_input == '-inf':
                    point = float('-inf')
                else:
                    point = float(point_input)

                eps = float(input("Enter tolerance eps [default 1e-6]: ") or 1e-6)
                step = float(input("Step size [default 1]: ") or 1)
                n0 = int(input("Starting point n0 [default 1000]: ") or 1000)
                iterate = int(input("Number of iterations [default 1000]: ") or 1000)

                result = func.approximate_limit(var=var_check, point=point, eps=eps, step=step, n0=n0, iterate=iterate)
                print(f"Approximate limit at {point}: {result}")
            except Exception as e:
                print(f"Error computing approximate limit: {e}")

        elif choice == '11':
            break

        else:
            print("Invalid choice. Please try again.")

def main():
    clear_screen()

    # 1. Налаштування типу списку (один раз на старті)
    get_user_list_choice()

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Sequences")
        print("2. Series")
        print("3. Functions")
        print("0. Exit")

        mode: str = input("Select an option: ")

        if mode == '1':
            menu_sequences()
        elif mode == '2':
            menu_series()
        elif mode == '3':
            menu_functions()
        elif mode == '0':
            print("Goodbye.")
            break
        else:
            print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()