#ifndef ROOT_ROOT_HISTOGRAM_HPP
#define ROOT_ROOT_HISTOGRAM_HPP

#include "interface/histogram-function.hpp"

/** \brief Plugin to project a Histogram from a ROOT TTree
 *
 */
class root_projector: public theta::ConstantHistogramFunction{
public:
    /// Constructor used by the plugin system
    root_projector(const theta::Configuration & ctx);
};

#endif
