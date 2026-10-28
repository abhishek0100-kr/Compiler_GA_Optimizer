"""Reference interpreter for straight-line 3AC; supports INPUT for semantic checks."""
def execute_ir(ir, inputs=()):
    values, outputs, it = {}, [], iter(inputs)
    for inst in ir:
        op=inst[0]
        if op == 'INPUT':
            try: values[inst[1]]=next(it)
            except StopIteration as exc: raise ValueError(f'Missing input value for {inst[1]}') from exc
        elif op == 'CONST': values[inst[1]]=inst[2]
        elif op == 'COPY': values[inst[1]]=_value(inst[2],values)
        elif op == 'BINOP':
            operator,dest,a,b=inst[1:]; av,bv=_value(a,values),_value(b,values)
            if operator=='+': result=av+bv
            elif operator=='-': result=av-bv
            elif operator=='*': result=av*bv
            elif operator=='/':
                if bv==0: raise ZeroDivisionError('division by zero')
                result=av/bv
            else: raise ValueError(f'Unsupported operator {operator}')
            values[dest]=result
        elif op == 'PRINT': outputs.append(_value(inst[1],values))
        else: raise ValueError(f'Unsupported opcode: {op}')
    return outputs

def _value(x,values):
    if isinstance(x,(int,float)): return x
    if x not in values: raise ValueError(f'Read of undefined variable {x!r}')
    return values[x]

def preserves_outputs(original,candidate,input_cases=((),)):
    for case in input_cases:
        try: expected=execute_ir(original,case); actual=execute_ir(candidate,case)
        except Exception as exc: return False,f'execution error for inputs {case}: {exc}'
        if len(expected)!=len(actual) or any(not _equiv(a,b) for a,b in zip(expected,actual)):
            return False,f'output mismatch for inputs {case}: expected {expected}, got {actual}'
    return True,'outputs preserved on all supplied test cases'
def _equiv(a,b):
    if isinstance(a,(int,float)) and isinstance(b,(int,float)): return abs(a-b)<=1e-9*max(1.0,abs(a),abs(b))
    return a==b
