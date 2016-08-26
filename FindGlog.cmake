# Try to find GLOG
# Once done, this will define
#
# GLOG_FOUND        - system has GLOG
# GLOG_INCLUDE_DIRS - GLOG include directories
# GLOG_LIBRARIES    - libraries need to use GLOG

find_path(
	GLOG_INCLUDE_DIR
	NAMES glog/logging.h
	PATHS ${CONAN_INCLUDE_DIRS_GLOG}
)

find_library(
	GLOG_LIBRARY
	NAMES glog
	PATHS ${CONAN_LIB_DIRS_GLOG}
)

set(GLOG_FOUND TRUE)
set(GLOG_INCLUDE_DIRS ${GLOG_INCLUDE_DIR})
set(GLOG_LIBRARIES ${GLOG_LIBRARY})

mark_as_advanced(GLOG_LIBRARY GLOG_INCLUDE_DIR)
