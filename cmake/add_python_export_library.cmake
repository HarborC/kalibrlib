function(add_python_export_library TARGET_NAME)
  # 查找 Python 和 Boost
  find_package(PythonLibs REQUIRED)
  include_directories(${PYTHON_INCLUDE_DIRS})

  if(APPLE)
    set(BOOST_COMPONENTS system)
  else()
    set(BOOST_COMPONENTS)
  endif()

  if(PYTHONLIBS_VERSION_STRING VERSION_LESS 3)
    find_package(Boost QUIET)
    if(Boost_VERSION LESS 106700)
      list(APPEND BOOST_COMPONENTS python)
    else()
      list(APPEND BOOST_COMPONENTS python27)
    endif()
  else()
    list(APPEND BOOST_COMPONENTS python38)
  endif()

  find_package(Boost REQUIRED COMPONENTS ${BOOST_COMPONENTS})

  # 创建库目标
  add_library(${TARGET_NAME} SHARED ${ARGN})
  target_link_libraries(${TARGET_NAME}
    ${PYTHON_LIBRARY}
    ${Boost_LIBRARIES}
  )

  # 安装路径设定（根据常规路径）
  install(TARGETS ${TARGET_NAME}
    ARCHIVE DESTINATION lib
    LIBRARY DESTINATION lib
  )

  get_directory_property(AMCF ADDITIONAL_MAKE_CLEAN_FILES)
  list(APPEND AMCF ${PYTHON_LIB_DIR}/${PYLIB_OUTPUT_NAME})
  set_directory_properties(PROPERTIES ADDITIONAL_MAKE_CLEAN_FILES "${AMCF}")
endfunction()
