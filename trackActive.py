from ctypes import windll, c_ulong, byref

def getForegroundWindowPID():
    hWnd = windll.user32.GetForegroundWindow()
    buf = c_ulong()
    pid = windll.user32.GetWindowThreadProcessId(hWnd, byref(buf))

    if buf.value:
        return buf.value
    else:
        return None
