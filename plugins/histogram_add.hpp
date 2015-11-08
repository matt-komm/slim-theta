#ifndef ROOT_HISTOGRAM_ADD_HPP
#define ROOT_HISTOGRAM_ADD_HPP

#include "interface/histogram-function.hpp"

/** \brief Plugin to read Histogram from a root file
 *
 * Configuration: anywhere, where a (constant) Histogram has to be defined,
 * use a setting like:
 * \code
 * 
 * \endcode
 *
 */
class histogram_add: public theta::ConstantHistogramFunction{
public:
    /// Constructor used by the plugin system
    histogram_add(const theta::Configuration & ctx);
};

#endif
