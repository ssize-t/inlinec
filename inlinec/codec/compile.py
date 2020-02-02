from typing import *
from cffi import FFI
from pycparserext.ext_c_parser import GnuCParser
from pycparser import c_ast
from subprocess import Popen, PIPE


def extract_signature(
    func_name: str, body: str
) -> Optional[Tuple[str, List[Tuple[str, str]]]]:
    signature = None

    class FuncDefVisitor(c_ast.NodeVisitor):
        def visit_FuncDeclExt(self, node):
            nonlocal signature  # bad
            # so much badness below
            def get_typ_str(node):
                if isinstance(node, c_ast.PtrDecl):
                    return f"{' '.join(node.type.type.names)}*"
                else:
                    return " ".join(node.type.names)

            def get_arg_name(node):
                if isinstance(node, c_ast.PtrDecl):
                    return node.type.declname
                else:
                    return node.declname

            if get_arg_name(node.children()[1][1]) == func_name:
                return_typ = get_typ_str(node.children()[1][1])
                params = node.children()[0][1]
                signature = (
                    return_typ,
                    [(get_arg_name(p.type), get_typ_str(p.type)) for p in params]
                    if params
                    else [],
                )

    parser = GnuCParser()
    ast = parser.parse(body)
    v = FuncDefVisitor()
    v.visit(ast)
    # ast.show()

    return signature


def preprocess(src: str) -> str:
    # pcpp does not work correctly with includes, plus it evals #ifs
    # Typedef gcc directives to satisfy pycparser
    # src = '''#define __attribute__(x)
    #         #define __extension__
    #         #define __inline
    #         #define __restrict
    #         #definie __asm__
    # ''' + src
    p = Popen(["gcc", "-E", "-"], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    src = p.communicate(input=src.encode("ascii"))[0].decode()
    # from pcpp import Preprocessor
    # p = Preprocessor()
    # p.add_path('/Library/Developer/CommandLineTools/usr/lib/clang/11.0.0/include')
    # p.parse(src)
    # oh = StringIO()
    # p.write(oh)
    # src = oh.getvalue()
    return src


def compile(
    module_name: str, func_name: str, src: str
) -> Tuple[str, List[Tuple[str, str]]]:
    preprocessed_src = preprocess(src)
    sig = extract_signature(func_name, preprocessed_src)
    if not sig:
        raise Exception("Failed to extract signature for %s", func_name)
    ffibuilder = FFI()
    ffibuilder.dlopen(None)
    ffibuilder.cdef(f"{sig[0]} {func_name}({','.join(v[1] for v in sig[1])});")

    ffibuilder.set_source(module_name, src)
    ffibuilder.compile(verbose=False)

    return sig
