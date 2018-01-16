import os

from conans import ConanFile, CMake


class BenchmarkConanPackageTest(ConanFile):
    settings = {
        'os': None,
        'compiler': None,
        'arch': None,
        'build_type': ['Release', 'Debug']
    }
    generators = 'cmake'
    build_policy = 'missing'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        for ext in ('.dll', '.pdb'):
            self.copy(pattern='*{!s}'.format(ext), dst='bin', src='bin')
        for ext in ('.lib', '.a', '.so*', '.dylib*'):
            self.copy(pattern='*{!s}'.format(ext), dst='lib', src='lib')

    def test(self):
        self.run(os.sep.join(['.', 'bin', 'BenchmarkPackageTest']))
