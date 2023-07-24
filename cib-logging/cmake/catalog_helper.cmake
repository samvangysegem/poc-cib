function(generate_str_catalog output_lib)
    # Parse libraries for string catalog generation
    set(input_libs "${ARGN}")
    message("String catalog generation starting for the following libraries: ${input_libs}")

    foreach (lib IN LISTS input_libs)
        add_custom_command(
                OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
                DEPENDS $<TARGET_FILE:${lib}>
                COMMAND
                ${CMAKE_NM} -uC $<TARGET_FILE:${lib}> >>
                ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
                COMMENT "Extracting undefined symbols for $<TARGET_FILE:${lib}>")
    endforeach ()

    set(output_base_dir ${CMAKE_BINARY_DIR}/catalogs)
    set(output_cpp ${output_base_dir}/string_catalog.cpp)
    set(output_xml ${output_base_dir}/string_catalog.xml)
    set(output_json ${output_base_dir}/string_catalog.json)

    add_custom_command(
            OUTPUT ${output_cpp} ${output_json} ${output_xml}
            COMMAND
            ${PYTHON} ${CMAKE_SOURCE_DIR}/tools/log_parser.py
            ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt ${output_cpp}
            ${output_json} ${output_xml}
            DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/undefined_symbols.txt
            COMMENT "Generating string catalog")

    add_library(catalog STATIC ${output_cpp})
    target_link_libraries(catalog PUBLIC cib)
    target_compile_options(catalog PRIVATE -Wno-gnu-string-literal-operator-template)

    set(${output_lib} catalog PARENT_SCOPE)
endfunction()
