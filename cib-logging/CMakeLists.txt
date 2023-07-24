cmake_minimum_required(VERSION 3.27)
project(cib_logging_poc)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

file(REMOVE ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt)

# Build target
add_executable(${PROJECT_NAME} main.cpp)
target_compile_options(${PROJECT_NAME} PRIVATE -Wno-gnu-string-literal-operator-template)

include(cmake/helpers.cmake)

add_subdirectory(main)
add_subdirectory(extern)
add_subdirectory(libs/logging)

generate_log_catalog()
