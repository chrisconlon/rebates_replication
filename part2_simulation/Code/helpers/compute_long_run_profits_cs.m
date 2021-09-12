
%This long run profits calculation function computes the long run profits
%at the ergodic distribution of consumer arrivials. It takes in five
%parameters and returns results on long run profits and relevant optimal
%effort policies. The three input parameters are a matrix of payoffs,
%a stationary vector of incremental sales, the level of fixed costs, the
%elasticity level, and a boolean for a marginal cost of zero. 
function [longrun_profits,policies]=compute_long_run_profits_cs(payoffs,xx,fcvec,elas,mc)
	% this is the calibration for the consumer surplus
	alpha=2.7070/2 * abs(elas);
    % for mc=0
    if mc == 0
        rebsize = 0.16;
    % for mc=15
    elseif mc == 0.15
        rebsize = .222;
    else
        error("Marginal Cost not Properly Specified")
    end
    
    %Obtain the retailer weighted payoffs with rebates using mars bars
	retailerrebate= payoffs.retail+payoffs.mars.*rebsize;
    %Solve dynamic programming problems using retail payoffs, retail payoffs
    %with rebates, retail with payoff with mars, retail pay with the sum
    %of all brands sold, payoffs with mars bars and payoffs with nestle bars 
tic
	[resRReb]=solveDP(xx,retailerrebate,fcvec);
	[resNReb]=solveDP(xx,payoffs.retail,fcvec);
	[resInt]=solveDP(xx,payoffs.retail+payoffs.mars,fcvec);
	[resIndustry]=solveDP(xx,payoffs.retail+payoffs.mars+payoffs.nestle+payoffs.hershey,fcvec);
	[resMars]=solveDP(xx,payoffs.mars,0);
	[resNestle]=solveDP(xx,payoffs.nestle,0);

	% Hershey (without FC)
	if sum(payoffs.hershey)>1e-14,
	    [resHershey]=solveDP(xx,payoffs.hershey,0);
	else
	    resHershey.Vbar=zeros(size(resNestle.Vbar));
	end

	[resConsumer]=solveDP(xx,payoffs.surplus/alpha,0);
	% Social Surplus
	[resSocial1]=solveDP(xx,payoffs.retail+payoffs.mars+payoffs.nestle+payoffs.hershey+2*payoffs.surplus/alpha,fcvec);
	% Social Surplus
	[resSocial2]=solveDP(xx,payoffs.retail+payoffs.mars+payoffs.nestle+payoffs.hershey+payoffs.surplus/alpha,fcvec);
	% Social Surplus
	[resSocial4]=solveDP(xx,payoffs.retail+payoffs.mars+payoffs.nestle+payoffs.hershey+0.5*payoffs.surplus/alpha,fcvec);
    % Obtain optimal policies for socially optimal effort levels, 
    % all individual brands, consumer surplus and retailer payoffs 
	profits.Retail =resNReb.Vbar';
	profits.Mars =resMars.Vbar';
	profits.Hershey =resHershey.Vbar';
	profits.Nestle =resNestle.Vbar';
	profits.Consumer =resConsumer.Vbar';
	profits.Social = resSocial2.Vbar';
	profits.Social1 = resSocial1.Vbar';
	profits.Social4 = resSocial4.Vbar';
    
    %Obtain weighted consumer surplus using retailer payoffs
    retailer= payoffs.retail + 6*payoffs.surplus/alpha;   
    retailerrebate= retailer+payoffs.mars.*rebsize;

    [resRReb]=solveDP(xx,retailerrebate,fcvec);
	[resNReb]=solveDP(xx,retailer,fcvec);
	[resInt]=solveDP(xx,retailer+payoffs.mars,fcvec);
	[resIndustry]=solveDP(xx,retailer+payoffs.mars+payoffs.nestle+payoffs.hershey,fcvec);
	[resMars]=solveDP(xx,payoffs.mars,0);
	[resNestle]=solveDP(xx,payoffs.nestle,0);
    
    %Return optimal policies and long run profits
toc
    policies=[resNReb.policy; resRReb.policy; resInt.policy; resIndustry.policy; resSocial2.policy;resSocial1.policy;resSocial4.policy];
	longrun_profits=structofarrays2arrayofstructs(profits);
end