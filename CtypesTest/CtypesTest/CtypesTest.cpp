#include <iostream>
#include <Windows.h>
#include <io.h>
#include <fcntl.h>


typedef int(*cdecl_add_pointer)(int, int);
typedef int(__stdcall *stdcall_add_pointer)(int, int);
typedef int(*cdecl_string_pointer)(const char*, const wchar_t*);

struct CString
{
	wchar_t* s = nullptr;
	size_t len = 0;
	CString(wchar_t* ss) {
		s = ss;
		len = wcslen(ss);
	}
};

CString ccs((wchar_t*)L"aaaaaa这是个全局变量结构体");


int cdecl_add(int a, int b) {
	std::wcout << L"cdecl调用约定\n";
	return a + b;
}

int __stdcall stdcall_add(int a, int b) {
	std::wcout << L"stdcall调用约定\n";
	return a + b;
}

int add_callback(stdcall_add_pointer add, int a, int b) {
	std::wcout << L"add_callback \n";
	return add(a, b);
}

int callback(const char* a, const wchar_t* b) {
	std::wcout << a;
	std::wcout << b;
	return wcslen(b);
}

int string_callback(cdecl_string_pointer callback, char* a, wchar_t* b) {
	std::string arg1 = "char* string";
	arg1.append(a);
	std::wstring arg2 = L"wchar_t* string";
	arg2.append(b);
	return callback(arg1.c_str(), arg2.c_str());
}


int console_print(CString* cs) {
	std::wcout << L"print CString: ";
	std::wcout << cs->s;
	std::wcout << L"\n";
	return cs->len;
}

class ThisClass {
public:
	__declspec(dllexport) int add3(int a, int b, int c) {
		std::wcout << L"ThisClass add3 \n";
		return a + b + c;
	}
};




int main()
{
	_setmode(_fileno(stdout), _O_WTEXT); // or _O_U16TEXT, either work
	_setmode(_fileno(stdin), _O_WTEXT);
	std::wcout << L"测试程序\n";
	cdecl_add(1, 1);
	stdcall_add(2, 2);
	CString* cs2 = new CString((wchar_t*)L"console_print结构体字符串");
	console_print(cs2);
	delete cs2;
	add_callback(stdcall_add, 1, 5);
	string_callback(callback, (char*)"aaaaaaaa", (wchar_t*)L"bbbbbbbbbbbbbbbbb");
	
	ThisClass tc;
	tc.add3(1, 2, 4);
	while (true) {
		Sleep(2000);
	}
}

