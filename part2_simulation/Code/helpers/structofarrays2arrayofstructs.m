function S = structofarrays2arrayofstructs(A)
   % structofarrays2arrayofstructs does exactly what it says.
   % USAGE: 
   %   S = structofarrays2arrayofstructs(A) assumes that A is a struct, with each field
   %   containing Nx1 (columns) of values. (theoretically NxM values, where M may vary).  This results in an Nx1 array of
   %   structs, each containing 1 (or M) values.
   %  
   %  Example 1
   %     >> A.flower={'Daisy';'Rose';'Violet'};
   %     >> A.color={'white';'red';'violet'};
   %
   %     >> S = structofarrays2arrayofstructs(A)
   %
   %     S = 
   %     1x3 struct array with fields:
   %         flower
   %         color 
   %       
   %     >> S(2)
   %     ans = 
   %         flower: 'Rose'
   %          color: 'red'
   %
   %  Note, Any cells it encounters are unwrapped.
   
   % -Celso Reyes
   
fn=fieldnames(A);

nItems=numel(A.(fn{1}));
sf=fn';

sf(2,1:numel(fn))={{}};
sf = sf(:)';
S=struct(sf{:});

for f=1:numel(fn)
   if iscell( A.(fn{f})(1) )
      for n = nItems: -1 : 1;
         S(n).(fn{f}) = A.(fn{f}){n,:};
      end
   else
      for n = nItems: -1 : 1;
         S(n).(fn{f}) = A.(fn{f})(n,:);
      end
   end
end