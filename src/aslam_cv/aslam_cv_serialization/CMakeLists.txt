cmake_minimum_required(VERSION 3.10)
project(aslam_cv_serialization)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)

# 查找依赖项
find_package(Boost REQUIRED COMPONENTS system serialization)

INCLUDE(autogen_cameras.cmake)

include_directories(include ${Boost_INCLUDE_DIRS})

##############
## Building ##
##############


add_library(${PROJECT_NAME}
  ${AUTOGEN_CAMERA_CPP_FILES}
  src/FrameBaseSerialization.cpp
)

target_link_libraries(${PROJECT_NAME}
  ${Boost_LIBRARIES}
  aslam_cameras
  aslam_time
  sm_common
  sm_boost
  sm_property_tree
  sm_eigen
  sm_kinematics
  sm_opencv
  sm_logging
  sm_random
)

target_include_directories(${PROJECT_NAME} PUBLIC 
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

####################
## Installation ##
####################

install(TARGETS ${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(DIRECTORY include/
  DESTINATION include/${PROJECT_NAME}
)

install(TARGETS ${PROJECT_NAME}
        EXPORT ${PROJECT_NAME}-targets
        ARCHIVE DESTINATION lib
        LIBRARY DESTINATION lib
        RUNTIME DESTINATION bin
        )

install(EXPORT ${PROJECT_NAME}-targets
        FILE ${PROJECT_NAME}-config.cmake
        DESTINATION share/cmake/${PROJECT_NAME}/
     )
