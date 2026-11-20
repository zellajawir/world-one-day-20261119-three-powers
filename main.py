"""Write the single pre-rendered editorial image required by make.fun."""
import os
from pathlib import Path

if __name__ == '__main__':
    output = Path(os.environ.get('MAKEFUN_OUTPUT_DIR', '/output'))
    output.mkdir(parents=True, exist_ok=True)
    image = Path(__file__).resolve().with_name('entry.png')
    (output / 'entry.png').write_bytes(image.read_bytes())
