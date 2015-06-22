# -*- mode: python -*-
a = Analysis(['fut_cheat.py'],
             pathex=['/home/tj/Development/FUTCheat'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FutCheat',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='/res/favicon.xpm')
