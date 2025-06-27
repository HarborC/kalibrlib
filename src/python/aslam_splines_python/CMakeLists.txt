cmake_minimum_required(VERSION 3.10)
project(aslam_splines_python)

add_definitions(-fPIC)

add_python_export_library(${PROJECT_NAME}
  src/spline_module.cpp
  src/BSplineMotionError.cpp
  src/SimpleSplineError.cpp
)
target_link_libraries(${PROJECT_NAME} 
  aslam_splines
  bsplines_python
  bsplines
  numpy_eigen
  sparse_block_matrix
  sm_common
  sm_kinematics
  aslam_backend_expressions
  aslam_backend
  aslam_backend_python
  sm_timing
  aslam_cameras
  aslam_time
  sm_opencv
  sm_property_tree
  sm_logging)
