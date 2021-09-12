function [reb,reduced_lambda,cutoff_price]=compute_countermeasures(table,mc)
    piH = table(3,:,:);
    piR = table(1,:,:);
    
    if piH(1)> 0,
        piH = -1*piH;
        piR = -1*piR;
    end
    
    reb = table(8,:,:);
    tot = (piR+piH+reb);    
    
    if mc == 0,
        reduced_lambda=squeeze(100*(1-(piH*(15-42.75)./(42.75)-piR)./reb));
    else,
        reduced_lambda=squeeze(100*(tot)./reb);
        
    end
    cutoff_price=squeeze(mc*100+(42.75-100*mc)*tot./piH);
end

%reduced_lambda=squeeze(100*(piR+piH+reb)./reb);
%cutoff_price=squeeze(mc*100+(42.75-100*mc)*tot./piH);

