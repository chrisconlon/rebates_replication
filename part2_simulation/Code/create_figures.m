%In this file, we determine an appropriate weighted assortment for the
%retailer and how they respond to payoffs they recieve from different 
%assortments of products in the vending machine taking into account the 
%pricing of the products. The code outputs heatmaps and scatterplots of 
%payoffs from mars and hershey products under different pricing levels. 
clear
% Grab the correct parameter and setup the filenames
fn=fullfile('../Output/',strcat('Profits_mc15.mat'));
load(fn)
e=214;

profitsHH=profitsHH(e);
profitsHM=profitsHM(e);
profitsMM=profitsMM(e);

% set up grid of prices
p_vec = [15:54]./100;
p_vec;
[id1,id2]=meshgrid(1:length(p_vec));
id1=id1(:);
id2=id2(:);
w_m = p_vec(id1);
w_h = p_vec(id2);

% find retailer's best response
n = length(w_m);

n_grid=length(p_vec);

for i=1:n,
    out(i)=find_eq(w_h(i), w_m(i), profitsHH,profitsHM,profitsMM,0);
    out2(i)=find_eq(w_h(i), w_m(i), profitsHH,profitsHM,profitsMM,1);
end

% 1 = HH , 2 = HM, 3=MM; --> MM on bottom right
assortMat1 = sparse(id1,id2,[out.assort_id]);
assortMat2 = sparse(id1,id2,[out2.assort_id]);

[A2,B2,mars2, hershey2,p_m2,p_h2,pi_mars2,br_mars2,pi_hershey2,br_hershey2] = setup(out,id1,id2,w_m,w_h);
printHeatmaps(p_vec, A2,B2, 2,1)
[A1,B1,mars1, hershey1,p_m1,p_h1,pi_mars1,br_mars1,pi_hershey1,br_hershey1] = setup(out2,id1,id2,w_m,w_h);
printHeatmaps(p_vec, A1,B1, 1,3)

hershey_brs2=full(sparse(1:n_grid,br_hershey2,1,n_grid,n_grid));
mars_brs2=full(sparse(br_mars2,1:n_grid,1,n_grid,n_grid));

hershey_brs1=full(sparse(1:n_grid,br_hershey1,1,n_grid,n_grid));
mars_brs1=full(sparse(br_mars1,1:n_grid,1,n_grid,n_grid));

bestresponseplot(mars_brs2, hershey_brs2,p_vec,2,6)
bestresponseplot(mars_brs1, hershey_brs1,p_vec,1,5)

function printHeatmaps(p_vec, A,B, i,c)
    figure(c);
    h = heatmap(p_vec',p_vec',A,'XLabel','Hershey Price','YLabel','Mars Price','Title','Mars Payoffs');
    h.YDisplayData = flipud(h.YDisplayData);
    saveas(h,strcat('../Tables and Figures/linear_mars',int2str(i),'.png'))

    figure(c+1);
    h = heatmap(p_vec',p_vec',B,'XLabel','Hershey Price','YLabel','Mars Price','Title','Hershey Payoffs');
    h.YDisplayData = flipud(h.YDisplayData);
    saveas(h,strcat('../Tables and Figures/linear_hershey',int2str(i),'.png'))
end


function [A,B,mars, hershey,p_m,p_h,pi_mars,br_mars,pi_hershey,br_hershey] = setup(out,id1,id2,w_m,w_h)
    mars = [out.Mars];
    hershey = [out.Hershey];

    A=sparse(id1,id2,mars);
    B=sparse(id1,id2,hershey);
  
    p_m = sparse(id1,id2,w_m);
    p_h = sparse(id1,id2,w_h);

    [pi_mars,br_mars] = max(A,[],1);
    [pi_hershey,br_hershey] = max(B,[],2);
end

% Scatter of BR plots (same as Fig 3)
function bestresponseplot(mars_brs, hershey_brs,p_vec,k,c)
    figure(c);
    [i,j,s]=find(mars_brs);
    [i2,j2,s2]=find(hershey_brs);
    s=scatter(p_vec(i),p_vec(j),36,s,'filled','r');
    hold on
    s2=scatter(p_vec(i2),p_vec(j2),36,s2,'filled','b');
    set(gca,'FontSize',20)
    xlabel('Hershey Best Response (blue)')
    ylabel('Mars Best Response (red)')
    title('Best Responses')
    saveas(gca, strcat('../Tables and Figures/linear_br',int2str(k),'.png'))
end