add_project_library(app_lib 
                    SRCS src/application.cpp
                    INCLUDE_DIRS include
                    PRIV_REQUIRES cib poc_logging
                    -Wno-gnu-string-literal-operator-template)