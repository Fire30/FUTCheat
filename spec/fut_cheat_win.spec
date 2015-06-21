# -*- mode: python -*-
a = Analysis(['fut_cheat.py'],
             pathex=['c:\\Users\\TJ\\Documents\\FUTCheat'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
a.datas += [('res\\favicon.ico','res\\favicon.ico','DATA')]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='fut_cheat.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='res\\favicon.ico')
