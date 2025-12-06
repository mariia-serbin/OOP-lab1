"""!
@file work_with_sage.py
@brief Remote SageMath execution module.
@details Provides the SageRemote class for sending code to a remote SageMathCell server
         and retrieving results. Handles HTTP requests, JSON responses, timeouts, and errors.
@author
Maria Serbin
@date
06.12.2025
"""

import json
import requests

class SageRemote:

    """!
    @brief Remote execution wrapper for SageMathCell.
    @details This class provides an interface for sending Python/Sage code to the
             online SageMathCell server and retrieving the execution output.

             It uses HTTP POST requests to submit code and returns the received
             response as plain text. This makes it useful for performing symbolic
             calculations, algebraic manipulations, numerical evaluations, and
             other SageMath-supported computations without installing Sage locally.
    """
    def __init__(self, url: str ="https://sagecell.mathcell.org/service", timeout: int = 20):
        self.url: str = url
        self.timeout: int = timeout

    def run_code(self, code: str):

        """!
        @brief Executes Sage/Python code on the remote SageMathCell server.
        @param code A string of Sage or Python code to execute.
        @return Standard output returned by the server as a stripped string.
                Returns an empty string if output is missing.

        @details The method sends a POST request with JSON payload:
                 - `code`: the source code to run

                 If an error occurs (network issue, server failure, invalid response),
                 the method prints an error message and returns `None`.

        @par Example:
        @code
        sage = SageRemote()
        result = sage.run_code("factor(1001)")
        print(result)
        # Output: (7) * (11) * (13)
        @endcode
        """
        payload = {"code": code}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("stdout", "").strip()
        except Exception as e:
            print("Error executing code on SageMathCell:", e)
            return None
