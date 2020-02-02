# coding: inlinec
from inlinec import inlinec
from pytest import raises

def test_char_arg():
    @inlinec
    def test_char_arg(a):
        _Bool test_char_arg(char a) {
            return a == 'a';
        }
    
    assert test_char_arg('a')

def test_int_arg():
    @inlinec
    def test_int_arg(a):
        _Bool test_int_arg(int a) {
            return a == 1;
        }

    assert test_int_arg(1)

def test_bool_arg():
    @inlinec
    def test_bool_arg(t):
        _Bool test_bool_arg(_Bool t) {
            return t == 1;
        }
    
    assert test_bool_arg(True)
    assert not test_bool_arg(False)

def test_wchar_t_arg():
    @inlinec
    def test_wchar_t_arg(t):
        #include<wchar.h>
        _Bool test_wchar_t_arg(wchar_t t) {
            return t == L'\x57';
        }
    
    assert test_wchar_t_arg('W')

def test_uchar_arg():
    @inlinec
    def test_byte_arg(b):
        _Bool test_byte_arg(unsigned char b) {
            return b == 0;
        }

    assert test_byte_arg(0)

def test_short_arg():
    @inlinec
    def test_short_arg(c):
        _Bool test_short_arg(short c) {
            return c == 32767;
        }
    
    assert test_short_arg(32767)

    with raises(OverflowError):
        test_short_arg(99999)

    with raises(OverflowError):
        test_short_arg(-99999)

def test_ushort_arg():
    @inlinec
    def test_ushort_arg(c):
        _Bool test_ushort_arg(unsigned short c) {
            return c == 32767;
        }
    
    assert test_ushort_arg(32767)

    with raises(OverflowError):
        assert test_ushort_arg(-32767)

def test_int_arg():
    @inlinec
    def test_int_arg(i):
        _Bool test_int_arg(int i) {
            return i == 123456;
        }

    assert test_int_arg(123456)

def test_uint_arg():
    @inlinec
    def test_uint_arg(i):
        _Bool test_uint_arg(unsigned int i) {
            return i == 123456;
        }
    
    test_uint_arg(123456)
    
    with raises(OverflowError):
        test_uint_arg(-123456)

def test_long_arg():
    @inlinec
    def test_long_arg(i):
        _Bool test_long_arg(long i) {
            return i == 2147483647;
        }
    
    test_long_arg(2147483647)

def test_ulong_arg():
    @inlinec
    def test_ulong_arg(i):
        _Bool test_ulong_arg(unsigned long i) {
            return i == 4294967295;
        }
    
    test_ulong_arg(4294967295);

    with raises(OverflowError):
        test_ulong_arg(-1)

def test_long_long_arg():
    @inlinec
    def test_long_long_arg(i):
        _Bool test_long_long_arg(long long i) {
            return i == 9223372036854775806;
        }

    test_long_long_arg(9223372036854775806)

def test_ulong_long_arg():
    @inlinec
    def test_ulong_long_arg(i):
        _Bool test_ulong_long_arg(unsigned long long i) {
            return i == 18446744073709551613UL;
        }

    test_ulong_long_arg(18446744073709551613)

    with raises(OverflowError):
        test_ulong_long_arg(-1)

def test_size_t_arg():
    @inlinec
    def test_size_t_arg(i):
        typedef long unsigned int size_t;
        _Bool test_size_t_arg(size_t i) {
            return i == 9223372036854775806;
        }
    
    test_size_t_arg(9223372036854775806)

    with raises(OverflowError):
        test_size_t_arg(-1)

def test_ssize_t_arg():
    @inlinec
    def test_ssize_t_arg(i):
        # include<sys/types.h>
        _Bool test_ssize_t_arg(ssize_t i) {
            return i == -1;
        }
    
    test_ssize_t_arg(-1)

def test_float_arg():
    @inlinec
    def test_float_arg(f):
        _Bool test_float_arg(float f) {
            return f == 340282346638528859811704183484516925440.0000000000000000;
        }
    
    test_float_arg(340282346638528859811704183484516925440.0000000000000000)

def test_double_arg():
    @inlinec
    def test_double_arg(d):
        _Bool test_double_arg(double d) {
            return d == 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000000000000;
        }
    
    test_double_arg(179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000000000000)

def test_long_double_arg():
    @inlinec
    def test_long_double_arg(ld):
        _Bool test_long_double_arg(long double ld) {
            return ld == 179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000000000000;
        }
    
    test_long_double_arg(179769313486231570814527423731704356798070567525844996598917476803157260780028538760589558632766878171540458953514382464234321326889464182768467546703537516986049910576551282076245490090389328944075868508455133942304583236903222948165808559332123348274797826204144723168738177180919299881250404026184124858368.000000000000000)

def test_c_char_p_arg():
    @inlinec
    def test_c_char_p_arg(s):
        #include<string.h>
        _Bool test_c_char_p_arg(char *s) {
            return strcmp(s, "Hello, world!");
        }
    
    test_c_char_p_arg("Hello, world!")

def test_wchar_p_arg():
    @inlinec
    def test_wchar_p_arg(t):
        #include<wchar.h>
        _Bool test_wchar_p_arg(wchar_t *t) {
            return wcscmp(t, L"Helloo");
        }
    
    assert test_wchar_p_arg('Hello')
