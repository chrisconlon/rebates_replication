%This function takes in 5 parameters and returns a matrix containing
%differences for effort policies on different brands and the retailer
%payoffs as well as total surplus, producer surplus and weighted consumer 
%surplus differences. It also includes a weighted payoff for mars bars for
%initial effort policy. The parameters are two cases, usually different
%profit functions which each take in a effort policy as parameters 
%and output their individual payoffs under those policies. We have two
%effort policies as well to provide to our different case functions.
%Then we have an elasticity level parameter which is used to 
%weight the consumer surplus difference.
function [x]=payoff_difference(caseA,caseB,effA,effB,elas, mc)
    if nargin < 6,
        elas = -2;
    end
    if mc == 0,
        lambda=0.16;
    else
        lambda=0.222;
    end
    % normalized for elas = -2 at 2.7070
    alpha=2.7070/2 * abs(elas);
    alpha=2/ abs(elas);
    
    A = caseA(effA);
    B = caseB(effB);
    A.PS = A.Retail + A.Mars + A.Hershey + A.Nestle;
    B.PS = B.Retail + B.Mars + B.Hershey + B.Nestle;
    
    
    deltaR = A.Retail-B.Retail;
    deltaM = A.Mars - B.Mars;
    deltaN = A.Nestle - B.Nestle;
    deltaH = A.Hershey - B.Hershey;
    
    deltaPS = A.PS - B.PS;
    deltaCS = (A.Consumer-B.Consumer)/alpha;
    deltaSS = deltaPS + deltaCS;
    
    x=[deltaR deltaM deltaH deltaN deltaPS deltaCS deltaSS (A.Mars)*lambda]';
    
end
