from cx_Freeze import setup, Executable
import os

includefiles = []
includes = []
excludes = ['Tkinter', 'numpy']
packages = []

for dirname, dirnames, filenames in os.walk('postit_rush/asset'):
    for filename in filenames:
        includefiles.append(os.path.join(dirname, filename))

setup(
    name = 'PostIT Rush!',
    version = "0.1",
    options = {'build_exe': {'excludes':excludes,'packages':packages,'include_files':includefiles}},
    executables = [Executable(script = 'run.pyw', base = 'Win32GUI', icon='postit_rush/postit_rush/asset/icon.ico')],
)
