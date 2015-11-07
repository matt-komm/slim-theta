cmake_minimum_required(VERSION 2.8.3)
project(theta)

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_MODULE_PATH})

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

set(CMAKE_CXX_FLAGS "-Wno-deprecated-declarations -std=c++0x ${CMAKE_CXX_FLAGS}" )


include_directories(${Boost_INCLUDE_DIR})
message("include Boost from: " ${Boost_INCLUDE_DIR})
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
