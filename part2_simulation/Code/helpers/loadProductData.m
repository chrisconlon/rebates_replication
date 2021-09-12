%
% This script loads product info and fixes product names and margins
%
MP=importdata('../Raw Data/product-margins.csv');
J=73;
% exclude these products not in demand estimates
mindex=~ismember(MP.data(:,1),[408; 8769; 99924; 99925; ]);
price=[MP.data(mindex,2);0];
cost1=[MP.data(mindex,3);0];
reb=[MP.data(mindex,5);0];


mmplain = 14; butterfinger = 11; milkyway = 15; payday=16; reeses = 18; raisinets=36; threemusk = 10;
mmpeanut = 13; snickers = 20; skittles = 19; twix =23; crunch=54;
mars = sort([mmplain mmpeanut snickers twix milkyway skittles threemusk]);
marsextra=[threemusk milkyway];

hershey =sort([reeses payday]);
nestle = sort([butterfinger raisinets crunch]);
chocolate =sort([hershey mars nestle]);

cost1(nestle) = 0.44;
margins = price-cost1;