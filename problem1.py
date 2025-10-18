import sys

def solve():
    """
    Solves a single test case for the "Warm Up" problem.
    """
    try:
        N_str = sys.stdin.readline()
        if not N_str: return -1, None
        N = int(N_str)
        A = list(map(int, sys.stdin.readline().split()))
        B = list(map(int, sys.stdin.readline().split()))
    except (IOError, ValueError):
        return -1, None

    # Data structures for O(N) processing. Using 1-based indexing for temperatures and dishes.
    sinks_by_target = [[] for _ in range(N + 1)]
    initial_temps_present = [False] * (N + 1)
    
    # Feasibility Check 1: A[i] <= B[i] for all i.
    # Also, populate sinks and record initial temperatures present.
    for i in range(N):
        if A[i] > B[i]:
            return -1, None
        
        initial_temps_present[A[i]] = True
        
        if A[i] < B[i]:
            # Dish indices are 1-based in the problem statement.
            sinks_by_target[B[i]].append(i + 1)

    # Feasibility Check 2: A source must exist for each required target temperature.
    for t in range(1, N + 1):
        if sinks_by_target[t] and not initial_temps_present[t]:
            return -1, None

    # If feasible, generate the sequence of operations.
    operations = []
    
    # Group dishes by their initial temperature to serve as heaters.
    heaters_by_temp = [[] for _ in range(N + 1)]
    for i in range(N):
        heaters_by_temp[A[i]].append(i + 1)
        
    # Process temperatures in increasing order.
    for t in range(1, N + 1):
        sinks_to_heat = sinks_by_target[t]
        
        if sinks_to_heat:
            # Feasibility checks guarantee a heater exists at temperature t.
            master_heater = heaters_by_temp[t][0]
            
            for sink_dish in sinks_to_heat:
                # The operation is specified as (hotter_dish, colder_dish).
                operations.append((master_heater, sink_dish))
            
            # After being heated, these sinks are now also at temperature t.
            heaters_by_temp[t].extend(sinks_to_heat)

    return len(operations), operations

def main():
    """
    Main function to read input and handle multiple test cases.
    """
    try:
        num_test_cases_str = sys.stdin.readline()
        if not num_test_cases_str: return
        num_test_cases = int(num_test_cases_str)
        for i in range(1, num_test_cases + 1):
            k, ops = solve()
            if k == -1:
                print(f"Case #{i}: -1")
            else:
                print(f"Case #{i}: {k}")
                if ops:
                    for op in ops:
                        print(f"{op[0]} {op[1]}")
    except (IOError, ValueError):
        return

if __name__ == "__main__":
    main()


    # to run the code use this command : Get-Content input.txt | python problem1.py