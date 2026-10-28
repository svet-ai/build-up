import ast, math, operator as op
OPS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv, ast.Pow: op.pow, ast.Mod: op.mod, ast.USub: op.neg, ast.UAdd: op.pos}
FN = {'sqrt': math.sqrt, 'sin': lambda x: math.sin(math.radians(x)), 'cos': lambda x: math.cos(math.radians(x)),
      'tan': lambda x: math.tan(math.radians(x)), 'ln': math.log, 'log': math.log10}
CONST = {'pi': math.pi, 'e': math.e}

def _ev(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)): return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in OPS:
        a, b = _ev(n.left), _ev(n.right)
        if isinstance(n.op, ast.Pow) and abs(b) > 1000: raise ValueError('pow')
        return OPS[type(n.op)](a, b)
    if isinstance(n, ast.UnaryOp) and type(n.op) in OPS: return OPS[type(n.op)](_ev(n.operand))
    if isinstance(n, ast.Name) and n.id in CONST: return CONST[n.id]
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in FN and len(n.args) == 1: return FN[n.func.id](_ev(n.args[0]))
    raise ValueError('bad expression')

def calc(expr):
    """Safe evaluator (no eval). Returns a string or 'Error'."""
    try:
        v = _ev(ast.parse(expr.replace('^', '**').replace('×', '*').replace('÷', '/'), mode='eval').body)
        return str(int(v)) if float(v).is_integer() and abs(v) < 1e15 else f'{v:.10g}'
    except Exception: return 'Error'
