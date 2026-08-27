cmake_minimum_required(VERSION 3.20)

project(KORALLE-bpmn-tree-simulation)

set(CMAKE_CXX_STANDARD 20)

find_package(Curses REQUIRED)

add_executable(buildtree buildtree.cpp)

target_link_libraries(buildtree PRIVATE ${CURSES_LIBRARIES})
target_include_directories(buildtree PRIVATE ${CURSES_INCLUDE_DIR})
