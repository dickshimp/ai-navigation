# Install script for directory: /home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/weilannw/Autonomous-Navigation/planning_navigation/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/navigation/../../navigation_msgs/msg" TYPE FILE FILES
    "/home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation/../../navigation_msgs/msg//fe_request.msg"
    "/home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation/../../navigation_msgs/msg//lat_long_point.msg"
    "/home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation/../../navigation_msgs/msg//list_of_goals.msg"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/navigation" TYPE FILE FILES "/home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation/package.xml")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/weilannw/Autonomous-Navigation/planning_navigation/build/navigation/navigation/catkin_generated/installspace/navigation.pc")
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/navigation/cmake" TYPE FILE FILES
    "/home/weilannw/Autonomous-Navigation/planning_navigation/build/navigation/navigation/catkin_generated/installspace/navigationConfig.cmake"
    "/home/weilannw/Autonomous-Navigation/planning_navigation/build/navigation/navigation/catkin_generated/installspace/navigationConfig-version.cmake"
    )
endif()

if(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/navigation" TYPE FILE FILES "/home/weilannw/Autonomous-Navigation/planning_navigation/src/navigation/navigation/package.xml")
endif()

