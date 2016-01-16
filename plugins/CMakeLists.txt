add_library(plugins MODULE
    add.cpp
    add_sources.cpp
    asymptotic_cls.cpp
    blackhole_database.cpp
    cls_limits.cpp
    constrain_ratio.cpp
    convert_database.cpp
    core.cpp
    cubiclinear_histomorph.cpp
    deltanll_hypotest.cpp
    deltanll_intervals.cpp
    direct_data_histo.cpp
    equidistant_deltas.cpp
    exp_function.cpp
    exponential_hf.cpp
    gamma_distribution.cpp
    histogram_add.cpp
    histo_source.cpp
    igauss.cpp
    interpolating-histogram.cpp
    linear-histo-morph.cpp
    mcmc_chain.cpp
    mcmc_mean_prediction.cpp
    mcmc_minimizer.cpp
    mcmc_posterior_histo.cpp
    mcmc_posterior_ratio.cpp
    mcmc_quantiles.cpp
    mcmc-strategies.cpp
    minimizer_chain.cpp
    mle.cpp
    multiplexing_database.cpp
    multiply.cpp
    newton.cpp
    newton-utils.cpp
    neyman_belt.cpp
    nl_gauss.cpp
    nll_der.cpp
    nll_scan.cpp
    nl_one_over_sqrt.cpp
    pseudodata_writer.cpp
    replay_toys.cpp
    simple_linear_histomorph.cpp
    sqlite_database.cpp
    sqlite_database_in.cpp
    sys_rate_function.cpp
    textout_database.cpp
    vary_one.cpp
)

target_link_libraries(plugins libtheta ${Sqlite_LIBRARIES} ${Boost_LIBRARIES})

install(
    TARGETS plugins
    RUNTIME DESTINATION bin
    LIBRARY DESTINATION lib
)
