"""
Common utilities, most of them useful for a Qt related project.
"""

from collections import namedtuple
import os
import pathlib
import subprocess
import sys
import json
import importlib
from subprocess import run as run_proc
import shutil, tempfile
from typing import Iterable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtCore import QStandardPaths

all = [
    'msg_box', 'show_info', 'show_error',
    'add_table_widget_row', 'add_table_widget_rows',
    'load_qt_ui',
    'get_standard_location',
    'connectev',
    'compile_ui_if_needed',
    'compile_ui_if_needed_or_exit',

    'is_iterable',
    'ensure_iterable',
    'is_float',
    'is_int',

    'gen_unique_path_from',
    'overwrite_if_needed_or_exit',
    'exists_or_exit',
    'temporary_copy',
    'valid_path_for_file',
    'is_special_entry',
    'is_readable',
    'is_writable',
    'path_exists',

    'PipeData',
    'pipe_cmds',

    'dump_objs',
]

################################################################################
##
##      QT
##
################################################################################

UIC_COMPILER = 'pyside6-uic'
UI_COMPILATION_FAILURE_ERROR_CODE = 7

def msg_box(msg, icon_type):
    mbox = QMessageBox()
    mbox.setText(msg)
    mbox.setIcon(icon_type)
    mbox.exec()
#:

def show_info(msg, parent: QWidget | None = None):
    if parent:
        QMessageBox.information(parent, '', msg)
    else:
        msg_box(msg, icon_type=QMessageBox.Information)  # type: ignore
#:

def show_error(msg, parent: QWidget | None = None):
    if parent:
        QMessageBox.information(parent, '', msg)
    else:
        msg_box(msg, icon_type=QMessageBox.Critical)  # type: ignore
#:

def compile_ui_if_needed_or_exit(*compile_args, **compile_kargs):
    try: 
        compile_ui_if_needed(*compile_args, **compile_kargs)
    except Exception as ex:
        print(f"ERROR: {ex}", file=sys.stderr)
        sys.exit(UI_COMPILATION_FAILURE_ERROR_CODE)
#:

def compile_ui_if_needed(
        ui_file_path: str, 
        compiled_ui_file_path: str | None = None, 
        ignore_mtime = False
):
    """
    The following will dynamically compile the Qt Designer '.ui' file
    given by C{ui_file_path}, and import and load the generated Python
    module. The generated module will have the name: 
        
        C{ui_file_path} + '_ui.py'

    The '.ui' file will only be compiled if it's more recent that a
    previous instance of the generated module, or if this generated
    module doesn't exist at all (perhaps it's the first compilation).

    @param ui_file_path: The file path for the Qt Designer 'ui' file.
    @param ignore_mtime: If True, modification times for the ui file
    and the corresponding generated modules will be ignored and the
    ui file will ALWAYS be COMPILED.
    @throws ValueError, CompilationError
    @returns The imported and reloaded C{module} object.
    """
    if not os.path.exists(ui_file_path):
        raise ValueError(f"Can't find UI file {ui_file_path}")

    if not ui_file_path.endswith('.ui'):
        raise ValueError(f"UI file path ('{ui_file_path}') must end in '.ui'!")

    if compiled_ui_file_path:
        module_path = compiled_ui_file_path
        module_name = compiled_ui_file_path.strip('.py').replace('/', '.')
    else:
        module_name = ui_file_path.strip('.ui') + '_ui'
        module_path = module_name + '.py'
    module_name = module_name.replace('/', '.')

    ui_mtime = os.path.getmtime(ui_file_path)
    gen_mod_mtime = os.path.getmtime(module_path)

    module_temp_backup = None  # pys
    with TemporaryCopy(module_path) as module_temp_backup:
        try:
            if (
                    not os.path.exists(module_path) or 
                    (not ignore_mtime and ui_mtime > gen_mod_mtime)
                ):
                print(f"[+] Compiling '{ui_file_path}' to '{module_path}'.", file=sys.stderr)
                run_proc([UIC_COMPILER, '-o', module_path, ui_file_path])
                print(f"[+] Loading '{module_name}' module...", file=sys.stderr)


            # We want to make sure that the module is up to date, whether it 
            # was imported before or not. import_module won't really import the 
            # module if the module was imported before (it just returns the module
            # object). OTOH, reload won't reload if the module wasn't imported 
            # before. That's why wee need to import and then do a reload.
            importlib.invalidate_caches()
            module = importlib.reload(importlib.import_module(module_name))
            return module
        except Exception as ex:
            if module_temp_backup:
                print(f"[!] Restoring previous copy of {module_path}", file=sys.stderr)
                shutil.copy(module_temp_backup, module_path)
                os.utime(module_path, (gen_mod_mtime, gen_mod_mtime))
            raise UICompilationError(f"Compilation error: {ex}") from ex
#:

class UICompilationError(Exception):
    """
    An error other than ValueError than ocurred while compiling an 
    UI file.
    """
#:

def add_table_widget_row(
        table, 
        row_num, 
        row_obj, 
        editable=False, 
        extract_col_values=None,
):
    if not row_obj:
        raise ValueError("No row object (with column values) was given.")

    col_values = extract_col_values(row_obj) if extract_col_values else row_obj

    for col, col_val in enumerate(col_values):
        cell = QTableWidgetItem()
        cell.setText(col_val)
        flags = cell.flags()
        if editable:
            flags |= Qt.ItemFlags.ItemIsEditable    # type: ignore
        cell.setFlags(flags)
        table.setItem(row_num, col, cell)
#:

def add_table_widget_rows(
        table, 
        row_objs, 
        editable=False,
        extract_col_values=None,
):
    """
    Add a row to `table` for each object in `row_objs`. Rows will be 
    numbered from 1.
    """
    table.clearContents()
    table.setRowCount(len(row_objs))
    sorting_enabled = table.isSortingEnabled()
    table.setSortingEnabled(False)
    for row_num, row_obj in enumerate(row_objs):
        add_table_widget_row(
            table, 
            row_num,
            row_obj=row_obj,
            editable=editable,
            extract_col_values=extract_col_values,
        )
    table.setSortingEnabled(sorting_enabled)
#:

def get_standard_location(name: str, first_location_only=True) -> str | list[str]:
    """
    A wrapper for C{QStandardPaths.standardLocations} with predefined 
    keys:
        'home'    -> C{QStandardPaths.HomeLocation}
        'desktop' -> C{QStandardPaths.DesktopLocation}
        'docs'    -> C{QStandardPaths.DocumentsLocation}
        ... look at variable C{locs} to know the rest of the keys 

    This wrapper function returns a string with the first path found
    for the given C{name} if C{first_location_only} is C{True}, 
    otherwise all paths are returned. In some platforms it's possible
    to get several paths for the same key.
    """
    locs = {
        'home': QStandardPaths.HomeLocation,                    # type: ignore
        'desktop': QStandardPaths.DesktopLocation,              # type: ignore
        'docs': QStandardPaths.DocumentsLocation,               # type: ignore
        'apps_location': QStandardPaths.ApplicationsLocation,   # type: ignore
        'music': QStandardPaths.MusicLocation,                  # type: ignore
        'movies': QStandardPaths.MoviesLocation,                # type: ignore
        'pictures': QStandardPaths.PicturesLocation,            # type: ignore
        'config': QStandardPaths.ConfigLocation,                # type: ignore
    }
    paths = QStandardPaths.standardLocations(locs[name]) 
    return paths[0] if first_location_only else paths
#:

def connectev(
        widget, 
        event_name, 
        event_handler, 
        parent=None, 
        call_base_after=False,
        call_base_before=False
):
    """
    Connect C{event_handler} to the event given C{event_name}.
    C{event_name} must be a valid event for C{widget}. An optional
    C{parent} (eg, a window or dialog) can be passed and will
    be included in the call to C{event_handler} as the 1st argument.

    Example: 
    C{connectev(self.line_edit, 'keyPressEvent', self.method)}

    @param widget: The widget that responds to the event.
    @param event_name: A string with the event name (eg,
    C{'focusInEvent'})
    @param event_handler: A function to handle the event. It should
    have one or two parameters: the event object (not the name) and,
    if C{parent} is passed, this parent object. The event object is
    the last argument.
    @param parent: A parent widget. This can be useful if one wants
    to use an outside function as the event handler and still pass
    the parent widget for context.
    @param call_base_aftter: Whether to call the base event handler 
    after the new {event_handler}.
    @param call_base_before: Whether to call the base event handler 
    after the new {event_handler}.
    @return: Nothing.
    """
    def call_event_handler(event):
        if call_base_before:
            base_method(event)
        event_handler(event, *event_handler_args)
        if call_base_after:
            base_method(event)
    #:

    event_handler_args = (widget, parent) if parent else (widget,)
    base_method = getattr(widget, event_name)
    setattr(
        widget, 
        event_name,
        call_event_handler
    )
    setattr(
        widget, 
        f'__{event_name}_old_handler__',
        base_method
    )
#:

def disconnectev(
        widget, 
        event_name,
):
    base_method_name =  f'__{event_name}_old_handler__'
    if not (base_method := getattr(widget, base_method_name)):
        raise AttributeError(f'Reference to event {event_name} not found')
    #:
    setattr(
        widget,
        event_name,
        base_method
    )
    delattr(widget, base_method_name)
#:

#######################################################################
##
##   TYPES
##
#######################################################################

def is_float(txt: str) -> bool:
    try:
        float(txt)
    except:
        return False
    return True
#:

def is_int(txt: str, base = 10) -> bool:
    try:
        int(txt, base)
        # Note that int(23.2) => 23, but calling int(23.2, 10) (that is,
        # passing an explicit base) produces an exception. That's why
        # is_int(23.2) will always be False, even though int(23.2) makes
        # an int.
    except:
        return False
    return True
#:

def is_iterable(obj) -> bool:
    try:
        iter(obj)
    except TypeError:
        return False
    else:
        return True
#:

def ensure_iterable(obj_or_objs) -> Iterable:
    objs = obj_or_objs if is_iterable(obj_or_objs) else (obj_or_objs,)
    return (obj for obj in objs)
#:

#######################################################################
##
##   FILES, DIRECTORIES, PATHS
##
#######################################################################

def gen_unique_path_from(path_: str) -> str:
    """
    Generates a unique file path from C{path_} if the given {path_}
    exists. Otherwise, just returns that path.

    Returns a C{str} with the new unique path.

    >>> gen_unique_path_from('abc')   # assuming 'abc' exists
    abc_2
    >>> gen_unique_path_from('abc')   # assuming 'abc' doesn't exist
    abc
    >>> gen_unique_path_from('abc')   # assuming 'abc' and 'abc_2' both
    abc_3                             # exist
    """
    if not path_:
        raise ValueError('Empty path')
    path_ext = pathlib.Path(path_).suffix
    path_and_name = path_.partition(path_ext)[0] if path_ext else path_
    i = 2
    while os.path.exists(path_):
        path_ = f'{path_and_name}_{i}{path_ext}'
        i += 1
    return path_
#:

def overwrite_if_needed_or_exit(dest_file_path: str, error_code=3):
    if os.path.exists(dest_file_path):
        answer = input(f"File {dest_file_path} exists. Overwrite (y or n)? ")
        if answer.strip().lower() != 'y':
            print("File will not be overwritten")
            sys.exit(error_code)
#:

def exists_or_exit(file_path, error_code=3):
    if not os.path.exists(file_path):
        print(f"File {file_path} doesn't exist", file=sys.stderr)
        sys.exit(error_code)
#:

class TemporaryCopy():
    """
    Create a temporary copy of a file with a context manager.
    The file is copied and "yielded" when entering the managed
    code, and removed when exiting.
    Taken and adapted from:
        https://stackoverflow.com/a/43004895
    """
    def __init__(self, original_path: os.PathLike | str):
        self.original_path = original_path
    #:

    def __enter__(self):
        temp_dir = tempfile.gettempdir()
        base_path = os.path.basename(self.original_path)
        self.path = os.path.join(temp_dir,base_path)
        shutil.copy2(self.original_path, self.path)
        return self.path
    #:

    # def __exit__(self, exc_type, exc_val, exc_tb):
    def __exit__(self, *_):
        os.remove(self.path)
    #:
#:

def valid_path_for_file(
        file_path: str,
        unique = False,
        check_w = False,
        check_r = False,
) -> bool:
    """
    Returns `True` if `file_path`:
        - is not a path that is already being used by a dir., socket or 
          any type of entry other than a path available for a file
        - path to parent dir exists
        - has write permissions, if parameter `check_w` is `True`
        - has read permissions, if parameter `check_r` is `True`
        - doesn't exist if the `unique` is True.
    """
    try:
        path = pathlib.Path(file_path)
        return (
                not is_special_entry(path)
            and not path.is_dir()
            and path.parent.exists()
            and (not unique or not path.exists())
            and (not check_w or is_writable(path))
            and (not check_r or is_readable(path))
        )
    except:
        return False
#:

def is_special_entry(path: pathlib.Path | str) -> bool:
    """
    Whether this path is a special entry. A special entry is path that
    refers to either: block device, char. device, FIFO, junction, mount
    point, socket.
    """
    path = pathlib.Path(path)
    special_entries = (
        pathlib.Path.is_block_device, 
        pathlib.Path.is_char_device, 
        pathlib.Path.is_fifo,
        pathlib.Path.is_socket,
        pathlib.Path.is_junction,
        pathlib.Path.is_mount,
    )
    return any(special_entry_pred(path) for special_entry_pred in special_entries)
#:

def is_readable(path: pathlib.Path | str) -> bool:
    """
    A path is readable if it points to an existing entry and that
    entry is readable. 
    If the path is either an existing file, or a directory, the best
    way to check if it's readable is by trying to read from it. If the
    path is a file, we try to open it for reading. If the path is a
    directory, we try to check to see if we can list it with `os.walk`.
    If the path is a special entry, we use `os.access` to query its 
    flags, otherwise opening it may block the process.
    WARNING: Tested only on macOS.
    """
    path = pathlib.Path(path)
    if path.is_dir():
        return bool(next(os.walk(path), False))
    if path.is_file():
        try:
            file = open(path, 'r')
        except OSError:
            return False
        else:
            file.close()
            return True
    return os.access(path, os.R_OK)
#:

def is_writable(path: pathlib.Path | str) -> bool:
    """
    If the path already exists and is either a file or a special entry, 
    we use `os.access` to find out if the path is writable [1].
    If the path doesn't exists or points to a directory, there is no
    sure way to find if a path is writable before actually trying to 
    open it for writing. That's what we do here.
    If the path points to a directory, we try to create a temporary
    file inside of it. If the path is not a directory, then it doesn't
    exist (see [1]). In this case, the path is writable if we can 
    create a temporary file in the parent directory.
    WARNING: Tested only on macOS.
    """
    path = pathlib.Path(path)

    if path.is_file() or is_special_entry(path):
        return os.access(path, os.W_OK)

    try:
        if not path.is_dir():
            path = path.parent
        file = tempfile.TemporaryFile(dir=str(path)) 
    except OSError:
        return False
    else:
        file.close()
        return True
#:

def path_exists(path: pathlib.Path | str) -> bool:
    return os.path.exists(path)
#:

################################################################################
#
#   SHELL UTILS
#
################################################################################

PipeData = namedtuple('PipeData', 'returncode stdout stderr')

def pipe_cmds(cmd1_args: list[str], cmd2_args: list[str]) -> PipeData:
    """
    Pipes two commands and returns the return code and the output 
    (meaning, the contents of the standard output and standard error)
    of the second command. 
    """
    p1 = subprocess.Popen(
        cmd1_args,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    p2 = subprocess.Popen(
        cmd2_args,
        stdin = p1.stdout,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
    )
    p1.stdout.close()  # type: ignore
    data = p2.communicate()
    return PipeData(p2.returncode, data[0], data[1])
#:

#######################################################################
##
##   OTHER STUFF
##
#######################################################################

def dump_objs(objs_iter, dump_fn=json.dumps):
    """
    'Dumpa' um iterável de objectos do mesmo tipo para um array de 
    objectos de JSON. Recebe uma função para 'dumpar' os objectos 
    individuais. Atenção que em JSON só existe uma forma de representar 
    conjuntos de elementos: o array, que equivale a uma C{list}a em 
    Python. Assim sendo, esta função devolve um JSON-array que, à 
    semelhança de uma lista de Python, é delimitado por '[' e ']'.
    """
    return '[%s]' % ','.join((dump_fn(obj) for obj in objs_iter))
#:
