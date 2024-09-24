#!/usr/bin/env python 3
from unittest import TestCase, main

from moduli_assembly.ModuliAssembly import ModuliAssembly


def _default_config():
    """
    tbd - REMOVE Keylength 2048 BEFORE PRODUCTION
    :return:
    :rtype:
    """
    return {
        "generator_type": 2,
        "auth_bitsizes": ["2048", "3072", "4096", "6144", "7680", "8192"],
        "config_dir": ".moduli_assembly",
        "config_file": ".config",
        "moduli_dir": ".moduli"
    }


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
        pass

    @classmethod
    def test_get_candidate_path(cls):
        pass

    @classmethod
    def test_get_screened_path(cls):
        pass

    @classmethod
    def test_screen_candidates(cls):
        pass

    @classmethod
    def test_generate_candidates(cls):
        pass

    @classmethod
    def test_write_moduli_file(cls):
        pass

    @classmethod
    def test_restart_candidate_screening(cls):
        pass

    @classmethod
    def test_clear_artifacts(cls):
        pass


if __name__ == '__main__':
    main()
