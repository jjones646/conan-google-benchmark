import os
import shutil

from conans import ConanFile, CMake, tools
from conans.errors import ConanException


class GoogleBenchmarkConan(ConanFile):
    name = 'benchmark'
    version = '1.3.0'
    description = 'A microbenchmark support library.'
    url = 'http://github.com/jjones646/conan-google-benchmark'
    license = 'https://github.com/google/benchmark/blob/v1.3.0/LICENSE'
    settings = 'arch', 'build_type', 'compiler', 'os'
    options = {
        'enable_lto': [True, False],
        'enable_exceptions': [True, False]
    }
    default_options = 'enable_lto=False', 'enable_exceptions=True'
    exports_sources = 'CMakeLists.txt'
    generators = 'cmake'
    build_policy = 'missing'

    def source(self):
        archive_url = 'https://github.com/google/benchmark/archive/v{!s}.zip'.format(self.version)
        tools.download(archive_url, 'benchmark.zip')
        tools.check_sha256('benchmark.zip', '51c2d2d35491aea83aa6121afc4a1fd9262fbd5ad679eb5e03c9fa481e42571e')
        tools.unzip('benchmark.zip')
        os.unlink('benchmark.zip')
        shutil.move('benchmark-{!s}'.format(self.version), 'benchmark')

    def build(self):
        cmake = CMake(self, parallel=True)
        cmake.definitions['BUILD_SHARED_LIBS'] = 'OFF'  # only support static library with conan
        cmake.definitions['BENCHMARK_ENABLE_TESTING'] = 'OFF'
        cmake.definitions['BENCHMARK_ENABLE_LTO'] = 'ON' if self.options.enable_lto else 'OFF'
        cmake.definitions['BENCHMARK_ENABLE_EXCEPTIONS'] = 'ON' if self.options.enable_exceptions else 'OFF'
        cmake.definitions['BENCHMARK_BUILD_32_BITS'] = 'ON' if '64' not in str(self.settings.arch) else 'OFF'
        try:
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'ON' if (self.settings.compiler.libcxx == 'libc++') else 'OFF'
        except ConanException:
            pass
        cmake.configure()
        cmake.build(target='install')

    def package(self):
        self.copy(pattern='*.h', dst='include', src='include')
        self.copy(pattern='*{!s}*'.format(self.name), dst='lib', src='.', keep_path=False)
        self.copy(pattern='conan_run.log', dst='.', keep_path=False)

    def package_info(self):
        # let consuming projects know what library name is used for linking
        self.cpp_info.libs = [self.name]
        if self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['pthread', 'rt'])
        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('shlwapi')
