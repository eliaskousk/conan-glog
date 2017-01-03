from conan.packager import ConanMultiPackager
import platform

if __name__ == "__main__":
    builder = ConanMultiPackager()

    builder.add_common_builds(shared_option_name="glog:shared", pure_c=False)

    # Some isues on Linux and OSx when building on x86 the autotools version
    # of the library. Libtool complains about not finding dependent libraries.
    # Maybe in conanfile we are not passing correct environment variables to
    # correctly link the x86 builds, using the ConfigureEnvironment object.
    #
    # Latest glog uses CMake and doesn't have such issues, so use this if possible.
    # The package for this latest version is named 'glog/latest@eliaskousk/stable'
    # and uses the master branch of the package repo on Github.

    if platform.system() == "Linux" or platform.system() == "Darwin":
        filtered_builds = []
        for settings, options in builder.builds:
            if settings["arch"] != "x86":
                filtered_builds.append([settings, options])
        builder.builds = filtered_builds

    builder.run()
