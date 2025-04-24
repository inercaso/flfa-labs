from Grammar import Grammar
from UnitTest import TestGrammar
import unittest
import os

# ansi color codes
VIOLET = "\033[35m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_main_menu():
    # show main menu options with colors
    print(VIOLET + "="*40 + RESET)
    print(f"{CYAN}         Chomsky Normal Form Converter{RESET}")
    print(VIOLET + "="*40 + RESET)
    print(f"{YELLOW} 1.{RESET} Predefined Grammar (Variant)")
    print(f"{YELLOW} 2.{RESET} Run Unit Tests")
    print(f"{YELLOW} 3.{RESET} Custom Grammar")
    print(f"{YELLOW} 4.{RESET} Exit")
    print(VIOLET + "="*40 + RESET)

def display_grammar_menu():
    # show grammar transformation options
    print(VIOLET + "="*40 + RESET)
    print(f"{CYAN}         Transformation Steps{RESET}")
    print(VIOLET + "="*40 + RESET)
    print(f"{YELLOW} 1.{RESET} Eliminate Epsilon Productions")
    print(f"{YELLOW} 2.{RESET} Eliminate Unit Productions")
    print(f"{YELLOW} 3.{RESET} Eliminate Inaccessible Symbols")
    print(f"{YELLOW} 4.{RESET} Eliminate Unproductive Symbols")
    print(f"{YELLOW} 5.{RESET} Transform to Chomsky Normal Form")
    print(f"{YELLOW} 6.{RESET} Run All Transformations")
    print(f"{YELLOW} 0.{RESET} Return to Main Menu")
    print(VIOLET + "="*40 + RESET)

def run_unit_tests():
    # run unit tests and show results
    clear_screen()
    print(VIOLET + "="*40 + RESET)
    print(f"{CYAN}         Running Unit Tests{RESET}")
    print(VIOLET + "="*40 + RESET)
    
    # run tests
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGrammar)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # show test summary
    print("\n" + VIOLET + "="*40 + RESET)
    print(f"{CYAN}Test Summary:{RESET}")
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(VIOLET + "="*40 + RESET)
    
    input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")

def input_custom_grammar():
    clear_screen()
    print(VIOLET + "="*40 + RESET)
    print(f"{CYAN}         Input Custom Grammar{RESET}")
    print(VIOLET + "="*40 + RESET)
    
    # get non-terminals
    print(f"{YELLOW}Enter non-terminals (uppercase letters, separated by spaces):{RESET}")
    V_N = input(f"{CYAN}Non-terminals: {RESET}").strip().split()
    
    # get terminals
    print(f"\n{YELLOW}Enter terminals (lowercase letters, separated by spaces):{RESET}")
    V_T = input(f"{CYAN}Terminals: {RESET}").strip().split()
    
    # get productions
    P = {}
    print(f"\n{YELLOW}Enter productions in format: NonTerminal -> Production1 | Production2 | ...{RESET}")
    print(f"{YELLOW}Enter 'done' when finished{RESET}\n")
    
    while True:
        production = input(f"{CYAN}Enter production (or 'done' to finish): {RESET}")
        if production.lower() == 'done':
            break
        
        try:
            left, right = production.split('->')
            left = left.strip()
            if left not in V_N:
                print(f"{RED}Error: {left} is not a valid non-terminal{RESET}")
                continue
            
            productions = [p.strip() for p in right.split('|')]
            P[left] = productions
            
        except ValueError:
            print(f"{RED}Invalid format. Please use: NonTerminal -> Production1 | Production2 | ...{RESET}")
            continue
    
    # create grammar and set rules
    grammar = Grammar()
    if grammar.set_custom_grammar(P, V_N, V_T):
        print(f"\n{CYAN}Grammar successfully loaded!{RESET}")
        print(f"{YELLOW}Non-terminals: {', '.join(V_N)}{RESET}")
        print(f"{YELLOW}Terminals: {', '.join(V_T)}{RESET}")
        print(f"{YELLOW}Productions:{RESET}")
        for key, value in P.items():
            print(f"{key} -> {' | '.join(value)}")
        
        input(f"\n{YELLOW}Press Enter to proceed with transformations...{RESET}")
        
        # run all transformations
        clear_screen()
        print(VIOLET + "="*40 + RESET)
        print(f"{CYAN}         Running All Transformations{RESET}")
        print(VIOLET + "="*40 + RESET)
        grammar.ReturnProductions()
        
        input(f"\n{YELLOW}Press Enter to return to main menu...{RESET}")
        return grammar
    else:
        print(f"{RED}Invalid grammar. Please check your input.{RESET}")
        input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        return None

def process_grammar(grammar):
    # handle grammar transformations based on user choice
    while True:
        display_grammar_menu()
        choice = input(f"{CYAN}Enter your choice (0-6): {RESET}")
        
        if choice == '0':
            break
        elif choice == '1':
            clear_screen()
            print(f"{CYAN}Eliminating Epsilon Productions:{RESET}")
            grammar.elim_epsilon()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == '2':
            clear_screen()
            print(f"{CYAN}Eliminating Unit Productions:{RESET}")
            grammar.elim_unit_prod()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == '3':
            clear_screen()
            print(f"{CYAN}Eliminating Inaccessible Symbols:{RESET}")
            grammar.elim_inaccesible_symb()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == '4':
            clear_screen()
            print(f"{CYAN}Eliminating Unproductive Symbols:{RESET}")
            grammar.elin_unnprod_symb()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == '5':
            clear_screen()
            print(f"{CYAN}Transforming to Chomsky Normal Form:{RESET}")
            grammar.transf_to_cnf()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        elif choice == '6':
            clear_screen()
            print(f"{CYAN}Running All Transformations:{RESET}")
            grammar.ReturnProductions()
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")
        else:
            print(f"{RED}Invalid choice. Please try again.{RESET}")
            input(f"\n{YELLOW}Press Enter to continue...{RESET}")

def main():
    print(VIOLET + "*"*40 + RESET)
    print(f"{CYAN} Welcome to the Chomsky Normal Form Converter! {RESET}")
    print(VIOLET + "*"*40 + RESET)
    
    while True:
        display_main_menu()
        choice = input(f"{CYAN}Enter your choice (1-4): {RESET}").strip()
        
        if choice == '1':
            grammar = Grammar()  # use predefined grammar
            process_grammar(grammar)
        elif choice == '2':
            run_unit_tests()
        elif choice == '3':
            grammar = input_custom_grammar()
            if grammar:  # only process if grammar was loaded
                process_grammar(grammar)
        elif choice == '4':
            print(f"\n{CYAN}Exiting program. Goodbye!{RESET}")
            break
        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 4.{RESET}\n")
            input(f"{YELLOW}Press Enter to continue...{RESET}")

if __name__ == "__main__":
    main() 