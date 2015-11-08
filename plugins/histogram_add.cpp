#include "interface/plugin.hpp"
#include "interface/histogram-function.hpp"
#include "plugins/histogram_add.hpp"
#include "interface/histogram-with-uncertainties.hpp"

using namespace theta;
using namespace std;

histogram_add::histogram_add(const Configuration & ctx){
    Histogram1DWithUncertainties h;
    ParValues pv;
    size_t nbins;
    double xmin, xmax;
    for (unsigned int ihist = 0; ihist<ctx.setting["histoList"].size(); ++ihist)
    {
        Configuration histConf = Configuration(ctx,ctx.setting["histoList"][ihist]);
        std::auto_ptr<HistogramFunction> subHist = PluginManager<HistogramFunction>::build(histConf);
        if (ihist==0)
        {
            
            subHist->get_histogram_dimensions(nbins, xmin, xmax);
            h = Histogram1DWithUncertainties(nbins, xmin, xmax);
        }
        subHist->add_with_coeff_to(h,1.0,pv);
    }
    set_histo(h);
}

REGISTER_PLUGIN(histogram_add)
