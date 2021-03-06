from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake, ConfigureEnvironment

class GLogConan(ConanFile):
    name = "glog"
    version = "0.3.4"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "gflags": [True, False], "multithreaded": [True, False], "fpic": [True, False]}
    default_options = "shared=True", "gflags=True", "multithreaded=True", "fpic=True"
    url="http://github.com/eliaskousk/conan-glog"
    license="https://www.apache.org/licenses/LICENSE-2.0"
    exports= "CMakeLists.txt", "FindGlog.cmake", "change_dylib_names.sh"
    zip_name = "v%s.tar.gz" % version
    unzipped_name = "glog-%s" % version

    def config(self):
        if self.options.gflags == True:
            self.requires.add("gflags/2.2.0@eliaskousk/stable", private=False)
            self.options['gflags'].shared = True

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
        env = ConfigureEnvironment(self)
        if self.options.fpic:
            env_line = env.command_line.replace('CFLAGS="', 'CFLAGS="-fPIC ')
            env_line = env.command_line.replace('CXXFLAGS="', 'CXXFLAGS="-fPIC ')
        self.run("cd %s && %s autoreconf -fvi" % (self.unzipped_name, env.command_line_env))
        self.run("cd %s && %s ./configure %s %s %s --prefix=`pwd`/../_build" % (self.unzipped_name,
                                                                                env.command_line_env,
                                                                                gflags, shared, static))
        self.run("cd %s && %s make && make install" % (self.unzipped_name, env.command_line_env))

    def package(self):
        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findglog script into project
        self.copy("FindGlog.cmake", ".", ".")

        # Copying headers
        self.copy(pattern="*.h", dst="include", src="_build/include", keep_path=True)

        libdir = "_build/lib"
        if self.options.shared:
            # Copying dynamic libs
            self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
            self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
            self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)
        else:
            # Copying static libs
            self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)

        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['glog']

        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

