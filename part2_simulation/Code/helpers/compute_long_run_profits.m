
%The function takes in five parameters and returns results on long run 
%profits and relevant optimal
%effort policies. The four input parameters are a matrix of payoffs,
%a stationary vector of incremental sales, the level of fixed costs, the
%elasticity level and a boolean for a marginal cost of zero. 
%It returns a matrix containing long run smoothed
%profit levels as well as corresponding effort policies.
function [longrun_profits,policies]=compute_long_run_profits(payoffs,xx,fcvec,elas,mc)

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
	retailerrebate= payoffs.retail+payoffs.mars.*rebsize;
    %Solve the dynamic programming problems for Retailer Rebates, 
    %Retailers, and the different brands, using the fixed cost passed in
    %the function
tic
	[resRReb]=solveDP(xx,retailerrebate,fcvec);
	[resNReb]=solveDP(xx,payoffs.retail,fcvec);
	[resInt]=solveDP(xx,payoffs.retail+payoffs.mars,fcvec);
	[resIndustry]=solveDP(xx,payoffs.retail+payoffs.mars+payoffs.nestle+payoffs.hershey,fcvec);
	[resMars]=solveDP(xx,payoffs.mars,0);
	[resMarsExtra]=solveDP(xx,payoffs.marsExtra,0);
	[resNestle]=solveDP(xx,payoffs.nestle,0);

	% Hershey (without FC)
	if sum(payoffs.hershey)>1e-14
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
toc    
    %Set Appropriate Effort Policies
	profits.Retail =resNReb.Vbar';
	profits.Mars =resMars.Vbar';
	profits.MarsExtra =resMarsExtra.Vbar';
	profits.Hershey =resHershey.Vbar';
	profits.Nestle =resNestle.Vbar';
	profits.Consumer =resConsumer.Vbar';
	profits.Social = resSocial2.Vbar';
	profits.Social1 = resSocial1.Vbar';
	profits.Social4 = resSocial4.Vbar';
    %Return Effort Policies and Profits

	policies=[resNReb.policy; resRReb.policy; resInt.policy; resIndustry.policy; resSocial2.policy;resSocial1.policy;resSocial4.policy];
	longrun_profits=structofarrays2arrayofstructs(profits);
end