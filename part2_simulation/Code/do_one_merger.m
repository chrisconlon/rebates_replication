%The function takes in the profit levels for four assortments of product as
%input, the output is a merger table which compares the impact of an
%exclusive mars stocking policy under alternative ownership structures as
%well as a cutoff price to avoid foreclosure and an appropriate percent
%reduction in rebate.
%This code corresponds to Table 14 in the Paper "revision2_july2019"
function [x]=do_one_merger(profitsMM,profitsHM,profitsHH,profitsNN,mc)

if mc == 0,
    lambda=0.16;
else 
    lambda=0.222;
end

% update for mc15 effort
merger_table=[...
    payoff_difference(profitsMM,profitsHH,189,212,-2, mc)...
    payoff_difference(profitsHM,profitsNN,191,206,-2, mc)...
    payoff_difference(profitsMM,profitsHH,189,212,-2, mc)...
    payoff_difference(profitsMM,profitsHH,189,212,-2, mc)];

%% now adjust for the merger
% Mars Hershey
merger_table(2,2)=merger_table(2,2)+merger_table(3,2);
merger_table(3,2)=merger_table(4,2);
merger_table(4,2)=0;
merger_table(8,2)=merger_table(8,2)+lambda*profitsHM(191).Hershey;

% Mars-Nestle
merger_table(2,3)=merger_table(2,3)+merger_table(4,3);
merger_table(4,3)=0;
merger_table(8,3)=merger_table(8,3)+lambda*profitsMM(191).Nestle;

% Hershey-Nestle
merger_table(3,4)=merger_table(3,4)+merger_table(4,4);
merger_table(4,4)=0;

% Fix second column for nestle wholesale price
wholesale_p=[42.75 44.00  42.75  42.75 ];

piH = merger_table(3,:);
piR = merger_table(1,:);
reb = merger_table(8,:);


% sum of piR+piH+reb
cutoff_price=mc*100+wholesale_p.*sum(merger_table([1 3 8],:),1)./piH;
markup = (mc*100-wholesale_p)./(wholesale_p);

reduced_lambda=100*(piR+piH+reb)./reb;
x=[merger_table([1 2 3 8 5 6],:); cutoff_price; reduced_lambda];

end