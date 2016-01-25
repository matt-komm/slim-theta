#include "interface/plugin.hpp"
#include "interface/histogram-function.hpp"
#include "root/root_projector.hpp"
#include "interface/redirect_stdio.hpp"


#include "TH1D.h"
#include "TRandom.h"
#include "TFile.h"
#include "TTree.h"
#include "TCanvas.h"

using namespace theta;
using namespace std;

root_projector::root_projector(const Configuration & ctx){
    string filename = utils::replace_theta_dir(ctx.setting["filename"]);
    string treeName = ctx.setting["tree"];
    string varStr = ctx.setting["variable"];
    string weightStr = ctx.setting["weight"];
    
    
    
    double range_low = ctx.setting["range"][0];
    double range_high = ctx.setting["range"][1];
    int nbins = ctx.setting["nbins"];
    
    
    if(range_low >= range_high) {
        stringstream s;
        s << "invalid range given:  ["<< range_low <<"," << range_high <<"]" ;
        throw ConfigurationException(s.str());
    }
    if(nbins <= 0) {
        stringstream s;
        s << "invalid nbins given:  "<< nbins;
        throw ConfigurationException(s.str());
    }
    
    bool use_errors = false;
    if(ctx.setting.exists("use_errors")){
         use_errors = ctx.setting["use_errors"];
    }
    stringstream histNameStream;
    histNameStream << treeName << int(gRandom->Uniform(0,10000000));
    

    TFile file(filename.c_str(), "r");
    TH1D* hist = new TH1D(histNameStream.str().c_str(),"",nbins,range_low,range_high);
    if(file.IsZombie()){
        stringstream s;
        s << "Could not open file '" << filename << "'";
       throw ConfigurationException(s.str());
    }
    
    
    
    TTree* tree = dynamic_cast<TTree*>(file.Get(treeName.c_str()));
    if (!tree)
    {
        stringstream s;
        s << "Could find TTree '"<<treeName<<"' in file '" << filename << "'";
       throw ConfigurationException(s.str());
    }
    
    if (ctx.setting.exists("friends"))
    {

        for (unsigned int i= 0; i< ctx.setting["friends"].size();++i)
        {
            string friendname = utils::replace_theta_dir(ctx.setting["friends"][i]);
            tree->AddFriend(treeName.c_str(),friendname.c_str());
        }
    }
    theta::out<<"projecting ... "<<filename.c_str();
    tree->Project(hist->GetName(),varStr.c_str(),weightStr.c_str());
    theta::out<<" = "<<hist->GetEntries()<<" events, integral = "<<hist->Integral() << std::endl;
    if (ctx.setting.exists("print"))
    {
        TCanvas cv(("cv_"+histNameStream.str()).c_str(),"",800,600);
        hist->Draw();
        std::string printName = ctx.setting["print"];
        cv.Print(printName.c_str());
    }
    
    if (ctx.setting.exists("scale"))
    {
        double scale = ctx.setting["scale"];
        hist->Scale(scale);
    }

    if(ctx.setting.exists("normalize_to")){
       double norm = ctx.setting["normalize_to"];
       double hist_integral = hist->Integral();
       if(hist_integral==0){
           if(norm!=0){
               throw ConfigurationException("specified non-zero 'normalize_to' setting but original Histogram's integral is zero");
           }
       }
       else{
           hist->Scale(norm / hist_integral);
       }
    }


    // bin_low and bin_high refer to the ROOT binning convention
    int bin_low = 1;
    int bin_high = hist->GetNbinsX();
    double xmin = hist->GetXaxis()->GetXmin();
    double xmax = hist->GetXaxis()->GetXmax();
    bin_low = hist->GetXaxis()->FindBin(range_low);
    if(bin_low==0) 
    {
        xmin = hist->GetXaxis()->GetXmin() - hist->GetXaxis()->GetBinWidth(1);
    }
    else 
    {
        xmin = hist->GetXaxis()->GetBinLowEdge(bin_low);
    }
    if(bin_low > 0 && range_low!=hist->GetXaxis()->GetBinLowEdge(bin_low))
    {
        throw ConfigurationException("'range' setting incompatible with bin borders.");
    }


    if(range_high > hist->GetXaxis()->GetXmax())
    {
        bin_high = hist->GetNbinsX()+1;
        xmax = hist->GetXaxis()->GetXmax() + hist->GetXaxis()->GetBinWidth(hist->GetNbinsX());
    }
    else
    {
        bin_high = hist->GetXaxis()->FindBin(range_high);
        --bin_high;
        xmax = hist->GetXaxis()->GetBinUpEdge(bin_high);
        if(range_high!=hist->GetXaxis()->GetBinUpEdge(bin_high))
        {
            throw ConfigurationException("'range' setting incompatible with bin borders.");
        }
    }
    
    int n = bin_high - bin_low + 1;
    Histogram1DWithUncertainties h = Histogram1DWithUncertainties(n, xmin, xmax);
    for(int i = bin_low; i <= bin_high; i++)
    {
        double content = hist->GetBinContent(i);
        double unc = use_errors ? hist->GetBinError(i) : 0.0;
        h.set(i - bin_low, content, unc);
    }
    
    
    
    //apply zerobin_fillfactor:
    double zerobin_fillfactor = 0.0;
    if(ctx.setting.exists("zerobin_fillfactor")){
        zerobin_fillfactor = ctx.setting["zerobin_fillfactor"];
        if(zerobin_fillfactor < 0){
           throw ConfigurationException("zerobin_fillfactor must be >= 0.0!");
        }
        double integral = 0.0;
        for(size_t i=0; i<h.get_nbins(); ++i){
            integral += h.get_value(i);
        }
        // the minimum value to set all histogram bin to:
        const double min_val = integral * zerobin_fillfactor / h.get_nbins();
        for(size_t i=0; i<h.get_nbins(); ++i){
            double unc = h.get_uncertainty(i);
            double val = h.get_value(i);
            // set uncertainty to (at least) the difference of new and old value, if we have fill the histogram
            if(val < min_val){
                unc = max(unc, min_val - val);
                val = min_val;
            }
            h.set(i, val, unc);
        }
    }
    set_histo(h);
}

REGISTER_PLUGIN(root_projector)
