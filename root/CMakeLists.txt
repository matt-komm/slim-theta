add_library(root-plugin MODULE 
    root_minuit.cpp
    root_ntuple_source.cpp
    root_minuit1.cpp
    rootfile_database.cpp
    root_histogram.cpp
)

target_link_libraries(root-plugin libtheta ${Boost_LIBRARIES} ${ROOT_LIBRARIES} -lMinuit2 -lMinuit)


