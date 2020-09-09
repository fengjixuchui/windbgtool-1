import os
import shutil
import urllib.request
import zipfile

# https://githomelab.ru/pykd/pykd-ext/-/wikis/Downloads
pykd_ext_file = 'pykd_ext_2.0.0.24'
pykd_ext_zip_filename = pykd_ext_file + '.zip'
pykd_ext_url = r'https://githomelab.ru/pykd/pykd-ext/-/wikis/uploads/0bc82100609d24a8fcd1604203e782a6/' + pykd_ext_zip_filename
pykd_ext_folder = '.'

urllib.request.urlretrieve(pykd_ext_url, pykd_ext_zip_filename)
with zipfile.ZipFile(pykd_ext_zip_filename, 'r') as zip_ref:
    zip_ref.extractall(pykd_ext_folder)

if 'PROGRAMFILES(X86)' in os.environ:
    bits = '64bit'
else:
    bits = '32bit'

windbg_folders64 = []
windbg_folders32 = []

pykd_folder = r'\Lib\site-packages\pykd'
if bits == '64bit':
    windbg_folders64.append(os.environ["ProgramW6432"] + r'\Windows Kits\10\Debuggers\x64')
    windbg_folders64.append(os.environ["ProgramFiles(x86)"] + r'\Windows Kits\10\Debuggers\x64')
    windbg_folders64.append(os.environ["ProgramW6432"] + r'\Debugging Tools for Windows (x64)')

    windbg_folders32.append(os.environ["ProgramFiles(x86)"] + r'\Windows Kits\10\Debuggers\x86')
    windbg_folders32.append(os.environ["ProgramW6432"] + r'\Debugging Tools for Windows (x64)\Wow64')

elif bits == '32bit':
    windbg_folders32.append(os.environ["ProgramFiles"])

for windbg_folder in windbg_folders64:
    if not os.path.isdir(windbg_folder):
        continue

    src = pykd_ext_file + r'\x64\pykd.dll'
    dst = windbg_folder + '\winext'
    print('Copying "%s" -> "%s"' % (src, dst))
    shutil.copy(src, dst)

for windbg_folder in windbg_folders32:
    if not os.path.isdir(windbg_folder):
        continue

    src = pykd_ext_file + r'\x86\pykd.dll'
    dst = windbg_folder + '\winext'
    print('Copying "%s" -> "%s"' % (src, dst))
    shutil.copy(src, dst)
