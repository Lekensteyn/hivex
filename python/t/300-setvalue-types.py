# Test various possible types for assignment to setvalue
# Copyright (C) 2014 Peter Wu <peter@lekensteyn.nl>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import hivex
import os
from sys import getrefcount

srcdir = "."
if "srcdir" in os.environ and os.environ["srcdir"]:
    srcdir = os.environ["srcdir"]

h = hivex.Hivex ("%s/../images/minimal" % srcdir,
                 write = True)

REG_SZ = 1
REG_BINARY = 3
REG_DWORD = 4
REG_DWORD_BIG_ENDIAN = 5
REG_QWORD = 11

def set_value (key="test key", t=REG_BINARY, value=b'Val'):
    global h
    h.node_set_value (h.root (), {
        "key": key,
        "t": t,
        "value": value
    })

def test_pass (t, value, exp_bytes):
    global h
    key = "test_key"
    set_value (key, t, value)
    val = h.node_get_value (h.root (), key)
    ret_type, ret_value = h.value_value (val)
    assert t == ret_type, \
        "expected type {0}, got {1}".format(t, ret_type)
    assert exp_bytes == ret_value, \
        "expected value {0}, got {1}".format(exp_bytes, ret_value)

def test_exception (exception_type, **kwargs):
    try:
        set_value (**kwargs)
        raise AssertionError("expected {0}".format(exception_type))
    except exception_type:
        pass

# Good weather tests
test_pass (REG_BINARY,          b"\x01\x02",        b"\x01\x02")
test_pass (REG_SZ,              u"Val",             b"\x56\x61\x6c")
test_pass (REG_DWORD,           0xabcdef,           b'\xef\xcd\xab\x00')
test_pass (REG_DWORD_BIG_ENDIAN, 0xabcdef,          b'\x00\xab\xcd\xef')
test_pass (REG_QWORD,           0x0123456789abcdef,
        b'\xef\xcd\xab\x89\x67\x45\x23\x01')

# *WORDs must still accept bytes (the length is not checked)
test_pass (REG_DWORD,           b'\xaa\xbb\xcc',    b'\xaa\xbb\xcc')

# Bad weather tests
test_exception (TypeError, key = 1)
test_exception (TypeError, t = "meh")
test_exception (TypeError, t = REG_SZ, value = 1)
test_exception (TypeError, t = REG_DWORD, value = None)
