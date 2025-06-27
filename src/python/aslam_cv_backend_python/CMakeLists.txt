cmake_minimum_required(VERSION 3.10)
project(aslam_cv_backend_python)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)

include_directories(include)

add_python_export_library(${PROJECT_NAME}
  src/module.cpp  
  src/GridCalibration.cpp
  # src/CameraGeometryDesignVariableContainer.cpp
#  src/NCameraSystemDesignVariableContainer.cpp
)

target_link_libraries(${PROJECT_NAME} 
  sm_common
  sm_python
  sm_opencv
  numpy_eigen
  sparse_block_matrix
  aslam_backend
  aslam_backend_expressions
  aslam_backend_python
  aslam_cameras
  aslam_cv_error_terms
  aslam_splines
  aslam_cv_python
  aslam_cv_backend
  aslam_time)

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

