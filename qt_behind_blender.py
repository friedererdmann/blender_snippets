import ctypes
import os
from ctypes import wintypes
from collections import namedtuple
from PySide2.QtWidgets import QApplication

        
def get_process_hwnds():
    # https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    def check_zero(result, func, args):    
        if not result:
            err = ctypes.get_last_error()
            if err:
                raise ctypes.WinError(err)
        return args

    if not hasattr(wintypes, 'LPDWORD'): # PY2
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

    WindowInfo = namedtuple('WindowInfo', 'title hwnd')

    WNDENUMPROC = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HWND,    # _In_ hWnd
        wintypes.LPARAM,) # _In_ lParam

    user32.EnumWindows.errcheck = check_zero
    user32.EnumWindows.argtypes = (
       WNDENUMPROC,      # _In_ lpEnumFunc
       wintypes.LPARAM,) # _In_ lParam

    user32.IsWindowVisible.argtypes = (
        wintypes.HWND,) # _In_ hWnd

    user32.GetWindowThreadProcessId.restype = wintypes.DWORD
    user32.GetWindowThreadProcessId.argtypes = (
      wintypes.HWND,     # _In_      hWnd
      wintypes.LPDWORD,) # _Out_opt_ lpdwProcessId

    user32.GetWindowTextLengthW.errcheck = check_zero
    user32.GetWindowTextLengthW.argtypes = (
       wintypes.HWND,) # _In_ hWnd

    user32.GetWindowTextW.errcheck = check_zero
    user32.GetWindowTextW.argtypes = (
        wintypes.HWND,   # _In_  hWnd
        wintypes.LPWSTR, # _Out_ lpString
        ctypes.c_int,)   # _In_  nMaxCount
        
    def list_windows():
        '''Return a sorted list of visible windows.'''
        result = []
        @WNDENUMPROC
        def enum_proc(hWnd, lParam):
            if user32.IsWindowVisible(hWnd):
                pid = wintypes.DWORD()
                tid = user32.GetWindowThreadProcessId(
                            hWnd, ctypes.byref(pid))
                length = user32.GetWindowTextLengthW(hWnd) + 1
                title = ctypes.create_unicode_buffer(length)
                user32.GetWindowTextW(hWnd, title, length)
                current_pid = os.getpid()
                if pid.value == current_pid:
                    result.append(WindowInfo(title.value, hWnd))
            return True
        user32.EnumWindows(enum_proc, 0)
        return sorted(result)
    
    return list_windows()

def get_window_z_order():
    '''Returns windows in z-order (top first)'''
    # https://stackoverflow.com/questions/6381198/get-window-z-order-with-python-windows-extensions
    user32 = ctypes.windll.user32
    lst = []
    top = user32.GetTopWindow(None)
    if not top:
        return lst
    lst.append(top)
    while True:
        next = user32.GetWindow(lst[-1], 2)
        if not next:
            break
        lst.append(next)
    return lst

'''
def get_qt_window_order():
    window_order = get_window_z_order()
    app = QApplication.instance()
    qt_windows = app.topLevelWidgets()
    qt_window_ids = [window.winId() for window in qt_windows]
    return qt_window_ids
    # return order_window_list(qt_window_ids)


def order_window_list(list_of_windows=[]):
    all_windows_ordered_list = get_window_z_order()
    ordered_list = []
    for window in all_windows_ordered_list:
        if window in list_of_windows:
            ordered_list.append(window)
    return ordered_list
'''

# qt_order = get_qt_window_order()
all_windows = get_window_z_order()
process_windows = get_process_hwnds() 

# blender_windows = [b_window.hwnd for b_window in process_windows if b_window.hwnd not in qt_order]
window_dict = {wind.hwnd: wind.title for wind in process_windows}

print("Sort order is:")
i = 0
for window in all_windows:
    if window in window_dict:
        print("\t", i, window_dict[window])
    i += 1
