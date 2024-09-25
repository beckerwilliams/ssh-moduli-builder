#!/usr/bin/env python 3
from unittest import TestCase, main

from moduli_assembly.ModuliAssembly import (ModuliAssembly, _default_config)


class TestModuliAssembly(TestCase):
    #
    @classmethod
    def setUp(cls):
        cls.ma = ModuliAssembly()

    @classmethod
    def test_ModuliAssembly_default_config(cls):
        cls.assertTrue(cls, cls.ma.config is not None)
        for attr in _default_config():
            cls.assertTrue(cls, attr in cls.ma.config)
            cls.assertTrue(cls, 'generator_type' in cls.ma.config)
            cls.assertTrue(cls, 'auth_bitsizes' in cls.ma.config)
            cls.assertTrue(cls, 'config_file' in cls.ma.config)
            cls.assertTrue(cls, 'config_dir' in cls.ma.config)
            cls.assertTrue(cls, 'moduli_dir' in cls.ma.config)

    def test_ModuliAssembly_missing_attrs(cls):
        """
        Validate throws Exception on Missing Attributes

        :return:
        :rtype:
        """
        for attr in _default_config():
            with cls.assertRaises(AttributeError) as exception:
                config = _default_config()
                del config[attr]
                ma = ModuliAssembly(config)
            print(f'Exception Tested: {exception.exception}')

    @classmethod
    def test_get_moduli_dir(cls):
        cls.assertEqual(False)

    @classmethod
    def test_get_candidate_path(cls):
        cls.assertTrue(False)

    @classmethod
    def test_get_screened_path(cls):
        cls.assertTrue(False)

    @classmethod
    def test_screen_candidates(cls):
        cls.assertTrue(False)

    @classmethod
    def test_generate_candidates(cls):
        cls.assertTrue(False)

    @classmethod
    def test_write_moduli_file(cls):
        cls.assertTrue(False)

    @classmethod
    def test_restart_candidate_screening(cls):
        cls.assertTrue(False)

    def test_clear_artifacts(cls):
        cls.assertTrue(False)


if __name__ == '__main__':
    main()
