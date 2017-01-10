from conans import ConanFile
import os
from conans import CMake

class GLogConan(ConanFile):
    name = "glog"
    version = "latest"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "gflags": [True, False], "multithreaded": [True, False]}
    default_options = "shared=True", "gflags=True", "multithreaded=True"
    url="http://github.com/eliaskousk/conan-glog"
    license="https://www.apache.org/licenses/LICENSE-2.0"
    exports= "CMakeLists.txt", "FindGlog.cmake", "change_dylib_names.sh"
    # zip_name = "%s.tar.gz" % version
    # unzipped_name = "glog-%s" % version
    folder_name = "glog-%s" % version

    def config(self):
        if self.options.gflags == True:
            self.requires.add("gflags/2.2.0@eliaskousk/stable", private=False)
            self.options['gflags'].shared = True

    def source(self):
        self.run("git clone https://github.com/google/glog.git %s" % self.folder_name)
        self.run("cd %s && git checkout master" % self.folder_name)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        gflags = "-DWITH_GFLAGS=1" if self.options.gflags else ""
        multithreaded = "-DWITH_THREADS=1" if self.options.multithreaded else ""
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run('%s && cmake .. %s %s %s %s' % (cd_build, cmake.command_line, shared, gflags, multithreaded))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findglog script into project
        self.copy("FindGlog.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include/glog", src="_build/%s/glog" % self.folder_name, keep_path=True)
        self.copy(pattern="*.h", dst="include/glog", src="%s/src/glog" % self.folder_name, keep_path=True)

        # Copying static libs
        libdir = "_build/lib"
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)

        # Copying dynamic libs
        libdir = "_build/%s" % self.folder_name
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

        bindir = "_build/bin"
        # Copying binaries
        self.copy(pattern="*", dst="bin", src=bindir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['glog']

