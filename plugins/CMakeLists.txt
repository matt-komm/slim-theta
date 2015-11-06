add_library(plugins MODULE
    constrain_ratio.cpp
    mcmc_minimizer.cpp
    multiply.cpp
    histo_source.cpp
    newton-utils.cpp
    mcmc_chain.cpp
    deltanll_hypotest.cpp
    replay_toys.cpp
    nll_der.cpp
    igauss.cpp
    core.cpp
    mcmc_quantiles.cpp
    pseudodata_writer.cpp
    cls_limits.cpp
    blackhole_database.cpp
    mcmc_posterior_histo.cpp
    mcmc_mean_prediction.cpp
    mle.cpp
    textout_database.cpp
    newton.cpp
    exp_function.cpp
    add.cpp
    convert_database.cpp
    equidistant_deltas.cpp
    vary_one.cpp
    interpolating-histogram.cpp
    exponential_hf.cpp
    asymptotic_cls.cpp
    cubiclinear_histomorph.cpp
    nl_gauss.cpp
    minimizer_chain.cpp
    gamma_distribution.cpp
    neyman_belt.cpp
    deltanll_intervals.cpp
    sqlite_database_in.cpp
    mcmc-strategies.cpp
    mcmc_posterior_ratio.cpp
    add_sources.cpp
    nl_one_over_sqrt.cpp
    multiplexing_database.cpp
    sys_rate_function.cpp
    simple_linear_histomorph.cpp
    sqlite_database.cpp
    direct_data_histo.cpp
    nll_scan.cpp
    linear-histo-morph.cpp
)

target_link_libraries(plugins libtheta ${SQLITE_LIBRARIES} ${Boost_LIBRARIES})


