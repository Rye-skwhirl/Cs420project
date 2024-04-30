from textx import metamodel_from_file

error_meta = metamodel_from_file('finalerror404.tx')

error_model1 = error_meta.model_from_file('prog1.error404')
error_model2 = error_meta.model_from_file('prog2.error404')

def varmap(targetVar, state):
    if targetVar in state:
        return state[targetVar]
    else:
        raise ValueError("Error: Var not found in varmap")
    
def evalExpressions(expr, state):
# checks the expr string if it is a digit or not, if it is a digit it returns the value
    if expr.isdigit():
        return int(expr)
# this elif checks if expr is a key in the dictionary 's' and if it is, it returns the value    
    elif expr in state:
        return state[expr]
    
    if expr.lower() == "true":
        return True
    elif expr.lower() == "false":
        return False
    
    

# this while piece iterates as long as the program sees a opening parenthesis, it is used to calculate the inner value inside
    while '(' in expr:

# this start piece is used to find the last opening parenthesis aiming to calculate the deepest nested loop
        start = expr.rfind('(')
# this end is used to find the last parenthesis in the expression 
        end = expr.find(')', start)
        if end == -1:
            raise ValueError("Error: Mismatch parentheses")
        iresult = evalExpressions(expr[start + 1:end], state)
        expr = expr[:start] + str(iresult) + expr[end + 1:]

# This operator creates a list of which symbols are used to describe operators and their functions
    operators = ['+', '-', '*', '/', '%', '>=', '<=', '<', '>', '^', '==', '!=']
    for operator in operators:
        if operator in expr:
            lhand, rhand = expr.rsplit(operator, 1)
            lresult = evalExpressions(lhand, state)
            rresult= evalExpressions(rhand, state)

            # debugging print
            #print(f"Evaluated Left: {lresult}, Evaluated Right: {rresult}")
            #print(f"Left: {lhand}, Operator: {operator}, Right: {rhand}")
        

            if lresult is None or rresult is None:
             raise ValueError(f"Error evaluating expressions :'{lhand}' or '{rhand}' returned None")

            if operator == '+':
                return lresult + rresult
            elif operator == '-':
                return lresult - rresult
            elif operator == '*':
                return lresult * rresult
            elif operator == '/':
                if rresult == 0:
                    raise ValueError("Error: Division by zero")
                return lresult / rresult
            elif operator == '%':
                if rresult == 0:
                    raise ValueError("Error: Modulo by zero")
                return lresult % rresult
            elif operator == '^':
                return lresult ** rresult
            # comparison operators
            elif operator == '>=':
                return lresult >= rresult
            elif operator == '<=':
                return lresult <= rresult
    raise ValueError(f"Error: Variable or syntax are invalid '{expr}'")

def parserForCondition(condition):
    operators = ['>=', '<=', '==', '!=', '>', '<']
    for op in operators:
        if op in condition:
            lhand, rhand = condition.split(op)
            return lhand.strip(), op, rhand.strip()
    raise ValueError("Invalid condition format")

def evalCondition(condition, state):
    lhand, operator, rhand = parserForCondition(condition)
    lhandValue = evalExpressions(lhand, state)
    rhandValue = evalExpressions(rhand, state)
    
    if operator == '>=':
        return lhandValue >= rhandValue
    elif operator == '<=':
        return lhandValue <= rhandValue
    elif operator == '==':
        return lhandValue == rhandValue
    elif operator == '!=':
        return lhandValue != rhandValue
    elif operator == '>':
        return lhandValue > rhandValue
    elif operator == '<':
        return lhandValue < rhandValue
    else:
        raise ValueError("Unsupported operator")
    
def blockParser(lines):
    blocks = []
    currentBlock = []
    openBlock = False
    
    for line in lines:
        line = line.strip()
        if line == "start":
            openBlock = True
            currentBlock = []
        elif line == "destroy":
            openBlock = False
            blocks.appen(currentBlock)
            currentBlock = []
        elif openBlock:
            currentBlock.append(line)
        else:
            blocks.appen([line])
            
    return blocks

def blockLine(line, state):
    parts = line.split(' ', 1)
    instruction = parts[0]

    if instruction == "set":
        _, expr = line.split(" ", 1)
        var, val = expr.split('=', 1)
        state[var.strip()] = evalExpressions(val.strip(), state)
    elif instruction == "show":
        # Check if the argument is a string literal or an expression
        if len(parts) > 1:
            argument = parts[1].strip()
            if argument.startswith('"') and argument.endswith('"'):
                # It's a string literal, so print without the quotes
                print(argument[1:-1])
            else:
                # It's not a string literal, so evaluate as an expression
                try:
                    result = varmap(argument, state)
                    print(result)
                except ValueError as error:
                    print(error)

def blocksExecute(blocks, state):
    executeBlock = False
    for block in blocks:
        firstLine = block[0]
        if firstLine.startswith("IF"):
            _, condition = firstLine.split(" ", 1)
            executeBlock = evalCondition(condition, state)
        elif firstLine == "ELSE":
            executeBlock = not executeBlock
        else:
            executeBlock = True
        
        if executeBlock:
            for line in block[1:]:
                blockLine(line.strip(), state)
                
def whatif(condition, state):
    try:    
        parts = condition.split(' ', 2)
        if len(parts) != 3:
            raise ValueError("Condition format is incorrect'")
        
        var, operator, value = parts
        if var not in state:
            raise ValueError(f"Variable '{var}' not found.")

        lhandval = state[var]
        rhandval = int(value) if value.isdigit() else state.get(value, value)
        
        newExpr = f"{lhandval} {operator} '{rhandval}'" if isinstance(rhandval, str) else f"{lhandval} {operator} {rhandval}"
        result = evalComparisonExpr(newExpr, state)
        
        if result:
            print(f"{condition} is True.")
        if condition == "J == 66":
            print("Execute order 66")
        else:
            print(f"{condition} is False.")
    except ValueError as error:
        print(error)

def executeProgram(program):
# s = dict{} is used to initialize an empty dictionary named s, it is used to hold variables and their values    
    state = {}
    

# This takes multiple strings for the program and splits them up into single lines    
    for line in program.splitlines():

# This is used to remove whitespace or spaces
        if not line.strip():
            continue
       
        instruction, expression = line.split(maxsplit=1)
        
        if instruction == "set":
            var, expr = expression.split('=', 1)
            try:
                state[var.strip()] = evalExpressions(expr.strip(), state)
            except ValueError as error:
                print(error)
                
        elif instruction == "show":
            try:
                value = varmap(expression.strip(), state)
                print(f"{var} = {value}")
            except ValueError as error:
                print(error)
                
        elif instruction == "sentence":
        # Check if the line contains a quoted text
            if '"' in line:
                text = line.split('"')[1]  # Extract the text between quotes
                print(text)
            else:
                print("Error: No text found in print_sentence instruction")
        
        elif instruction == "out":
            try:
                value = varmap(expression.strip(), state)
                print(f"{var} = {value}")
            except ValueError as error:
                print(error)
        
    
prog1 = """
start program
set a = 3
set b = 6
set result = a+b
out result
destroy program
"""

prog2 = """
start program
sentence "Hello World"
destroy program
"""

prog3 = """
start program
set a = 10
set b = 20
if a < b 
out b
destroy program
"""

executeProgram(prog1)
executeProgram(prog2)
executeProgram(prog3)