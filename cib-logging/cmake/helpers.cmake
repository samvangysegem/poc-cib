# Add library and link to project target
# Not entirely sure whether this is the best approach regarding readability... 
# Use of this template in larger projects will reveal any usability issues rather quickly
# at which point I will update this project as well to reflect any improvements.
function(add_project_library target)
   set(options)
   set(single_value)
   set(multi_value SRCS
                   INCLUDE_DIRS PRIV_INCLUDE_DIRS 
                   REQUIRES PRIV_REQUIRES)

   cmake_parse_arguments(_ "${options}" "${single_value}" "${multi_value}" ${ARGN})

   # Update paths
   foreach(SRC IN LISTS __SRCS)
      list(APPEND sources ${CMAKE_CURRENT_LIST_DIR}/${SRC})
   endforeach()

   foreach(DIR IN LISTS __INCLUDE_DIRS)
      list(APPEND includes ${CMAKE_CURRENT_LIST_DIR}/${DIR})
   endforeach()

   foreach(DIR IN LISTS __PRIV_INCLUDE_DIRS)
      list(APPEND priv_includes ${CMAKE_CURRENT_LIST_DIR}/${DIR})
   endforeach()
   
   # Add library target
   if(sources)
      add_library(${target} OBJECT ${sources})
      target_include_directories(${target} PUBLIC ${includes})
      target_include_directories(${target} PRIVATE ${priv_includes})

      target_link_libraries(${target} PUBLIC ${__REQUIRES})
      target_link_libraries(${target} PRIVATE ${__PRIV_REQUIRES})

      # Catalog generation lists
      set_property(GLOBAL APPEND PROPERTY GLOBAL_TARGET_LOG_LIBS ${target})
      set_property(GLOBAL APPEND PROPERTY GLOBAL_TARGET_LOG_OBJS $<TARGET_OBJECTS:${target}>)
   else()
      add_library(${target} INTERFACE)
      target_include_directories(${target} INTERFACE ${includes})
      
      if(priv_includes)
         message(WARNING "PRIV_INCLUDE_DIRS is ignored for INTERFACE libraries!")
      endif()

      target_link_libraries(${target} INTERFACE ${__REQUIRES})
      target_link_libraries(${target} INTERFACE ${__PRIV_REQUIRES})
   endif()
   
   target_compile_options(${target} PRIVATE ${__ARGN})

   # Link library to project target
   target_link_libraries(${PROJECT_NAME} PUBLIC ${target})

endfunction()

# Generate catalog of log messages
function(generate_log_catalog)
   set(CPP_OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/logging/logs_catalog.cpp)
   set(JSON_OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/logging/logs_catalog.json)
   set(XML_OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/logging/logs_catalog.xml)
   set(GEN_STR_CATALOG_SCRIPT ${CMAKE_CURRENT_SOURCE_DIR}/tools/log_parser.py)

   get_property(TARGET_LIBS GLOBAL PROPERTY GLOBAL_TARGET_LOG_LIBS)
   get_property(TARGET_OBJS GLOBAL PROPERTY GLOBAL_TARGET_LOG_OBJS)

   add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
                     DEPENDS
                           ${TARGET_LIBS}
                     COMMAND 
                           ${CMAKE_NM} -uC ${TARGET_OBJS} >> 
                           ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
                     COMMENT "Running undefined symbols extraction...")

   add_custom_command(OUTPUT 
                           ${CPP_OUTPUT_FILE}
                           ${JSON_OUTPUT_FILE} 
                           ${XML_OUTPUT_FILE} 
                     DEPENDS
                           ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
                     COMMAND
                           python3 ${GEN_STR_CATALOG_SCRIPT}
                           ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt 
                           ${CPP_OUTPUT_FILE} ${JSON_OUTPUT_FILE} ${XML_OUTPUT_FILE}
                     COMMENT "Starting string catalog generation...")

   add_library(string_catalog STATIC ${CPP_OUTPUT_FILE})
   target_link_libraries(string_catalog PUBLIC cib)
   target_compile_options(string_catalog PRIVATE -Wno-gnu-string-literal-operator-template)
   
   target_link_libraries(${PROJECT_NAME} PUBLIC string_catalog)
endfunction()
