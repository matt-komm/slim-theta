#include "interface/plugin.hpp"
#include "interface/histogram-function.hpp"
#include "plugins/histogram_add.hpp"
#include "interface/histogram-with-uncertainties.hpp"

#include <random>

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
    if (ctx.setting.exists("dice_stat"))
    {
        bool dicing = ctx.setting["dice_stat"];
        if (dicing)
        {
            std::default_random_engine generator;
            for (int ibin = 0; ibin< h.get_nbins(); ++ibin)
            {
                if (h.get(ibin)>0)
                {
                    std::poisson_distribution<int> distribution(h.get(ibin));
                    int diced = distribution(generator);
                    h.set(ibin,
                        diced,
                        std::sqrt(diced)
                    );
                }
            }
        }
    }
    
    set_histo(h);
}

REGISTER_PLUGIN(histogram_add)
