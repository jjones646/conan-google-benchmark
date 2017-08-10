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
    for settings, options, env_vars, build_requires in builder.builds:
        builds.append([settings, {'benchmark:enable_lto':True}, env_vars, build_requires])
        builds.append([settings, {'benchmark:enable_lto':False}, env_vars, build_requires])
        builds.append([settings, {'benchmark:enable_exceptions':True}, env_vars, build_requires])
        builds.append([settings, {'benchmark:enable_exceptions':False}, env_vars, build_requires])
    return builds

if __name__ == '__main__':
    builder = ConanMultiPackager(
        gcc_versions=['4.9', '5.2', '5.3', '5.4', '6.2', '6.3', '6.4', '7.1'],
        apple_clang_versions=['6.1', '7.0', '7.3', '8.0', '8.1'],
        visual_versions=['12', '14'],
        archs=['x86_64', 'x86'],
        username=username,
        channel=channel,
        reference='benchmark/1.2.0',
    )
    builder.add_common_builds(pure_c=False)
    builder.builds = get_builds_with_options(builder)
    builder.run()
