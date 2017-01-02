[![Build Status](https://travis-ci.org/eliaskousk/conan-glog.svg?branch=master)](https://travis-ci.org/eliaskousk/conan-glog)

# conan-glog

[Conan.io](https://conan.io) package for Google's GLog logging library

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py
    
## Upload packages to server

    $ conan upload glog/latest@eliaskousk/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install glog/latest@eliaskousk/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    glog/latest@eliaskousk/stable

    [options]
    glog:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install . 

Project setup installs the library (and all his dependencies) and generates the files
*conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that
you need to link with your dependencies.
