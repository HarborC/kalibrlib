cmake_minimum_required(VERSION 3.10)
project(numpy_eigen)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -D__STRICT_ANSI__")

find_package(Boost REQUIRED COMPONENTS system)
find_package(Eigen3 REQUIRED)

add_definitions(${EIGEN_DEFINITIONS})
include_directories(include ${EIGEN3_INCLUDE_DIRS})
include_directories("${PROJECT_SOURCE_DIR}/include/numpy_eigen")

# ignore "error: return-statement with a value, in function returning ‘void’" in "__multiarray_api.h"
add_compile_options(-fpermissive)

include_directories(include ${Boost_INCLUDE_DIRS})

IF(APPLE)
  link_directories( /usr/local/lib )
ENDIF(APPLE)

##############
## Building ##
##############

INCLUDE(src/autogen_files.cmake)
add_python_export_library(${PROJECT_NAME} ${AUTOGEN_FILES})

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES})

target_include_directories(${PROJECT_NAME} PUBLIC 
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

####################
## Installation ##
####################
install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)
