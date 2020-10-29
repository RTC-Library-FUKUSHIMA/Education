if(NOT ENABLE_GUI)
  return()
endif()

option(BUILD_TURTLEBOT2 "Building the TURTLEBOT2 files" ON)
if(NOT BUILD_TURTLEBOT2)
  return()
endif()

add_subdirectory(controller)

if(UNIX)
  add_custom_target(
    symlink_to_TurtleBot ALL
    COMMAND ${CMAKE_COMMAND} -E create_symlink
    ${CMAKE_CURRENT_SOURCE_DIR} ${CNOID_BINARY_SHARE_DIR}/TurtleBot2)
endif()

install(DIRECTORY
  model
  project
  DESTINATION ${CNOID_SHARE_SUBDIR}/TurtleBot2)

