cmake_minimum_required(VERSION 3.27)
project(cib_logging_poc)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

file(REMOVE ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt)

# Include helpers
include(cmake/constants.cmake)
include(cmake/catalog_helper.cmake)

# Add library directories
add_subdirectory(main)
add_subdirectory(libs/logging)
add_subdirectory(extern)

# Build target
add_executable(${PROJECT_NAME} main.cpp)
target_compile_options(${PROJECT_NAME} PRIVATE -Wno-gnu-string-literal-operator-template)

# Generate log catalog
generate_str_catalog(log_catalog app)
target_link_libraries(${PROJECT_NAME} PUBLIC ${log_catalog})

# Link remaining libraries
target_link_libraries(${PROJECT_NAME} PUBLIC app cib)
