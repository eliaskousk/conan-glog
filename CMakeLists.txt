PROJECT(conanglog)
cmake_minimum_required(VERSION 2.8)
include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()
add_subdirectory("./glog-0.3.4")
