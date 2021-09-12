%This function is used to help print table 11
%The function takes in a profit function, a policy function, an elasticty
%level and a Boolean value that determines whether to use a specific alpha
%value
function [table]=print_pi_ae_table(profits,policy,elas,use_alpha, mc)
    %We create a temporary value for the profits using a provided policty
    temp=profits(policy);
    %This If/else statement determines which alpha case to utilize in
    %calculation
    if use_alpha,
        alpha=2.7070/2 * abs(elas);
    else,
        alpha=abs(elas)/2;
    end
    %rebsize is a variable that contains the size of the rebate
    if mc == 0,
        rebsize = 0.16;
    else
        rebsize = 0.222;
    end
    %Creating our effort policy table with a for loop, we use the single_ae
    %function to populate the created matrix with vectors of size 10.
    %The table's length is determined by the size of the temporary profits
    %table and the it has 10 columns.
    table=zeros(length(temp),10);
    for i=1:length(temp),
        table(i,:)=single_ae(temp(i),policy(i));
    end
    
    %Creating another function that takes in a policy and our temporary profit
    %function and returns a vector which includes information such as
    %producer surplus, the impact of a rebate for mars bars, weighted
    %consumer surplus and SS(?)
    function [x]=single_ae(A,eff)
            A.PS = A.Retail + A.Mars + A.Hershey + A.Nestle;
            SS = A.PS + A.Consumer/alpha;
            x=[eff A.Retail rebsize*A.Mars A.Mars A.Hershey A.Nestle A.Retail+A.Mars A.PS A.Consumer/alpha SS ];
    end

end
