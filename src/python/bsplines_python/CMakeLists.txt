cmake_minimum_required(VERSION 3.10)
project(bsplines_python)

add_definitions(-fPIC)

add_python_export_library(${PROJECT_NAME}
  src/SplinePython.cpp
  src/BSplinePython.cpp
  src/BSplinePosePython.cpp
)

target_link_libraries(${PROJECT_NAME} 
  bsplines
  numpy_eigen
  sparse_block_matrix
  sm_common
  sm_kinematics
)