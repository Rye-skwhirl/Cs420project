from textx import metamodel_from_file

error404_meta = metamodel_from_file('finalerror404.tx')

error404_model = error404_meta.model_from_file('prog1.error404')
error404_model = error404_meta.model_from_file('prog2.error404')

class InputStatement:
    def __init__(self, source):
        self.source = source

class OutputStatement:
    def __init__(self, value):
        self.value = value

class AssignmentStatement:
    def __init__(self, target, expression):
        self.target = target
        self.expression = expression

class DestroyStatement:
    pass  # No attributes needed for destroy statement

class ShowStatement:
    def __init__(self, message):
        self.message = message

def handle_input(input_statement):
    pass 

def handle_output(output_statement):
    value = output_statement.value.strip('"')
    print(value)

def handle_assignment(assignment_statement):
    pass  

def handle_destroy(destroy_statement):
    print("Program destroyed.")

def handle_show(show_statement):
    message = show_statement.message.strip('"')
    print(message)

for statement in error404_model.statements:
    if isinstance(statement, InputStatement):
        handle_input(statement)
    elif isinstance(statement, OutputStatement):
        handle_output(statement)
    elif isinstance(statement, AssignmentStatement):
        handle_assignment(statement)
    elif isinstance(statement, DestroyStatement):
        handle_destroy(statement)
    elif isinstance(statement, ShowStatement):
        handle_show(statement)

prog1 = """
start program;
in wl a;
in wl b;
set wl result = wl a + wl b;
out "result";
destroy program;
"""

prog2 = """
start program; 
show "Hello World";
destroy program;
"""

print(prog1)
print(prog2)

