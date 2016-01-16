add_executable(theta theta.cpp)
target_link_libraries(theta libtheta)

install(
    TARGETS theta
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
)
