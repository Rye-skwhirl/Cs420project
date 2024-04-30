from textx import metamodel_from_file

error_meta = metamodel_from_file('finalerror404.tx')

error_model1 = error_meta.model_from_file('prog1.error404')
error_model2 = error_meta.model_from_file('prog2.error404')

prog1 = """
start program
show "Hello World"
destroy program
"""

prog2 = """
start program
set a = 3
set b = 6
set result = a + b
out "result"
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


print(prog1)
print(prog2)
print(prog3)