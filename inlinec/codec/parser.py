import parso
from parso.python.tree import PythonNode
from typing import *
from tokenize import generate_tokens, TokenInfo, INDENT
from io import StringIO
from uuid import uuid4
from inlinec.codec.compile import compile


def token_at(line_no: int, typ: int, tokens: List[TokenInfo]) -> Optional[TokenInfo]:
    for t in tokens:
        if t.start[0] >= line_no and t.type == typ:
            return t


def ffc(typ: str, node: PythonNode) -> Optional[PythonNode]:
    for x in node.children:
        if x.type == typ:
            return x


def find_decorated_nodes(mod: PythonNode) -> List[PythonNode]:
    decorated = []
    q = [mod]
    while q:
        n = q.pop()
        if not hasattr(n, "children"):
            continue
        decorator_found = False
        for x in n.children:
            if not decorator_found and x.type == "decorator":
                name = ffc("name", x).value
                if name == "inlinec":
                    decorator_found = True
                    continue
            elif decorator_found and x.type == "funcdef":
                decorated.append(x)
            if hasattr(x, "children"):
                q.append(x)

    return decorated


def chain(start_val, *funcs):
    v = start_val
    for f in funcs:
        vp = f(v)
        if not vp:
            return None
        v = vp
    return v


def gen_call(
    qual: str,
    func_name: str,
    params: List[Tuple[str, str]],
    return_typ: str,
    annotated_params: Dict[str, str],
) -> str:
    convert_params = []
    for param, typ in params:
        param = (
            f'{param}.encode("ascii")' if typ == "char*" else
            f'{param}.encode("ascii")' if typ == "char" else
            param
        )
        convert_params.append(param)
    convert_ret = (
        (lambda ret_val: f'{qual}_ffi.string({ret_val}).decode("ascii")')
        if return_typ == "char*"
        else lambda ret_val: ret_val
    )
    return "return " + convert_ret(f'{qual}_lib.{func_name}({",".join([p for p in convert_params if p is not None])})')


def gen_import(qual: str) -> str:
    return f"from {qual} import lib as {qual}_lib, ffi as {qual}_ffi\n"

def gen_qual(alias: str, func_name: str) -> str:
    return f'{alias}__{func_name}'

def transform(lines: List[str]) -> str:
    src = "".join(lines)
    mod = parso.parse(src)
    tokens = list(generate_tokens(StringIO(src).readline))
    cfuncs = find_decorated_nodes(mod)
    aliases = {cf: str(uuid4()).replace('-', '_') for cf in cfuncs}
    imports = ["\n"] + [gen_import(gen_qual(cf.name.value, alias)) for cf, alias in aliases.items()]
    lines = imports + lines[1:]
    offset = len(imports) - 1

    for func in cfuncs:
        name = func.name.value
        alias = aliases[func]
        qual = gen_qual(name, alias)
        startl = func.start_pos[0] + offset
        endl = func.end_pos[0] + offset
        body = "".join(lines[startl:endl])

        sig = compile(qual, func.name.value, body)

        annotated_params = {}
        for p in func.get_params():
            if p.annotation:
                annotated_params[p.name.value] = p.annotation.value

        indent = token_at(startl - offset, INDENT, tokens).string
        lines[startl] = indent + gen_call(
            qual, name, sig[1], sig[0], annotated_params
        )
        for i in range(startl + 1, endl - 1):
            lines[i] = ""

    return "".join(lines)
