add_project_library(poc_logging
                    INCLUDE_DIRS include
                    PRIV_REQUIRES cib
                    -Wno-gnu-string-literal-operator-template)