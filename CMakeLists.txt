cmake_minimum_required(VERSION 3.10)
project(kalibr)

find_package(Eigen3 REQUIRED)

# SuiteSparse (CHOLMOD 等)
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)

include(add_python_export_library)

find_package(SuiteSparse REQUIRED)

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})

include_directories(
  ${EIGEN3_INCLUDE_DIRS}
  ${CHOLMOD_INCLUDE_DIR}
)

add_subdirectory(src)