import ctypes
import os
from ctypes import wintypes
from collections import namedtuple
from PySide2.QtWidgets import QApplication

        
def get_blender_hwnd():
    # https://stackoverflow.com/questions/37501191/how-to-get-windows-window-names-with-ctypes-in-python
    blender_pid = os.getpid()
    global blender_hwnd
    blender_hwnd = 0
    user32 = ctypes.WinDLL('user32', use_last_error=True)

    def check_zero(result, func, args):    
        if not result:
            err = ctypes.get_last_error()
            if err:
                raise ctypes.WinError(err)
        return args

    if not hasattr(wintypes, 'LPDWORD'): # PY2
        wintypes.LPDWORD = ctypes.POINTER(wintypes.DWORD)

    WindowInfo = namedtuple('WindowInfo', 'pid title')

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
            global blender_hwnd
            if user32.IsWindowVisible(hWnd):
                pid = wintypes.DWORD()
                tid = user32.GetWindowThreadProcessId(
                            hWnd, ctypes.byref(pid))
                length = user32.GetWindowTextLengthW(hWnd) + 1
                title = ctypes.create_unicode_buffer(length)
                user32.GetWindowTextW(hWnd, title, length)
                result.append(WindowInfo(pid.value, title.value))
                if pid.value == blender_pid and "Blender" in title.value:
                    blender_hwnd = hWnd
            return True
        user32.EnumWindows(enum_proc, 0)
        return sorted(result)
    
    list_windows()
    return blender_hwnd


def get_window_order():
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


def get_qt_window_order():
    window_order = get_window_order()
    app = QApplication.instance()
    qt_windows = app.topLevelWidgets()
    qt_window_ids = [window.winId() for window in qt_windows]
    qt_ordered_ids = []
    for window in window_order:
        if window in qt_window_ids:
            qt_ordered_ids.append(window)
    return qt_ordered_ids


qt_order = get_qt_window_order()
all_windows = get_window_order()
blender_main = get_blender_hwnd() 

print("QTWidget HWND in order are {0}".format(qt_order))
print("Blender's HWND is {0}".format(blender_main))
print("Sort order is:")
i = 1
for window in all_windows:
    if window == blender_main:
        print("\t{0} Blender".format(str(i)))
        i += 1
    if window in qt_order:
        print("\t{0} QtWidget {1}".format(str(i), str(window)))
        i += 1

if qt_order:
    z_blender = all_windows.index(blender_main)
    z_qt = all_windows.index(qt_order[-1])
    if z_blender < z_qt:
        print("Blender is covering at least one of the QtWindows")
