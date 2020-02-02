# Inline C
Effortlessly write inline C functions in Python source code
```python
# coding: inlinec
from inlinec import inlinec

@inlinec
def Q_rsqrt(number):
    float Q_rsqrt( float number )
    {
        long i;
        float x2, y;
        const float threehalfs = 1.5F;

        x2 = number * 0.5F;
        y  = number;
        i  = * ( long * ) &y;                       // evil floating point bit level hacking
        i  = 0x5f3759df - ( i >> 1 );               // what the fuck? 
        y  = * ( float * ) &i;
        y  = y * ( threehalfs - ( x2 * y * y ) );   // 1st iteration

        return y;
    }

print(Q_rsqrt(1.234))
```
Inlinec supports gnu-specific c extensions, so you're likely to have reasonable success #includeing glibc headers.

Inspired by [Pyxl](https://github.com/pyxl4/pyxl4)

# How does this work?
Python has a mechanism for creating custom codecs, which given an input token stream, produce an output token stream. Inlinec consumes the entire token stream, runs a fault-tolerant parser on it ([parso](https://github.com/davidhalter/parso)), finds which function nodes are annotated with an `@inlinec` decorator, creates a `ctypes` wrapper for the content of the function, and replaces the function body with a call to the ctypes wrapper. The import for the wrapper is lifted to the top of the file. Once this transformation has been made, the source code is re-tokenized and the Python interpreter only sees the transformed source.
So a function like this:
```python
@inlinec
def test():
    #include<stdio.h>
    void test() {
        printf("Hello, world");
    }
```
Gets turned into:
```python
from test_8281231239129310 import lib as test_8281231239129310_lib, ffii as test_8281231239129310_ffi

@inlinec
def test():
    return test_8281231239129310_lib.test()
```
In theory, this allows inline c functions to be called with a one-time compilation overhead and the same performance characteristics as ctypes -- the underlying FFI library. 

# Limitations
Note: This is just a proof of concept
    
* Passing pointers to C functions does not currently work (aside from strings)
* Shells out to `gcc -E` to preprocess the source code
* Compilation is not cached and takes a long time every run
* Compilation pollutes the current directory with .so, .o, .c files
* The source file is parsed multiple times unnecessarily
* Many more


# Installation
Inlinec requires a C compiler to be installed on the system (tested with GCC and Clang), as well as the python development libraries to be installed (python3-dev).
To play around with it in a container you can use the provided Dockerfile, just run docker build, exec into a shell in the container, and you have a working installation of inlinec.
```bash
> docker build -t inlinec . && docker run -it inlinec bash
```