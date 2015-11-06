add_library(libtheta SHARED
    asimov-utils.cpp
    atomic.cpp
    run.cpp
    toymaker.cpp
    random.cpp
    plugin.cpp
    distribution.cpp
    variables.cpp
    run_mt.cpp
    cfg-utils.cpp
    matrix.cpp
    utils.cpp
    random-utils.cpp
    phys.cpp
    model.cpp
    histogram-with-uncertainties.cpp
    histogram.cpp
    main.cpp
    producer.cpp
    log2_dot.cpp
    mcmc.cpp
    redirect_stdio.cpp
    exception.cpp
    database.cpp
    histogram-function.cpp
    minimizer.cpp
)
target_link_libraries(libtheta m dl libconfig ${Boost_LIBRARIES})

