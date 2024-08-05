import sys
import matplotlib
from cx_Freeze import setup, Executable
from PyQt5.QtWidgets import QApplication, QMessageBox

try:
    # Application main script
    script = "main.py"

    # Include files (additional files to include in the build)
    include_files = [
        (matplotlib.get_data_path(), "mpl-data"),
        ("path/to/data", "data")  # Add the data folder and its contents
    ]

    # Packages to include
    packages = [
        "matplotlib", 
        "numpy",
        "PyQt5.QtWidgets"
    ]

    # Include additional dynamic libraries if needed
    # bin_path_includes = [
    #     os.path.join(os.path.dirname(sys.executable), "Library", "bin", "mkl_core.dll"),
    #     os.path.join(os.path.dirname(sys.executable), "Library", "bin", "mkl_def.dll"),
    #     os.path.join(os.path.dirname(sys.executable), "Library", "bin", "mkl_intel_thread.dll"),
    #     os.path.join(os.path.dirname(sys.executable), "Library", "bin", "mkl_rt.dll"),
    #     os.path.join(os.path.dirname(sys.executable), "Library", "bin", "libiomp5md.dll"),
    # ]

    # Output directory
    build_exe_options = {
        "packages": packages,
        "excludes": [],
        "include_files": [(matplotlib.get_data_path(), "mpl-data"), ("./ui", "ui")],
        "build_exe": "C:/myproject/build"  # Specify the output directory
    }

    # Base
    base = None
    if sys.platform == "win32":
        base = "Win32GUI"  # Use "Win32GUI" for GUI applications

    setup(
        name="OVERTIME",
        version="1.6",
        description="DOOCH OVERTIME",
        executables=[
            Executable(
                "main.py",
                copyright="Copyright (C) 2023 cx_Freeze",
                # base="C:\Python Workplace\Make_ERP",
                icon="warehouse.ico",
            ),
        ],
        options={
            "build_exe": build_exe_options,
            # "bdist_msi": bdist_msi_options,
        },
    )
except Exception as e:
    app = QApplication(sys.argv)
    msg = QMessageBox()
    msg.setWindowTitle("Error")
    msg.setText(str(e))
    msg.exec_()
