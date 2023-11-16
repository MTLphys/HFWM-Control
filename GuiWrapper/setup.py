from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('GuiWrapper.py', base=base, target_name = 'HFWMControl')
]

setup(name='GuiWrapper',
      version = '0.1',
      description = 'Simple Interface tool for HFWM conrol',
      options = {'build_exe': build_options},
      executables = executables)
