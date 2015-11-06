cmake_minimum_required(VERSION 2.8.3)
project(theta)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_MODULE_PATH})

set(BOOST_ROOT "" CACHE PATH "Boost install prefix")
if (NOT BOOST_ROOT STREQUAL "")
    message(STATUS "boost will be taken from BOOST_ROOT=" ${BOOST_ROOT})
    set(Boost_NO_SYSTEM_PATHS ON)
else(NOT BOOST_ROOT STREQUAL "")
    message(STATUS "auto detecting boost. Set '-DBOOST_ROOT=' to override!")
endif(NOT BOOST_ROOT STREQUAL "")

find_package(Boost 
    REQUIRED 
    COMPONENTS regex program_options filesystem system thread timer iostreams
)

find_package(Sqlite
    REQUIRED 
)

find_package(ROOT 
    REQUIRED 
)

include_directories(${Boost_INCLUDE_DIRS})
message("include Boost from: " ${Boost_INCLUDE_DIRS})
message("link Boost: " ${Boost_LIBRARIES})
include_directories(${ROOT_INCLUDE_DIR})
message("include Root from: " ${ROOT_INCLUDE_DIR})
message("link Root: " ${ROOT_LIBRARIES})
include_directories(${SQLITE_INCLUDE_DIR})
message("include Sqlite from: " ${SQLITE_INCLUDE_DIR})
message("link Sqlite: " ${SQLITE_LIBRARIES})

include_directories(${CMAKE_SOURCE_DIR})


add_subdirectory(libconfig)
add_subdirectory(src)
add_subdirectory(bin)
add_subdirectory(plugins)
