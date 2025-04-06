import sys

# --- ansi color codes ---
VIOLET = "\033[35m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
RESET = "\033[0m"

# --- import parser and MAX_REPEATS ---
try:
    # using the user-specified filename 'RegexParser.py'
    from RegexParser import parse_regex, RegexNode, MAX_REPEATS
except ImportError:
    print(f"{RED}Error: Could not import required components from RegexParser.py.{RESET}")
    print(f"{RED}Please ensure 'RegexParser.py' exists and defines 'parse_regex', 'RegexNode', and 'MAX_REPEATS'.{RESET}")
    sys.exit(1)
except Exception as e:
    print(f"{RED}Error importing from RegexParser.py: {e}{RESET}")
    sys.exit(1)

# --- predefined patterns ---
variant3_patterns = [
    "O(P|Q|R)+2(3|4)",
    "A*B(C|D|E)F(G|H|I)²",
    "J+K(L|M|N)*O?(P|Q)³",
]

# --- processing function ---
def process_pattern(pattern_string):
    """Parses, generates, and prints results for a single regex pattern using ANSI colors."""
    print(VIOLET + "------------------------------------" + RESET)
    print(f"{CYAN}Processing Pattern: {RESET}{pattern_string}")
    print(VIOLET + "------------------------------------" + RESET)
    success = False
    try:
        # 1. parse the regex string into an ast
        print(f"{YELLOW}1. Parsing pattern...{RESET}")
        ast_root = parse_regex(pattern_string)
        print(f"{GREEN}   Parser successful.{RESET}")

        # 2. generate a random string using the ast
        print(f"\n{YELLOW}2. Generating random string...{RESET}")
        generation_log = []
        generated_string = ast_root.generate(log=generation_log)

        # 3. print results
        print(f"\n{YELLOW}3. Results:{RESET}")
        print(f"   Generated String: {GREEN}\"{generated_string}\"{RESET}") # color the generated string

        print(f"\n{YELLOW}4. Generation Process Log (Bonus):{RESET}")
        if generation_log:
            indent = "   "
            current_indent = indent
            for step in generation_log:
                if step.startswith("->"):
                    log_color = CYAN
                elif step.startswith("<-"):
                    log_color = CYAN
                else:
                    log_color = "" # default terminal color

                if step.startswith("<- exiting"):
                    current_indent = current_indent[:-len(indent)] if len(current_indent) > len(indent) else indent
                print(f"{current_indent}{log_color}{step}{RESET}") # apply reset if color used
                if step.startswith("-> entering"):
                    current_indent += indent
        else:
            print(f"{YELLOW}   (Log is empty or logging not implemented correctly in generate methods){RESET}")
        success = True

    except NotImplementedError:
        print(f"\n {RED}*** Error: Parser logic is not fully implemented in RegexParser.py ***{RESET}")
    except ValueError as e:
        # parser exceptions are printed within the parser class now, just note failure here
        print(f"\n {RED}*** Error: Failed to parse or process pattern '{pattern_string}'. See parser error details above. ***{RESET}")
    except Exception as e:
        print(f"\n {RED}*** Unexpected error processing pattern '{pattern_string}': {e} ***{RESET}")
        import traceback
        print(f"{RED}Traceback:")
        traceback.print_exc() # print full traceback for debugging

    print(VIOLET + "------------------------------------" + RESET + "\n")
    return success

# --- menu function ---
def display_menu():
    """Displays the main menu options using ANSI colors."""
    print(VIOLET + "="*40 + RESET)
    print(f"{CYAN}         Regex Generator Menu{RESET}")
    print(VIOLET + "="*40 + RESET)
    print(f"{YELLOW} 1.{RESET} Generate from a specific predefined pattern (Variant 3)")
    print(f"{YELLOW} 2.{RESET} Generate from ALL predefined patterns (Variant 3)")
    print(f"{YELLOW} 3.{RESET} Generate from a CUSTOM regex pattern")
    print(f"{YELLOW} 4.{RESET} Exit")
    print(VIOLET + "="*40 + RESET)

# --- main execution loop ---
if __name__ == "__main__":
    print(VIOLET + "*"*40 + RESET)
    print(f"{CYAN} Welcome to the Dynamic Regex Generator! {RESET}")
    print(VIOLET + "*"*40 + RESET)

    while True:
        display_menu()
        choice = input(f"{CYAN}Enter your choice (1-4): {RESET}").strip()

        if choice == '1':
            print("\nPredefined Patterns (Variant 3):")
            for i, p in enumerate(variant3_patterns):
                print(f"  {YELLOW}{i+1}:{RESET} {p}")
            try:
                pattern_choice = input(f"{CYAN}Select pattern number (1-{len(variant3_patterns)}): {RESET}").strip()
                pattern_index = int(pattern_choice) - 1
                if 0 <= pattern_index < len(variant3_patterns):
                    process_pattern(variant3_patterns[pattern_index])
                else:
                    print(f"{RED}Invalid pattern number.{RESET}")
            except ValueError:
                print(f"{RED}Invalid input. Please enter a number.{RESET}")
            input(f"{YELLOW}Press Enter to return to the menu...{RESET}")

        elif choice == '2':
            print(f"\n{CYAN}Generating from all {len(variant3_patterns)} predefined patterns...{RESET}\n")
            for pattern in variant3_patterns:
                process_pattern(pattern)
            input(f"{YELLOW}Press Enter to return to the menu...{RESET}")

        elif choice == '3':
            # --- Display hints before asking for input ---
            print(f"\n{CYAN}Enter a custom regex pattern using the supported syntax:{RESET}")
            print(VIOLET + "  Syntax Hints:" + RESET)
            print(f"    - {YELLOW}Literals{RESET}: A-Z, 0-9, other non-special chars (e.g., {GREEN}'A'{RESET}, {GREEN}'7'{RESET})")
            print(f"    - {YELLOW}Sequence{RESET}: Place items side-by-side (e.g., {GREEN}'AB3'{RESET})")
            print(f"    - {YELLOW}Grouping{RESET}: Use parentheses {GREEN}'()'{RESET} (e.g., {GREEN}'(AB)'{RESET}, {GREEN}'(A|B)'{RESET})")
            print(f"    - {YELLOW}Choice{RESET}: Use {GREEN}'|'{RESET} inside groups (e.g., {GREEN}'(A|B|C)'{RESET})")
            print(f"    - {YELLOW}Quantifiers{RESET} (apply to preceding item):")
            print(f"        {GREEN}'+'{RESET}: One or more (1 to {MAX_REPEATS})   (e.g., {GREEN}'A+'{RESET}, {GREEN}'(AB)+'{RESET})")
            print(f"        {GREEN}'*'{RESET}: Zero or more (0 to {MAX_REPEATS})  (e.g., {GREEN}'B*'{RESET}, {GREEN}'(C|D)*'{RESET})")
            print(f"        {GREEN}'?'{RESET}: Zero or one         (e.g., {GREEN}'C?'{RESET}, {GREEN}'(EF)?'{RESET})")
            print(f"        {GREEN}'²'{RESET}: Exactly two         (e.g., {GREEN}'D²'{RESET}, {GREEN}'(GH)²'{RESET})")
            print(f"        {GREEN}'³'{RESET}: Exactly three        (e.g., {GREEN}'E³'{RESET}, {GREEN}'(I|J)³'{RESET})")
            print(f"  {CYAN}Example:{RESET} {GREEN}'X(Y|Z)²A+B?'{RESET}")
            print("-" * 20) # separator

            # --- Get custom pattern input ---
            custom_pattern = input(f"{CYAN}Enter your custom regex pattern: {RESET}").strip()

            # --- Process the pattern ---
            if custom_pattern:
                process_pattern(custom_pattern)
            else:
                print(f"{YELLOW}No pattern entered.{RESET}")

            input(f"{YELLOW}Press Enter to return to the menu...{RESET}") # pause before showing menu again

        elif choice == '4':
            print(f"\n{CYAN}Exiting program. Goodbye!{RESET}")
            break # exit the while loop

        else:
            print(f"\n{RED}Invalid choice. Please enter a number between 1 and 4.{RESET}\n")
            input(f"{YELLOW}Press Enter to continue...{RESET}")