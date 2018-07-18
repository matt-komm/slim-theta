#include "interface/plugin.hpp"
#include "interface/histogram-function.hpp"
#include "plugins/histogram_add.hpp"
#include "interface/histogram-with-uncertainties.hpp"
#include "interface/redirect_stdio.hpp"

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
            int seed = 123;
            if (ctx.setting.exists("rnd"))
            {
                seed= ctx.setting["rnd"];
            }
            std::default_random_engine generator(seed);
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
    //apply zerobin_fillfactor:
    bool allowNegativeValues = true;
    if (ctx.setting.exists("allow_negative"))
    {
        allowNegativeValues = ctx.setting["allow_negative"];
    }
    double zerobin_fillfactor = 0.000000001;
    double integral = 0.0;
    for(size_t i=0; i<h.get_nbins(); ++i){
        integral += h.get_value(i);
    }
    if(ctx.setting.exists("zerobin_fillfactor"))
    {
        zerobin_fillfactor = ctx.setting["zerobin_fillfactor"];
    }
    if(zerobin_fillfactor < 0)
    {
       throw ConfigurationException("zerobin_fillfactor must be >= 0.0!");
    }
    
    
    // the minimum value to set all histogram bin to:
    const double min_absval = fabs(integral) * zerobin_fillfactor / h.get_nbins();
    for(size_t i=0; i<h.get_nbins(); ++i)
    {
        double unc = h.get_uncertainty(i);
        double val = h.get_value(i);
        // if close to 0 set to min_val; if val<0 do the same
        if((fabs(val) < min_absval) or ((not allowNegativeValues) and (val<0)))
        {
            h.set(i, min_absval, max(unc, min_absval - fabs(val)));
        }
    } 
    
    integral = 0.0;
    for(size_t i=0; i<h.get_nbins(); ++i)
    {
        integral += h.get_value(i);
    }
    //theta::out<<"-----------------------------"<< std::endl;
    //theta::out<<"histo_add: integral = "<<integral<< std::endl;
    //theta::out<<"-----------------------------"<< std::endl;
    //theta::out<< std::endl;
    
    set_histo(h);
}

REGISTER_PLUGIN(histogram_add)
