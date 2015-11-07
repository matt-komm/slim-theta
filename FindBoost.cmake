set(BOOST_ROOT "" CACHE PATH "Boost install prefix")

if (BOOST_ROOT STREQUAL "")
    message(STATUS "BOOST_ROOT not set. Using system default paths to find Boost.")
    find_path(Boost_INCLUDE_DIR NAMES boost/version.hpp
    )
    foreach(Boost_COMPONENT ${Boost_FIND_COMPONENTS})
        message(STATUS "Looking for library: " ${Boost_COMPONENT})

        find_library(BOOST_LIB_${Boost_COMPONENT} NAMES ${Boost_COMPONENT} boost_${Boost_COMPONENT}   
        )
        message(STATUS ${BOOST_LIB_${Boost_COMPONENT}})
        set(Boost_LIBRARIES ${BOOST_LIB_${Boost_COMPONENT}} " " ${Boost_LIBRARIES})
    endforeach(Boost_COMPONENT)
    
    
else (BOOST_ROOT STREQUAL "")
    message(STATUS "Using BOOST_ROOT = ${BOOST_ROOT} to find Boost.")
    find_path(Boost_INCLUDE_DIR NAMES boost/version.hpp
        PATHS
        ${BOOST_ROOT}/include
        
        NO_DEFAULT_PATH
    )
    set(Boost_LIBRARIES "")
    foreach(Boost_COMPONENT ${Boost_FIND_COMPONENTS})
        message(STATUS "Looking for library: " ${Boost_COMPONENT})

        find_library(BOOST_LIB_${Boost_COMPONENT} NAMES ${Boost_COMPONENT} boost_${Boost_COMPONENT}
            PATHS
            ${BOOST_ROOT}/lib    
            
            NO_DEFAULT_PATH
        )
        message(STATUS ${BOOST_LIB_${Boost_COMPONENT}})
        set(Boost_LIBRARIES ${BOOST_LIB_${Boost_COMPONENT}} ${Boost_LIBRARIES})
    endforeach(Boost_COMPONENT)

endif (BOOST_ROOT STREQUAL "")


include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Boost DEFAULT_MSG Boost_INCLUDE_DIR Boost_LIBRARIES)

mark_as_advanced(Boost_INCLUDE_DIR Boost_LIBRARIES)

