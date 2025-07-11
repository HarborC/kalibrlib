cmake_minimum_required(VERSION 3.10)
project(sm_property_tree)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_definitions(-fPIC)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -D__STRICT_ANSI__")

find_package(Boost REQUIRED COMPONENTS system filesystem)

include_directories(include ${Boost_INCLUDE_DIRS})

##############
## Building ##
##############

add_library(${PROJECT_NAME}
  src/PropertyTree.cpp
  src/BoostPropertyTreeImplementation.cpp
  src/BoostPropertyTree.cpp
  src/PropertyTreeImplementation.cpp
  src/BoostPropertyTreeSupport.cpp
)

target_link_libraries(${PROJECT_NAME} ${Boost_LIBRARIES} pthread sm_common)

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