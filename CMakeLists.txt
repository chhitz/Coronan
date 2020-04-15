cmake_minimum_required(VERSION 3.10)

project(
    Coronan
    VERSION 0.1
    DESCRIPTION "Conan example project showing Covid-19 cases."
    LANGUAGES CXX
)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Debug)
endif()

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake")
include(clang)

include(conan)

conan_cmake_run(REQUIRES doctest/2.3.7
                         poco/1.10.1
                         rapidjson/1.1.0
                         lyra/1.3.0
                         openssl/1.0.2t  # resolve conflict between poco and qt
                         qt/5.12.7@bincrafters/stable
                         Qt5Charts/5.12.7
                OPTIONS *:shared=True
                NO_LOAD 1 
                BUILD missing
                GENERATORS cmake_find_package cmake_paths)

include(${CMAKE_BINARY_DIR}/conan_paths.cmake)

if(CMAKE_PROJECT_NAME STREQUAL PROJECT_NAME)

    set_property(GLOBAL PROPERTY USE_FOLDERS ON)

    include(CTest)

    find_package(Doxygen)
    if(Doxygen_FOUND)
        add_subdirectory(docs)
    else()
        message(STATUS "Doxygen not found. Docu is not built")
    endif()
endif()

add_subdirectory(src)
add_subdirectory(tests)
add_subdirectory(apps/cli)
add_subdirectory(apps/qt)
