cmake_minimum_required(VERSION 3.10)
project(sm_python)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Eigen3 REQUIRED)

add_definitions(-fPIC)
add_definitions(-D__STRICT_ANSI__)
  
include_directories(include ${EIGEN3_INCLUDE_DIRS})

find_package(Boost REQUIRED COMPONENTS system serialization)

##############
## Building ##
##############
add_python_export_library(${PROJECT_NAME}
  src/module.cpp
  src/export_rotational_kinematics.cpp
  src/export_rotations.cpp
  src/export_transformations.cpp
  src/export_quaternion_algebra.cpp
  src/export_homogeneous.cpp
  src/exportTransformation.cpp
  src/exportHomogeneousPoint.cpp
  src/exportTimestampCorrector.cpp
  src/exportPropertyTree.cpp
  src/exportEigen.cpp
  src/exportUncertainVector.cpp
  src/exportMatrixArchive.cpp
  src/export_kinematics_property_tree.cpp
  src/export_eigen_property_tree.cpp
  src/Logging.cpp
  src/exportNsecTime.cpp
  src/random.cpp
)

target_link_libraries(${PROJECT_NAME} 
  ${Boost_LIBRARIES} 
  sm_timing 
  sm_logging 
  sm_matrix_archive
  sm_property_tree 
  sm_kinematics
  numpy_eigen)

target_include_directories(${PROJECT_NAME} PUBLIC 
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

##################
## Installation ##
##################
install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)
