#!/usr/bin/env python

import sys
import argparse

TEXT_FIELD = 1
FEATURE_FIELD = 2
SCORE_FIELD = 3


def main():
    args = parse_user_args()

    # Read feature names and weights
    weights = read_feature_weights(args.config)

    # Iterate n-best list
    for sid, lines in iterate_nbest(args.input):
        scored_lines = []
        # Iterate candidates
        for i, line in enumerate(lines):
            fields = [f.strip() for f in line.split('|||')]
            feats = fields[FEATURE_FIELD].split()
            # Rescore
            score = rescore_features(feats, weights)
            if args.normalize:
                length = len(fields[TEXT_FIELD].split(' ')) + 1
                score = score / (float(length) ** args.normalize)
            # Keep candidates with new scores
            if args.top_best:
                new_line = fields[TEXT_FIELD]
            else:
                fields[SCORE_FIELD] = str(score)
                new_line = ' ||| '.join(fields)
            scored_lines.append((score, new_line))

        # Sort candidates according to new scores
        scored_lines.sort(key=lambda p: -p[0])

        # Print re-scored candidates
        if args.top_best:
            args.output.write(scored_lines[0][1] + '\n')
        else:
            for _, line in scored_lines:
                args.output.write(line + '\n')


def rescore_features(feats, weights):
    score = 0
    i = 0
    key = ''
    for f in feats:
        if f.endswith('='):
            key = f
            i = 0
            continue
        if key in weights:
            score += (float(f) * weights[key][i])
        # else:
            # sys.stderr.write("Feature '{}' not recognized\n".format(key))
        i += 1
    return score

def iterate_nbest(nbest):
    sid = 0
    prev_sid = 0
    lines = []
    for line in nbest:
        line = line.rstrip('\n')
        sid, _ = line.split(' ||| ', 1)
        sid = int(sid)
        if sid > prev_sid:
            yield sid, lines
            lines = []
        prev_sid = sid
        lines.append(line)
    yield sid, lines


def read_feature_weights(config):
    weights = {}
    while True:
        line = config.readline()
        if not line:
            sys.stderr.write('Error: no [weight] section\n')
            sys.exit(1)
        if '[weight]' in line:
            break
    while True:
        line = config.readline()
        if not line or line.strip().startswith('['):
            break
        if not line.strip():
            continue
        fields = line.split()
        weights[fields[0]] = [float(f) for f in fields[1:]]
    return weights


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', metavar='FILE', required=True,
                        type=argparse.FileType('r'),
                        help='rescore.ini')
    parser.add_argument('-i', '--input', metavar='FILE', nargs='?',
                        type=argparse.FileType('r'), default=sys.stdin,
                        help='input n-best list, default: STDIN')
    parser.add_argument('-o', '--output', metavar='FILE', nargs='?',
                        type=argparse.FileType('w'), default=sys.stdout,
                        help='output re-scored n-best list, default: STDOUT')
    parser.add_argument('-n', '--normalize', metavar='FLOAT', type=float,
                        help='parameter for length normalization')
    parser.add_argument('-t', '--top-best', action='store_true',
                        help='print top best candidate')
    return parser.parse_args()


if __name__ == '__main__':
    main()
