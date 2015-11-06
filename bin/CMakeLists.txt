add_executable(theta theta.cpp)
target_link_libraries(theta libtheta)

add_executable(create-histograms create_histograms.cpp)
target_link_libraries(create-histograms libtheta ${Boost_LIBRARIES} ${SQLITE_LIBRARIES} ${ROOT_LIBRARIES})
