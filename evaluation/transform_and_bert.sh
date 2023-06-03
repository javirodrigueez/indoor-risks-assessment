# ARGUMENTS
# -------------------------
# 1 -> input
# 2 -> dataset
# 3 -> transformation
# 4 -> predictions file name
# 5 -> annotations file name
# -------------------------

if [ "$3" == "r" ]; then
  echo "Raw transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py > ../results/transf.$2
elif [ "$3" == "rp" ]; then
  echo "Raw+pos transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos > ../results/transf.$2
elif [ "$3" == "rl" ]; then
  echo "Raw+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --lemma > ../results/transf.$2
elif [ "$3" == "rpl" ]; then
  echo "Raw+pos+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --lemma > ../results/transf.$2
elif [ "$3" == "p" ]; then
  echo "Punct transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --punct > ../results/transf.$2
elif [ "$3" == "pp" ]; then
  echo "Punct+pos transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --punct > ../results/transf.$2
elif [ "$3" == "pl" ]; then
  echo "Punct+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --punct --lemma > ../results/transf.$2
elif [ "$3" == "ppl" ]; then
  echo "Punct+pos+lemma transformation is going to be applied"
  tail -n +2 $1 | python3 transform_text.py --pos --punct --lemma > ../results/transf.$2
else
  echo "Wrong transformation argument"
  exit
fi

if [ "$3" == "p" ] || [ "$3" == "pp" ] || [ "$3" == "ppl" ] || [ "$3" == "pl" ]; then
  echo "Removing commas from transformed sentences..."
  cat ../results/transf.$2 | python3 separate_lines.py $4 $5 --punct
else
  cat ../results/transf.$2 | python3 separate_lines.py $4 $5
fi
bert-score -r $5 -c $4 --lang en --rescale_with_baseline