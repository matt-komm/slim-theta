cmake_minimum_required(VERSION 2.6)
project(theta)


set(Boost_ADDITIONAL_VERSIONS "1.52" "1.52.0")
find_package(Boost REQUIRED COMPONENTS regex program_options filesystem system thread timer iostreams)

if(NOT Boost_FOUND)
   message(SEND_ERROR "boost not found")
else()
   message("boost found at include=${Boost_INCLUDE_DIRS}; lib=${Boost_LIBRARY_DIRS}")
endif()

include_directories(${Boost_INCLUDE_DIRS})
include_directories(${CMAKE_SOURCE_DIR})

add_subdirectory(libconfig)
add_subdirectory(src)


