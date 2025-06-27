cmake_minimum_required(VERSION 3.10)
project(incremental_calibration_python)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)

add_python_export_library(${PROJECT_NAME}
  src/module.cpp
  src/OptimizationProblem.cpp
  src/IncrementalEstimator.cpp
  src/LinearSolver.cpp
)

target_link_libraries(${PROJECT_NAME} 
  aslam_backend 
  incremental_calibration 
  sm_property_tree
  numpy_eigen
)