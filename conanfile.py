from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class GLogConan(ConanFile):
    name = "glog"
    version = "0.3.4"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "gflags": [True, False], "multithreaded": [True, False]}
    default_options = "shared=True", "gflags=True", "multithreaded=True"
    url="http://github.com/eliaskousk/conan-glog"
    license="https://www.apache.org/licenses/LICENSE-2.0"
    exports= "CMakeLists.txt", "FindGlog.cmake", "change_dylib_names.sh"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "glog-%s" % version

    def config(self):
        if self.options.gflags == True:
            self.requires.add("gflags/2.2.0@eliaskousk/stable", private=False)

    def source(self):
        url = "https://github.com/google/glog/archive/%s" % self.zip_name
        download(url, self.zip_name)
        unzip(self.zip_name)
        os.unlink(self.zip_name)

        # Or clone the repo and possibly checkout a branch
        #
        # self.run("git clone https://github.com/google/glog.git glog-%s" % self.version)
        # self.run("cd glog-%s && git checkout v0.3.4" % self.version)

    def build(self):
        gflags_path = self.deps_cpp_info["gflags"].rootpath
        gflags = "--with-gflags=%s" % gflags_path if self.options.gflags else ""
        shared ="--enable-static=no" if self.options.shared else ""
        static ="--enable-shared=no" if not self.options.shared else ""

        self.run("cd %s && autoreconf --force --install && ./configure --prefix=`pwd`/../_build %s %s %s && make && make install" % (self.unzipped_name, gflags, shared, static))

        # When using CMake to build
        #
        # cmake = CMake(self.settings)
        # if self.settings.os == "Windows":
            # self.run("IF not exist _build mkdir _build")
        # else:
            # self.run("mkdir _build")
        # cd_build = "cd _build"
        # gflags = "-DWITH_GFLAGS=1" if self.options.gflags else ""
        # multithreaded = "-DWITH_THREADS=1" if self.options.multithreaded else ""
        # shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        # self.run('%s && cmake .. %s %s %s %s' % (cd_build, cmake.command_line, shared, gflags, multithreaded))
        # self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findglog script into project
        self.copy("FindGlog.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="_build/include", keep_path=True)

        # When using CMake to build
        #
        # self.copy(pattern="*.h", dst="include/glog", src="_build/glog-%s/glog" % self.version, keep_path=True)

        libdir = "_build/lib"
        # Copying static and dynamic libs
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['glog']
