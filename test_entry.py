"""Verify the exact program output, using a networking-denied interpreter."""
import os
import runpy
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent

class EntryTest(unittest.TestCase):
    def test_two_offline_runs_create_the_same_single_valid_sized_png(self):
        self.assertTrue((ROOT / 'main.py').is_file(), 'competition entrypoint is missing')
        check = '''import runpy, sys

def deny(event, _args):
    if event.startswith(('socket.', 'subprocess.')) or event == 'os.system':
        raise RuntimeError(f'Unexpected external operation: {event}')

sys.addaudithook(deny)
runpy.run_path(sys.argv[1], run_name="__main__")'''
        outputs = []
        for _ in range(2):
            with tempfile.TemporaryDirectory() as folder:
                output = Path(folder) / 'output'
                env = os.environ | {'MAKEFUN_OUTPUT_DIR': str(output)}
                subprocess.run([sys.executable, '-I', '-S', '-c', check,
                                str(ROOT / 'main.py')], cwd=folder, env=env, check=True)
                self.assertEqual([p.name for p in output.iterdir()], ['entry.png'])
                outputs.append((output / 'entry.png').read_bytes())
        self.assertEqual(outputs[0], outputs[1])
        png = outputs[0]
        self.assertLessEqual(len(png), 1 << 20)
        self.assertEqual(png[:16], b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR')
        w, h, depth, color, compression, filter_method, interlace = struct.unpack('>IIBBBBB', png[16:29])
        self.assertTrue(1 <= w <= 1024 and 1 <= h <= 1024)
        self.assertEqual((depth, color, compression, filter_method, interlace), (8, 2, 0, 0, 0))
        self.assertEqual(png[-12:], b'\x00\x00\x00\x00IEND\xaeB`\x82')

if __name__ == '__main__':
    unittest.main()
