import unittest
from pathlib import PosixPath as Path

# from moduli_assembly.__main__ import (create_moduli_dir, clear_artifacts, generate_candidates, get_candidate_path,
#                                       get_screened_path, load_conf, restart_candidate_screening, rm_config_dir,
#                                       screen_candidates, version, write_moduli_file)
from moduli_assembly.moduli_assembly_conf import load_conf


class TestModuliAssembly(unittest.TestCase):

    # Setup test, test values below
    def test_is_prime(self):
        conf = load_conf(MODULI_DIR=Path("DOTmdtemp"), conf=Path("DOTconfig"))
        self.assertTrue(conf["MODULI_DIR"].exists())
        self.assertTrue(conf["MODULI_DIR"].joinpath(".moduli").is_dir())
        # finally
        Path("DOTconfig").unlink(missing_ok=True)
        Path("DOTmdtemp").joinpath(".moduli").rmdir()
        Path("DOTmdtemp").rmdir()


if __name__ == '__main__':
    unittest.main()
