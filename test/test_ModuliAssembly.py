#!/usr/bin/env python 3
from pathlib import PosixPath as Path
from unittest import TestCase, main

from moduli_assembly.ModuliAssembly import (ModuliAssembly, default_config)


class TestModuliAssembly(TestCase):

    def setUp(cls):
        cls.ma = ModuliAssembly()
        cls.moduli_dir = Path.home().joinpath('.moduli_assembly', '.moduli')

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
        """
        Validate throws Exception on Missing Attributes

        :return:
        :rtype:
        """
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
        cp = str(cls.ma.get_candidate_path(key_length))
        cls.assertTrue(tpath in cp)

    def test_get_screened_path(cls):
        key_length = 2048
        cp = cls.ma.get_candidate_path(key_length)
        sp = str(cls.ma.get_screened_path(cp).absolute())
        cls.assertTrue(str(sp).replace('screened', 'candidate') == str(cp.absolute()))

    def test_generate_candidates(cls):
        """
        Here's we'll attempt generation with one key_length, 2048,
        and test the Return CANDIDATE File for Candidate ENTRIES
        :return:
        :rtype:
        """
        # key_length = 2048
        # candidates_file = cls.ma.generate_candidates(key_length)
        # cf = candidates_file.read_text()
        # # Validate Each File Exists and is Non-Zero
        # tbd
        cls.assertTrue(False)
        
    #
    # def test_write_moduli_file(cls):
    #     cls.assertTrue(False, True)
    #
    # def test_restart_candidate_screening(cls):
    #     cls.assertTrue(False, True)
    #
    # def test_clear_artifacts(cls):
    #     cls.assertTrue(False, True)


if __name__ == '__main__':
    main()
