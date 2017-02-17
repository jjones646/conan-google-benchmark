from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os, shutil, glob

class GoogleBenchmarkConan(ConanFile):
    name = 'benchmark'
    version = '1.1.0'
    description = 'A microbenchmark support library.'
    url = 'http://github.com/jjones646/conan-google-benchmark'
    license = 'https://github.com/google/benchmark/blob/v1.1.0/LICENSE'
    settings = 'arch', 'build_type', 'compiler', 'os'
    options =   { 'enable_lto': [True, False] }
    default_options = 'enable_lto=False'
    exports_sources = 'CMakeLists.txt', 'rt-lib.patch'
    generators = 'cmake'
    build_policy = 'missing'

    def source(self):
        archive_url = 'https://github.com/google/benchmark/archive/v{!s}.zip'.format(self.version)
        tools.download(archive_url, 'benchmark.zip')
        tools.check_sha256('benchmark.zip', '3f5321836cf531e621e0187ccbb1d836cd909994ed00c102a41385cbc1254e4e')
        tools.unzip('benchmark.zip')
        os.unlink('benchmark.zip')
        shutil.move('benchmark-{!s}'.format(self.version), 'benchmark')
        tools.patch(patch_file='rt-lib.patch', base_path='benchmark')

    def build(self):
        cmake = CMake(self.settings)
        gen_extra_args = list()
        gen_extra_args += ['-DBUILD_SHARED_LIBS=OFF']   # only support static library with conan
        gen_extra_args += ['-DCMAKE_INSTALL_PREFIX:PATH="{!s}"'.format(self.conanfile_directory)]
        gen_extra_args += ['-DBENCHMARK_ENABLE_TESTING=ON']   # always build the tests for packaging
        gen_extra_args += ['-DBENCHMARK_ENABLE_LTO={!s}'.format('ON' if self.options.enable_lto else 'OFF')]
        try:
            gen_extra_args += ['-DBENCHMARK_USE_LIBCXX={!s}'.format('ON' if (self.settings.compiler.libcxx == 'libc++') else 'OFF')]
        except ConanException:
            pass
        gen_extra_args = ' '.join(gen_extra_args)
        self.run('cmake "{!s}" {!s} {!s}'.format(self.conanfile_directory, cmake.command_line, gen_extra_args))
        build_extra_args = list()
        build_extra_args += ['-- -j -k'] if self.settings.compiler != 'Visual Studio' else ['']
        build_extra_args = ' '.join(build_extra_args)
        self.run('cmake --build . --target install {!s} {!s}'.format(cmake.build_config, build_extra_args))
        for f in glob.glob(os.path.join('bin', '*')):
            shutil.copy2(f, os.path.join('benchmark', 'test'))
        self.run('ctest -C {!s}'.format(self.settings.build_type))

    def package(self):
        self.copy(pattern='*.h', dst='include', src='include')
        self.copy(pattern='*{!s}*'.format(self.name), dst='lib', src='lib', keep_path=False)
        self.copy(pattern='conan_run.log', dst='.', keep_path=False)

    def package_info(self):
        # let consuming projects know what library name is used for linking
        self.cpp_info.libs = [self.name]
        if self.settings.os == 'Linux':
            self.cpp_info.libs.extend(['pthread', 'rt'])
        if self.settings.os == 'Windows':
            self.cpp_info.libs.append('shlwapi')
