cmake_minimum_required(VERSION 3.10)
project(sm_eigen)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)

find_package(Boost REQUIRED COMPONENTS system serialization)
find_package(Eigen3 REQUIRED)

include_directories(include ${EIGEN3_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})

##############
## Building ##
##############

add_library(${PROJECT_NAME}  
  src/random.cpp
)

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES} sm_random)

target_include_directories(${PROJECT_NAME} PUBLIC 
  $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

##################
## Installation ##
##################

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