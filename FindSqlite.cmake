set(SQLITE_ROOT "" CACHE PATH "Sqlite install prefix")

if (SQLITE_ROOT STREQUAL "")
    find_package(PkgConfig)
    pkg_check_modules(PKG_SQLITE sqlite3)

    if (PKG_SQLITE_FOUND)
        message(STATUS "SQLITE_ROOT not set. Trying PkgConfig ...")
        find_path(Sqlite_INCLUDE_DIR NAMES sqlite3.h
            PATHS
            ${PKG_SQLITE_INCLUDEDIR}
            ${PKG_SQLITE_INCLUDE_DIRS}
            
            NO_DEFAULT_PATH
        )
        find_library(SQLITE_LIB NAMES sqlite3
            PATHS
            ${PKG_SQLITE_LIBDIR}
            ${PC_SQLITE_LIBRARY_DIRS}
            
            NO_DEFAULT_PATH
        )
        
    else (PKG_SQLITE_FOUND)
        message(STATUS "SQLITE_ROOT not set. Trying system paths ...")
        find_path(Sqlite_INCLUDE_DIR NAMES sqlite3.h
        )
        find_library(SQLITE_LIB NAMES sqlite3
        )
    
    endif (PKG_SQLITE_FOUND)
    
    
    set(Sqlite_LIBRARIES ${SQLITE_LIB})
    
    
else (SQLITE_ROOT STREQUAL "")
    message(STATUS "Using SQLITE_ROOT = ${SQLITE_ROOT} to find Sqlite.")
    find_path(Sqlite_INCLUDE_DIR NAMES sqlite3.h
        PATHS
        ${SQLITE_ROOT}/include
        
        NO_DEFAULT_PATH
    )
    
        
    find_library(SQLITE_LIB NAMES sqlite3
        PATHS
        ${SQLITE_ROOT}/lib
        
        NO_DEFAULT_PATH
    )
    
    set(Sqlite_LIBRARIES ${SQLITE_LIB})

endif (SQLITE_ROOT STREQUAL "")


include(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(Sqlite DEFAULT_MSG Sqlite_INCLUDE_DIR Sqlite_LIBRARIES)

mark_as_advanced(Sqlite_INCLUDE_DIR Sqlite_LIBRARIES)
