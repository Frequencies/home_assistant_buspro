import pathlib
import py_compile
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class SmokeCompileTests(unittest.TestCase):
    def test_all_python_files_compile(self):
        py_files = [
            p for p in ROOT.rglob("*.py")
            if "/tests/" not in str(p).replace('\\', '/')
        ]
        self.assertGreater(len(py_files), 0)

        for path in py_files:
            with self.subTest(path=str(path)):
                out = pathlib.Path(tempfile.gettempdir()) / (path.stem + ".pyc")
                py_compile.compile(str(path), cfile=str(out), doraise=True)


if __name__ == "__main__":
    unittest.main()
