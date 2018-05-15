#include "plugins/minimizer_chain.hpp"
#include "interface/plugin.hpp"
#include "interface/phys.hpp"
#include "interface/redirect_stdio.hpp"

using namespace theta;
using namespace std;

MinimizationResult minimizer_chain::minimize(const Function & f, const ParValues & start,
                const ParValues & step, const Ranges & ranges){
    MinimizationResult res;
    bool success = false;
    for(size_t i=0; i < minimizers.size(); ++i){
        try{
            out<<"Trying minimizer: "<<(i+1);
            res = minimizers[i].minimize(f, start, step, ranges);
            success = true;
            out<<" success!"<<std::endl;
        }
        catch(MinimizationException & ex){
            out<<" FAILED! (MinimizationException: "<<ex.what()<<")"<<std::endl;
            // if this was the last attempt: re-throw, otherwise silently ignore and try the next minimizer ...
            if(i+1==minimizers.size()) throw;
        }
        catch(std::logic_error & ex){
            out<<" FAILED! (LogicError: "<<ex.what()<<")"<<std::endl;
            if(i+1==minimizers.size()) throw;
        }
        if(success) break;
    }
    if(last_minimizer.get()){
        ParValues step2 = step;
        // set step2 to the errors from the minimization, if available:
        const ParIds & pids = f.get_parameters();
        for(ParIds::const_iterator it=pids.begin(); it!=pids.end(); ++it){
            if(res.errors_plus.contains(*it)){
                double width = res.errors_plus.get(*it);
                if(width > 0){
                    step2.set(*it, width);
                }
            }
        }
        try{
            out<<"Running last minimizer: ";
            res = last_minimizer->minimize(f, res.values, step2, ranges);
            out<<" success!"<<std::endl;
        }
        catch(MinimizationException & ex){
            out<<" FAILED! (MinimizationException: "<<ex.what()<<")"<<std::endl;
            throw;
        }
        catch(std::logic_error & ex){
            out<<" FAILED! (LogicError: "<<ex.what()<<")"<<std::endl;
            throw;
        }
    }
    return res;
}


minimizer_chain::minimizer_chain(const theta::Configuration & cfg){
    Setting s = cfg.setting;
    const size_t n = s["minimizers"].size();
    minimizers.reserve(n);
    size_t n_minimizers = 0;
    for(size_t i=0; i<n; ++i){
        minimizers.push_back(PluginManager<Minimizer>::build(Configuration(cfg, s["minimizers"][i])));
        ++n_minimizers;
    }
    if(s.exists("last_minimizer")){
        last_minimizer = PluginManager<Minimizer>::build(Configuration(cfg, s["last_minimizer"]));
        ++n_minimizers;
    }
    if(n_minimizers==0) throw ConfigurationException("no minimizers specified; required is at least one (counting last_minimizer)");
}

REGISTER_PLUGIN(minimizer_chain)

