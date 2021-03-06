cmake_minimum_required(VERSION 3.10..3.16)

project(
    coronan_lib
    VERSION 0.1
    LANGUAGES CXX
)

find_package(Poco REQUIRED Net)
find_package(RapidJSON REQUIRED)

set(HEADER_LIST
    "${CMAKE_CURRENT_SOURCE_DIR}/../include/coronan/http_client.hpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/../include/coronan/corona-api_parser.hpp"
    "${CMAKE_CURRENT_SOURCE_DIR}/../include/coronan/ssl_initializer.hpp"
)

add_library(${PROJECT_NAME} STATIC ${HEADER_LIST})

add_library(coronan::lib ALIAS ${PROJECT_NAME})

target_include_directories(
    ${PROJECT_NAME} PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/../include
)

target_sources(
    ${PROJECT_NAME}
    PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/corona-api_parser.cpp
            ${CMAKE_CURRENT_SOURCE_DIR}/ssl_initializer.cpp ${HEADER_LIST}
)

target_link_libraries(
    ${PROJECT_NAME}
    PUBLIC Poco::Poco
    PUBLIC RapidJSON::RapidJSON
)

# IDE stuff
source_group(
    TREE "${CMAKE_CURRENT_SOURCE_DIR}/../include"
    PREFIX "Header Files"
    FILES ${HEADER_LIST}
)

target_compile_options(
    ${PROJECT_NAME}
    PRIVATE -Wall
            -Werror
            -Wextra
            -pedantic
            -Wcast-align
            -Wconversion
            -Wunused
            -Wpointer-arith
            -Wcast-qual
            -Wcast-qual
            -Wctor-dtor-privacy
            -Wdisabled-optimization
            -Wformat=2
            -Winit-self
            -Wmissing-declarations
            -Wmissing-include-dirs
            -Wold-style-cast
            -Woverloaded-virtual
            -Wredundant-decls
            -Wshadow
            -Wsign-conversion
            -Wsign-promo
            -Wstrict-overflow=5
            -Wswitch-default
            -Wundef
            $<$<CONFIG:Release>:-O3>
)

if(CMAKE_COMPILER_IS_GNUCXX)
    target_compile_options(
        ${PROJECT_NAME} PRIVATE -Wlogical-op -Wnoexcept -Wstrict-null-sentinel
                                -fconcepts
    )
elseif(CMAKE_COMPILER_IS_CLANGCXX)
    target_compile_options(${PROJECT_NAME} 
        PRIVATE 
            -Wno-gnu-zero-variadic-macro-arguments 
    )
endif(CMAKE_COMPILER_IS_GNUCXX)

target_compile_options(
    ${PROJECT_NAME} PUBLIC $<$<BOOL:MSVC>:-D_WIN32_WINNT=0x0601>
                           $<$<BOOL:UNIX>:-fPIC;>
)

if(CODE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
# Include code-coverage settings:
    target_link_libraries(${PROJECT_NAME} PUBLIC code_coverage::config)
endif()

if(CLANG_TIDY_EXE AND NOT CMAKE_COMPILER_IS_GNUCXX)
    set_target_properties(
        ${PROJECT_NAME} PROPERTIES CXX_CLANG_TIDY "${CLANG_TIDY_PROPERTIES}"
    )
endif()

set_target_properties(${PROJECT_NAME} PROPERTIES
    CXX_STANDARD 17
    CXX_EXTENSIONS OFF
)
