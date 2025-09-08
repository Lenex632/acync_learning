from typing import Iterable, Tuple
import select


def check_ready_to(files_for_read: Iterable,
                   files_for_write: Iterable,
                   timeout: int | float) -> Tuple[bool, bool, bool]:
    try:
        is_files_for_read, is_files_for_write, _ = select.select(files_for_read, files_for_write, [], timeout)
        is_files_for_read = True if is_files_for_read else False
        is_files_for_write = True if is_files_for_write else False
        is_timeout = not (is_files_for_read or is_files_for_write)
    except Exception:
        is_files_for_read, is_files_for_write, is_timeout = False, False, False
    finally:
        return is_files_for_read, is_files_for_write, is_timeout

