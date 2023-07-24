add_library(app STATIC src/application.cpp)
target_include_directories(app PUBLIC include)
target_link_libraries(app PRIVATE cib logging)
target_compile_options(app PRIVATE -Wno-gnu-string-literal-operator-template)