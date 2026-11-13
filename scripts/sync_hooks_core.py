#!/usr/bin/env python3
"""Kopiuje src/symetria_dowodowa/core.py do pluginu hooków (pluginy instalują się osobno,
więc hooki nie mogą importować kodu z drugiego pluginu). Test pilnuje identyczności."""
from pathlib import Path
import shutil
root = Path(__file__).resolve().parents[1]
src = root / "plugins/symetria-dowodowa-tknc/src/symetria_dowodowa/core.py"
dst = root / "plugins/symetria-prawna-hooki/hooks/symetria_core.py"
shutil.copyfile(src, dst)
print(f"OK: {dst.relative_to(root)} = {src.relative_to(root)}")
