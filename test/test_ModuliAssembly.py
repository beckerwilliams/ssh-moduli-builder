#!/usr/bin/env python 3
from pathlib import PosixPath as Path
from unittest import TestCase, main

from moduli_assembly.ModuliAssembly import (ModuliAssembly, default_config)


def _delete_fs(path: Path):
    for file in path.iterdir():
        if file.is_file():
            file.unlink()
        else:
            _delete_fs(file)
    path.rmdir()


class TestModuliAssembly(TestCase):

    def setUp(cls):
        config_dir = Path.home().joinpath(".moduli_assembly")
        if config_dir.exists():
            _delete_fs(config_dir)
        cls.ma = ModuliAssembly()
        cls.moduli_dir = Path.home().joinpath('.moduli_assembly', '.moduli')

    def tearDown(cls):
        pass

    def test_ModuliAssembly_default_config(cls):
        cls.assertTrue(cls, cls.ma.config is not None)
        for attr in default_config():
            cls.assertTrue(cls, attr in cls.ma.config)
            cls.assertTrue(cls, 'generator_type' in cls.ma.config)
            cls.assertTrue(cls, 'auth_key_lengths' in cls.ma.config)
            cls.assertTrue(cls, 'config_file' in cls.ma.config)
            cls.assertTrue(cls, 'config_dir' in cls.ma.config)
            cls.assertTrue(cls, 'moduli_dir' in cls.ma.config)

    def test_ModuliAssembly_missing_attrs(cls):
        for attr in default_config():
            with cls.assertRaises(AttributeError) as exception:
                config = default_config()
                del config[attr]
                ModuliAssembly(config)
            print(f'Successful Exception Tested: {exception.exception}')

    def test_get_moduli_dir(cls):
        cls.assertEqual(cls.ma.get_moduli_dir(), cls.moduli_dir)

    def test_get_candidate_path(cls):
        # Vars for get_candidate_file
        key_length = 2048
        tpath = str(cls.ma.get_moduli_dir().joinpath(f'{key_length}.candidate_'))
        # cp = str(cls.ma.get_candidate_path(key_length))
        cls.assertTrue(tpath in str(cls.ma.get_candidate_path(key_length)))

    def test_get_screened_path(cls):
        key_length = 2048
        cp = cls.ma.get_candidate_path(key_length)
        sp = cls.ma.get_screened_path(cp)
        cls.assertTrue(str(sp).replace('screened', 'candidate') == str(cp.absolute()))

    def test_generate_and_screen_candidates(cls):
        candidate_file = cls.ma.generate_candidates(2048, 1)
        cls.assertTrue(candidate_file.exists())
        cls.assertTrue(candidate_file.stat().st_size > 1)
        cls.assertTrue(len(candidate_file.read_text().split('\n')) > 50000)

        screened_file = cls.ma.screen_candidates(candidate_file)
        cls.assertTrue(screened_file.exists())
        cls.assertTrue(screened_file.stat().st_size > 1)
        cls.assertTrue(len(screened_file.read_text().split('\n')) > 15)


if __name__ == '__main__':
    main()
