# Helper functions to identify terms
def is_variable(expr):
    """By convention, single lowercase letters are variables."""
    return isinstance(expr, str) and len(expr) == 1 and expr.islower()

def is_constant(expr):
    """By convention, capitalized words or numbers are constants."""
    return isinstance(expr, str) and not is_variable(expr)

def occurs_check(var, expr):
    """Checks if variable 'var' occurs anywhere inside compound expression 'expr'."""
    if var == expr:
        return True
    if isinstance(expr, list):
        return any(occurs_check(var, sub_expr) for sub_expr in expr)
    return False

def apply_substitution(sub_pair, expr_list):
    """Applies a substitution pair (term, var) to a list of remaining arguments."""
    term, var = sub_pair
    
    def subst(e):
        if e == var:
            return term
        if isinstance(e, list):
            return [subst(item) for item in e]
        return e

    return [subst(e) for e in expr_list]


def unify(psi1, psi2):
    # Step 1: If psi1 or psi2 is a variable or constant
    if is_variable(psi1) or is_constant(psi1) or is_variable(psi2) or is_constant(psi2):
        # a) If psi1 or psi2 are identical, then return NIL
        if psi1 == psi2:
            return "NIL"
        
        # b) Else if psi1 is a variable
        elif is_variable(psi1):
            # a. then if psi1 occurs in psi2, then return FAILURE
            if occurs_check(psi1, psi2):
                return "FAILURE"
            # b. Else return {(psi2 / psi1)}
            else:
                return [(psi2, psi1)]  # Represented as a list containing a tuple (term, variable)
        
        # c) Else if psi2 is a variable
        elif is_variable(psi2):
            # a. If psi2 occurs in psi1 then return FAILURE
            if occurs_check(psi2, psi1):
                return "FAILURE"
            # b. Else return {(psi1 / psi2)}
            else:
                return [(psi1, psi2)]
        
        # d) Else return FAILURE
        else:
            return "FAILURE"

    # Step 2: If the initial Predicate symbol in psi1 and psi2 are not same, then return FAILURE
    if psi1[0] != psi2[0]:
        return "FAILURE"

    # Step 3: If psi1 and psi2 have a different number of arguments, then return FAILURE
    if len(psi1) != len(psi2):
        return "FAILURE"

    # Step 4: Set Substitution set (SUBST) to NIL
    SUBST = "NIL"

    # Step 5: For i=1 to the number of elements in psi1 (skipping predicate index 0)
    # Note: Elements in list are from index 1 to len(psi1)-1
    args1 = psi1[1:]
    args2 = psi2[1:]
    
    for i in range(len(args1)):
        # a) Call Unify function with the ith element
        S = unify(args1[i], args2[i])
        
        # b) If S = failure then returns Failure
        if S == "FAILURE":
            return "FAILURE"
        
        # c) If S != NIL then do
        if S != "NIL":
            # a. Apply S to the remainder of both L1 and L2
            # (Applies the substitution to all subsequent arguments in the loop)
            for sub_pair in S:
                args1[i+1:] = apply_substitution(sub_pair, args1[i+1:])
                args2[i+1:] = apply_substitution(sub_pair, args2[i+1:])
            
            # b. SUBST = APPEND(S, SUBST)
            if SUBST == "NIL":
                SUBST = S.copy()
            else:
                SUBST = S + SUBST

    # Step 6: Return SUBST
    return SUBST


# --- Execution Tests ---
if __name__ == "__main__":
    # Test case 1: Knows(John, x) and Knows(John, Mary)
    psi1 = ["Knows", "John", "x"]
    psi2 = ["Knows", "John", "Mary"]
    print(f"Unifying {psi1} and {psi2}:")
    print("SUBST:", unify(psi1, psi2))  # Expected: [('Mary', 'x')]
    print("-" * 50)

    # Test case 2: P(x, f(y)) and P(a, f(b))
    psi3 = ["P", "x", ["f", "y"]]
    psi4 = ["P", "a", ["f", "b"]]
    print(f"Unifying {psi3} and {psi4}:")
    print("SUBST:", unify(psi3, psi4))  # Expected: [('b', 'y'), ('a', 'x')]
    print("-" * 50)

    # Test case 3: Occurs check failure -> x and f(x)
    print("Unifying 'x' and ['f', 'x']:")
    print("SUBST:", unify("x", ["f", "x"]))  # Expected: FAILURE
