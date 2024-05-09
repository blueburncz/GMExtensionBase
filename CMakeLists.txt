cmake_minimum_required(VERSION 3.23)

project(GMExtensionBase)

set(CMAKE_CXX_STANDARD 17)

set(SOURCES
    src/dllmain.cpp
    )

add_library(${PROJECT_NAME} SHARED ${SOURCES})

if(WIN32)
    add_definitions(-DOS_Windows)
endif()

target_include_directories(${PROJECT_NAME} PRIVATE include/)

add_custom_command(
    TARGET ${PROJECT_NAME} POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        $<TARGET_FILE:${PROJECT_NAME}>
        "${CMAKE_CURRENT_SOURCE_DIR}/extensions/${PROJECT_NAME}"
        )
