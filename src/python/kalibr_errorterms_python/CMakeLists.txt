cmake_minimum_required(VERSION 3.10)
project(kalibr_errorterms_python)

add_definitions(-fPIC)

##################################
# error terms (+python export)
##################################
include_directories(include)

add_python_export_library(${PROJECT_NAME}
  src/module.cpp
)
target_link_libraries(${PROJECT_NAME}
  numpy_eigen
  aslam_backend
  aslam_backend_expressions
  kalibr_errorterms
  )