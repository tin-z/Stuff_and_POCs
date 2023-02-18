from distutils.core import setup, Extension

# the c++ extension module
MOD = "testfree"
extension_mod = Extension(MOD, ["test_free.c"])
setup(name = MOD, ext_modules=[extension_mod])

