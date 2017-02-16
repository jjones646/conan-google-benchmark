from conan.packager import ConanMultiPackager
import os

username = os.getenv('CONAN_USERNAME', 'jjones646')
os.environ['CONAN_USERNAME'] = username
channel = os.getenv('CONAN_CHANNEL', 'stable')
os.environ['CONAN_CHANNEL'] = channel
log_run = os.getenv('CONAN_LOG_RUN_TO_FILE', '1')
os.environ['CONAN_LOG_RUN_TO_FILE'] = log_run

def get_builds_with_options(builder):
    builds = []
    for settings, options in builder.builds:
        builds.append([settings, {'benchmark:enable_lto':True}])
        builds.append([settings, {'benchmark:enable_lto':False}])
    return builds

if __name__ == '__main__':
    builder = ConanMultiPackager(
        gcc_versions=['4.8', '4.9', '5.2', '5.3', '5.4', '6.2'],
        apple_clang_versions=['8.0'],
        visual_versions=['14'],
        archs=['x86_64', 'x86'],
        use_docker=False,
        upload=False,
        username=username,
        channel=channel,
        reference='benchmark/1.1.0',
    )
    builder.add_common_builds(pure_c=False)
    builder.builds = get_builds_with_options(builder)
    builder.run()
