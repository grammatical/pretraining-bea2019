#!/bin/bash

set -eo pipefail

TOOLS=./tools
MODEL=./model.restricted
DIR=./outputs.restricted

mkdir -p $DIR

for prefix in ABCN.dev fce.dev fce.test; do
    # Translate
    test -s $DIR/$prefix.out || bash run.sh $MODEL data/$prefix.err $DIR/$prefix.out $@

    # Evaluate
    python3 $TOOLS/errant/parallel_to_m2.py -orig data/$prefix.err -cor $DIR/$prefix.out -out $DIR/$prefix.out.m2
    python3 $TOOLS/errant/compare_m2.py -ref data/$prefix.m2 -hyp $DIR/$prefix.out.m2 > $DIR/$prefix.out.eval
done

for prefix in ABCN.test; do
    # Translate
    test -s $DIR/$prefix.out || bash run.sh $MODEL data/$prefix.err $DIR/$prefix.out $@
done

for prefix in test2013 test2014; do
    # Translate
    test -s $DIR/$prefix.out || bash run.sh $MODEL data/$prefix.err $DIR/$prefix.out $@

    # Evaluate
    $TOOLS/m2scorer/scripts/m2scorer.py $DIR/$prefix.out data/$prefix.m2 > $DIR/$prefix.eval
done

for infix in dev test; do
    # Translate
    test -s $DIR/jfleg$infix.out || bash run.sh $MODEL $TOOLS/jfleg/$infix/$infix.src $DIR/jfleg$infix.out $@

    # Evaluate
    python $TOOLS/jfleg/eval/gleu.py --src $TOOLS/jfleg/$infix/$infix.src --ref $TOOLS/jfleg/$infix/$infix.ref? --hyp $DIR/jfleg$infix.out > $DIR/jfleg$infix.eval
done

tail $DIR/*.eval
