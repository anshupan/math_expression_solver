import tkinter as tk
from tkinter import messagebox
import ast
import operator
import math
operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.FloorDiv: operator.floordiv
}

functions = {
    "sqrt": math.sqrt,
    "log": math.log,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "abs": abs
}

variables = {}  # Dictionary to store user-defined variables

def evaluate_expression(expression):
    """Safely evaluates a math expression with functions & variables."""
    try:
        tree = ast.parse(expression, mode='eval')
        return evaluate_ast(tree.body)
    except Exception as e:
        return f"Error: {str(e)}"

def evaluate_ast(node):
    """Recursively evaluates AST nodes with function & variable support."""
    if isinstance(node, ast.BinOp) and type(node.op) in operators:
        left = evaluate_ast(node.left)
        right = evaluate_ast(node.right)
        return operators[type(node.op)](left, right)
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        else:
            raise ValueError(f"Unknown variable: {node.id}")
    elif isinstance(node, ast.Call):
        if node.func.id in functions:
            args = [evaluate_ast(arg) for arg in node.args]
            return functions[node.func.id](*args)
        else:
            raise ValueError(f"Unknown function: {node.func.id}")
    elif isinstance(node, ast.Assign):
        var_name = node.targets[0].id
        variables[var_name] = evaluate_ast(node.value)
        return f"Variable {var_name} set to {variables[var_name]}"
    else:
        raise ValueError("Invalid Expression")

def calculate():
    """Handles button click event."""
    expression = entry.get()
    result = evaluate_expression(expression)
    history_listbox.insert(tk.END, f"{expression} = {result}")
    messagebox.showinfo("Result", f"Result: {result}")

# Create GUI window
root = tk.Tk()
root.title("Advanced Math Solver")
root.geometry("400x300")

# Create input field and button
tk.Label(root, text="Enter Expression:").pack(pady=5)
entry = tk.Entry(root, width=40)
entry.pack(pady=5)
tk.Button(root, text="Solve", command=calculate).pack(pady=10)

# History Section
tk.Label(root, text="Calculation History:").pack(pady=5)
history_listbox = tk.Listbox(root, width=50, height=10)
history_listbox.pack(pady=5)

# Run the GUI loop
root.mainloop()
