# import sys;sys.path.append(r"T:\Code\PyRobot\part3\py_code")
# import importlib;importlib.reload(testa)
import ctypes

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
GetModuleHandleW = kernel32.GetModuleHandleW
GetModuleHandleW.argtypes = (ctypes.c_wchar_p, )
GetModuleHandleW.restype = ctypes.c_int

base = GetModuleHandleW("CtypesTest.exe")

# 调用cdecl_add
cdecl_add_pfunc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
cdecl_add_offset = 0x00AF4190 - 0x00AE0000
cdecl_add = cdecl_add_pfunc(base + cdecl_add_offset)
print("cdecl_add: ", cdecl_add(111, 222))

# 调用stdcall_add
stdcall_add_pfunc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
stdcall_add_offset = 0x00AF43B0 - 0x00AE0000
stdcall_add = stdcall_add_pfunc(base + stdcall_add_offset)
print("stdcall_add: ", stdcall_add(333, 444))

# 调用console_print
class CString(ctypes.Structure):
    _fields_ = [
        ('s', ctypes.c_wchar_p),
        ('len', ctypes.c_uint)
    ]
console_print_pfunc = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(CString))
console_print_offset = 0x00AF2F10 - 0x00AE0000
console_print = console_print_pfunc(base + console_print_offset)

cs = CString()
s = "Python结构体字符串"
cs.s = ctypes.c_wchar_p(s)
cs.len = len(s)
# 获取该结构体的内存指针地址的三种方式
print("ctypes.byref: ", ctypes.byref(cs))
print("ctypes.addressof: ", hex(ctypes.addressof(cs)))
print("ctypes.cast: ", hex(ctypes.cast(ctypes.pointer(cs), ctypes.c_void_p).value))

# 调用该函数
result = console_print(ctypes.byref(cs))
print("console_print result: ", result)

# 全局结构体一般偏移是固定的
ccs_offset = 0x00AFE2D0 - 0x00AE0000 
css_addr = base + ccs_offset

# 读取内存中的字符串和int
s = ctypes.c_wchar_p.from_address(css_addr)
l = ctypes.c_uint.from_address(css_addr + 0x4)
print("单独读取内存结构体: ", s.value, l)

# 读取全局结构体数据
css = CString.from_address(css_addr)
print("读取整个结构体: ", css.s, css.len)


# 调用回调函数
def python_stdcall_add(a:int, b:int):
    print("python_stdcall_add: ", a, b)
    return a-b

add_callback_pfunc = ctypes.CFUNCTYPE(ctypes.c_int, stdcall_add_pfunc, ctypes.c_int, ctypes.c_int) 
add_callback_offset = 0x00AF40D0 - 0x00AE0000
add_callback = add_callback_pfunc(base + add_callback_offset)
result = add_callback(stdcall_add_pfunc(python_stdcall_add), 5, 2)
print("add_callback: ", result)