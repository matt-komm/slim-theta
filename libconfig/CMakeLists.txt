include_directories(${CMAKE_CURRENT_SOURCE_DIR})

add_library(libconfig SHARED 
    grammar.c  
    libconfig.c  
    libconfigcpp.cpp  
    scanctx.c  
    scanner.c  
    strbuf.c
)


