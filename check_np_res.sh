#!/bin/sh

swipl np.pl > res
sed -i '.bak' 's/phrases/bad_phrases/g' np.pl
swipl np.pl > bad_res
sed -i '.bak' 's/bad_phrases/phrases/g' np.pl
echo 'Good:'
grep -c GOOD res
echo 'FalseGood:'
grep -c GOOD bad_res 
