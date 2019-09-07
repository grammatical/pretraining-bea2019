#!/bin/bash -v

MARIAN=./tools/marian-dev/build

if [ $# -lt 3 ]; then
    echo "usage: $0 <model-dir> <input-file> <output-file> <marian-options>" 1>&2
    exit 1
fi

if [ ! -e $MARIAN/marian-decoder ]; then
    echo "marian-decoder is not compiled in $MARIAN/" 1>&2
    exit 1
fi

MODEL=$1
shift
# The input needs to be tokenizer with the spaCy tokenizer
INPUT=$1
shift
OUTPUT=$1
shift


# Generate the n-best list with the ensemble NMT + LM system
$MARIAN/marian-decoder -c $MODEL/config.yml --n-best -i $INPUT -o $OUTPUT.nbest0 --log $OUTPUT.nbest0.log $@

# Re-score the n-best list with each right-to-left model
for i in 1 2 3 4; do
    $MARIAN/marian-scorer -m $MODEL/rl$i.npz -v $MODEL/vocab.{spm,spm} --n-best --n-best-feature R2L$i \
        --workspace 6000 --mini-batch-words 4000 $@ \
        -t $INPUT $OUTPUT.nbest$(expr $i - 1) > $OUTPUT.nbest$i --log $OUTPUT.nbest$i.log
done

# Re-rank the n-best list
python ./tools/rescore.py -c $MODEL/rescore.ini -t -n 1.0 < $OUTPUT.nbest4 > $OUTPUT
