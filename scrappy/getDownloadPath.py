import platform
from pathlib import Path
import os

def get_default_download_path():
    system = platform.system()

    if system == "Windows":
        try:
            import ctypes
            from ctypes import wintypes
            from uuid import UUID

            KF_FLAG_DEFAULT = 0
            FOLDERID_Downloads = UUID('{374DE290-123F-4565-9164-39C4925E467B}')
            HRESULT = ctypes.c_long

            SHGetKnownFolderPath = ctypes.windll.shell32.SHGetKnownFolderPath
            SHGetKnownFolderPath.argtypes = [ctypes.POINTER(ctypes.c_byte * 16), wintypes.DWORD, wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)]
            SHGetKnownFolderPath.restype = HRESULT

            path_ptr = ctypes.c_wchar_p()
            r = SHGetKnownFolderPath((ctypes.c_byte * 16).from_buffer_copy(FOLDERID_Downloads.bytes_le), KF_FLAG_DEFAULT, 0, ctypes.byref(path_ptr))
            if r != 0:
                raise ctypes.WinError()
            path = path_ptr.value
            ctypes.windll.ole32.CoTaskMemFree(path_ptr)
            return Path(path)
        except Exception as e:
            print(" Error getting default download path, Error:", e)
            # fallback
            return Path.home() / "Downloads"

    elif system == "Darwin":  # macOS
        return Path.home() / "Downloads"

    else:  # Linux and others
        # Use XDG user dirs if available
        try:
            xdg_config_home = os.environ.get("XDG_CONFIG_HOME", os.path.join(Path.home(), ".config"))
            user_dirs_file = os.path.join(xdg_config_home, "user-dirs.dirs")

            if os.path.exists(user_dirs_file):
                with open(user_dirs_file) as f:
                    for line in f:
                        if line.startswith("XDG_DOWNLOAD_DIR"):
                            # Example: XDG_DOWNLOAD_DIR="$HOME/Downloads"
                            path = line.split("=")[1].strip().strip('"').replace("$HOME", str(Path.home()))
                            return Path(path)
        except Exception:
            pass

        # fallback
        return Path.home() / "Downloads"


if __name__ == "__main__":
    print(get_default_download_path())