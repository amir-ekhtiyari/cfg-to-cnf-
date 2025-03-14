def large(rules, let, voc):
    new_dict = {k: v[:] for k, v in rules.items()}  # Manual deep copy
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) > 2:
                for j in range(0, len(values[i]) - 2):
                    if j == 0:
                        rules[key][i] = rules[key][i][0] + let[0]
                    else:
                        if new_key not in rules:
                            rules[new_key] = []
                        rules[new_key].append(values[i][j] + let[0])
                    voc.append(let[0])
                    new_key = let[0]
                    let = let[1:]  # Remove the used letter
                if new_key not in rules:
                    rules[new_key] = []
                rules[new_key].append(values[i][-2:])
    return rules, let, voc


def empty(rules, voc):
    e_list = []
    new_dict = {k: v[:] for k, v in rules.items()}  # Manual deep copy
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if values[i] == 'e' and key not in e_list:
                e_list.append(key)
                rules[key].remove(values[i])
        if len(rules[key]) == 0:
            if key in rules:
                voc.remove(key)
            del rules[key]
    new_dict = {k: v[:] for k, v in rules.items()}  # Manual deep copy
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) == 2:
                if values[i][0] in e_list and key != values[i][1]:
                    if key not in rules:
                        rules[key] = []
                    rules[key].append(values[i][1])
                if values[i][1] in e_list and key != values[i][0]:
                    if values[i][0] != values[i][1]:
                        if key not in rules:
                            rules[key] = []
                        rules[key].append(values[i][0])
    return rules, voc


def short(rules, voc):
    # Initialize D with all symbols (terminals and non-terminals)
    D = {key: [key] for key in voc}  # Non-terminals
    for key in rules:
        for production in rules[key]:
            for symbol in production:
                if symbol not in D and symbol != 'e':  # Add terminals
                    D[symbol] = [symbol]

    for letter in voc:
        for key in rules:
            if key in D[letter]:
                values = rules[key]
                for i in range(len(values)):
                    if len(values[i]) == 1 and values[i] not in D[letter]:
                        D[letter].append(values[i])
    rules, D = short1(rules, D)
    return rules, D


def short1(rules, D):
    new_dict = {k: v[:] for k, v in rules.items()}  # Manual deep copy
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            if len(values[i]) == 1:
                rules[key].remove(values[i])
        if len(rules[key]) == 0:
            del rules[key]
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            for j in D[values[i][0]]:
                for k in D[values[i][1]]:
                    if j + k not in values:
                        if key not in rules:
                            rules[key] = []
                        rules[key].append(j + k)
    return rules, D


def final_rules(rules, D, S):
    for let in D[S]:
        if not rules.get(S, []) and not rules.get(let, []):
            for v in rules[let]:
                if v not in rules.get(S, []):
                    if S not in rules:
                        rules[S] = []
                    rules[S].append(v)
    return rules


def print_rules(rules):
    for key in rules:
        values = rules[key]
        for i in range(len(values)):
            print(f"{key} -> {values[i]}")


def generate_strings(grammar, start_symbol, max_length):
    def expand(symbol, current_length):
        if current_length > max_length:
            return []
        if symbol not in grammar:
            return [symbol]

        strings = []
        for production in grammar[symbol]:
            if production == "λ":
                strings.append("")
                continue
            temp = [""]
            for char in production:
                new_temp = []
                for t in temp:
                    for s in expand(char, current_length + 1):
                        new_temp.append(t + s)
                temp = new_temp
            strings.extend(temp)

        return strings

    all_strings = expand(start_symbol, 0)
    valid_strings = [s for s in all_strings if 0 <= len(s) <= max_length]
    return valid_strings


def main():
    myGrammar = {}
    nonTerminal = input('Enter non-terminals (space-separated): ').split()

    for nt in nonTerminal:
        rules = input(f"Enter rules for {nt} (space-separated): ").split()
        myGrammar[nt] = rules

    let = [chr(i) for i in range(65, 91)] + [chr(i) for i in range(97, 123)]  # A-Z, a-z
    let.remove('e')  # Remove 'e' from the pool
    voc = nonTerminal.copy()  # Initialize voc with non-terminals
    S = input("Enter start symbol: ")

    print('\nRules before do sth:')
    print_rules(myGrammar)

    print('\nRules after large rules removal:')
    myGrammar, let, voc = large(myGrammar, let, voc)
    print_rules(myGrammar)

    print('\nRules after deleting lambda productions:')
    myGrammar, voc = empty(myGrammar, voc)
    print_rules(myGrammar)

    print('\nRules after deleting unit productions:')
    myGrammar, D = short(myGrammar, voc)
    print_rules(myGrammar)

    print('\nFinal rules (Chomsky Normal Form):')
    myGrammar = final_rules(myGrammar, D, S)
    print_rules(myGrammar)

    # Now to check whether a string is acceptable
    mystr = input("\nEnter your string to check: ")
    myStrlength = len(mystr)
    allStrings = generate_strings(myGrammar, S, myStrlength)

    if mystr in allStrings:
        print(f'The string "{mystr}" is acceptable.')
    else:
        print(f'The string "{mystr}" is not acceptable.')


if __name__ == '__main__':
    main()