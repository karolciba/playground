cmake_minimum_required(VERSION 3.5)
project(cross)

set(CMAKE_CXX_STANDARD 11)

set (CMAKE_CXX_FLAGS "-lsfml-graphics -lsfml-window -lsfml-system")

add_executable(cross
        csolv.cpp
        )

target_link_libraries(cross -lsfml-graphics -lsfml-window -lsfml-system)

set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake_modules" ${CMAKE_MODULE_PATH})

#find_package(SFML 2 REQUIRED graphics window system)
#
#if(SFML_FOUND)
#    include_directories(${SFML_INCLUDE_DIR})
#    target_link_libraries(${EXECUTABLE_NAME} ${SFML_LIBRARIES} ${SFML_DEPENDENCIES})
#endif()


#add_library(csolv
#        csolv.cpp)
