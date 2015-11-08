add_library(root-plugin MODULE 
    rootfile_database.cpp
    root_histogram.cpp
    root_minuit1.cpp
    root_minuit.cpp
    root_ntuple_source.cpp
    root_projector.cpp
)

target_link_libraries(root-plugin libtheta ${Boost_LIBRARIES} ${ROOT_LIBRARIES} -lMinuit2 -lMinuit)


