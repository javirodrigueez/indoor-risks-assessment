# ARGUMENTS
# ----------------
# 1 -> input text
# 2 -> dataset
# 3 -> output results file
# 4 -> transformation

if [ "$4" == "r" ]; then
  echo "Raw transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py > ../results/transf_$2.txt
elif [ "$4" == "rp" ]; then
  echo "Raw+pos transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos > ../results/transf_$2.txt
elif [ "$4" == "rl" ]; then
  echo "Raw+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --lemma > ../results/transf_$2.txt
elif [ "$4" == "rpl" ]; then
  echo "Raw+pos+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --lemma > ../results/transf_$2.txt
elif [ "$4" == "p" ]; then
  echo "Punct transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --punct > ../results/transf_$2.txt
elif [ "$4" == "pp" ]; then
  echo "Punct+pos transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --punct > ../results/transf_$2.txt
elif [ "$4" == "pl" ]; then
  echo "Punct+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --punct --lemma > ../results/transf_$2.txt
elif [ "$4" == "ppl" ]; then
  echo "Punct+pos+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --punct --lemma > ../results/transf_$2.txt
else
  echo "Wrong transformation argument"
  exit
fi

python3 extract_bleu.py ../results/transf_$2.txt ../results/bleu_$2.txt
paste -d',' ../results/transf_$2.txt ../results/bleu_$2.txt > $3
sed -i '1i\VIDEO,GROUND-TRUTH,INFERENCE,BLEU' $3
cat ../results/bleu_$2.txt | awk -F, '{c+=$1;total++} END {print c/total}'