%The function takes in 6 parameters including the wholesale value of 
% Hershey and mars bars, the profit level for all
%three assortments of products, a boolean which indicates whether a
%representative machine is used.
%The function outputs a weighted machine assortment taking into account the
%impact of profits.
function [out] = find_eq(w_H, w_M, profitsHH,profitsHM,profitsMM,all_prods)
    p_mars = .5373; p_hershey = .4275;
    mc= 0.15;
   
    lam_mars = 1-(w_M - mc)./(p_mars - mc);
    lam_hershey = 1-(w_H - mc)./(p_hershey - mc);
    
    if all_prods,
        profitsHH.MarsExtra = profitsHH.Mars;
        profitsHM.MarsExtra = profitsHM.Mars;
        profitsMM.MarsExtra = profitsMM.Mars;
    end
    
    
    r_HH=profitsHH.Retail + lam_mars * profitsHH.MarsExtra + lam_hershey * profitsHH.Hershey;
    r_HM=profitsHM.Retail + lam_mars * profitsHM.MarsExtra + lam_hershey * profitsHM.Hershey;
    r_MM=profitsMM.Retail + lam_mars * profitsMM.MarsExtra + lam_hershey * profitsMM.Hershey;
    
    [out.retail,out.assort_id] = max([r_HH,r_HM,r_MM]);

    switch out.assort_id
        case 1,
            out.assort_name = 'HH';
            out.Mars = (1-lam_mars) * profitsHH.MarsExtra;
            out.MarsOther =  profitsHH.Mars - profitsHH.MarsExtra;
            out.Hershey = (1-lam_hershey) * profitsHH.Hershey;
        case 2,
            out.assort_name = 'HM';
            out.Mars = (1-lam_mars) * profitsHM.MarsExtra;
            out.MarsOther =  profitsHM.Mars - profitsHM.MarsExtra;
            out.Hershey = (1-lam_hershey) * profitsHM.Hershey;
        case 3,
            out.assort_name = 'MM';
            out.Mars = (1-lam_mars) * profitsMM.MarsExtra;
            out.MarsOther =  profitsMM.Mars - profitsMM.MarsExtra;
            out.Hershey = (1-lam_hershey) * profitsMM.Hershey;
    end        
    
end