from conans import ConanFile, CMake
import os

username = os.getenv('CONAN_USERNAME', 'jjones646')
os.environ['CONAN_USERNAME'] = username
channel = os.getenv('CONAN_CHANNEL', 'testing')
os.environ['CONAN_CHANNEL'] = channel
log_run = os.getenv('CONAN_LOG_RUN_TO_FILE', '1')
os.environ['CONAN_LOG_RUN_TO_FILE'] = log_run

class BenchmarkConanPackageTest(ConanFile):
    settings =  {
                    'os': None,
                    'compiler': None,
                    'arch': None,
                    'build_type': ['Release', 'Debug']
                }
    requires = 'benchmark/1.2.0@{!s}/{!s}'.format(username, channel)
    generators = 'cmake'
    build_policy = 'missing'

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "{!s}" {!s}'.format(self.conanfile_directory, cmake.command_line))
        self.run('cmake --build . {!s}'.format(cmake.build_config))

    def imports(self):
        self.copy(pattern='*', dst='bin', src='bin')
        self.copy(pattern='*.dylib', dst='bin', src='lib')
        self.copy(pattern='*.pdb', dst='bin', src='lib')

    def test(self):
        self.run(os.sep.join(['.', 'bin', 'BenchmarkPackageTest']))
