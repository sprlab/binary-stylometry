

import argparse
import re
import os


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("path", metavar="/path/to/arff")
    argparser.add_argument("--features", metavar="/path/to/feature_arff",
            help="Write a new arff file using data from first arff," +
                " and features from this one.")
    argparser.add_argument("-v", help="increase verbosity", action="store_true")
    args = argparser.parse_args()

    if args.features:
        feature_set = parse_arff(args.features, verbose=args.v, features_only=True)
                    
        if args.v:
            print(f"Feature set extracted from {args.features}:\n{feature_set}\n")
            print(f"{len(feature_set)} total features")
        data = parse_arff(args.path)

        new_data = list()

        for datadict in data:
            newdict = {f:datadict.get(f,'0') for f in feature_set}
            new_data.append(newdict)


        # write data to new arff file
        new_file = args.path.rsplit('.',1)[0] + "_ff_" + os.path.basename(args.features)

        copy_features(args.features, new_file)
        with open(new_file, 'a') as fobj:
            for datadict in new_data:
                fobj.write(",".join(datadict.values()) + "\n")
    else:
        print(parse_arff(args.path))


def copy_features(source, dest):
    """
    Copy the features section of an arff file from source to dest,
    stopping immediately after the @data header
    """
    with open(source) as src:
        lines = list()
        for line in src:
            lines.append(line)
            if line[:5] == "@data":
                break

    with open(dest, 'w') as dst:
        for line in lines:
            dst.write(line)


def parse_arff(fname, verbose=False, features_only=False):
    """
    Reads in an arff file at the given location, and returns a list of dicts
    representing the data. The keys of each dictionary are the features, while
    the value are the corresponding values for each observation.

    if argument 'features_only' is given, simply returns list of features
    """
    features = list()


    with open(fname) as fobj:
        for line in fobj:
            parsed = parse_line(line)
            token = parsed[0]
            if token == "BLANK":
                continue
            elif token == "ATTRIBUTE":
                if parsed[1] == "authorName_original":
                    authors = parsed[2].strip("{}\n").split(',')
                features.append(parse_feature(parsed[1]))
            elif token == "DATA":
                break

        if verbose:
            print(f"Extracted features:\n{features}\n{len(features)} in total")
        if features_only:
            return features
        observations = list()

        for line in fobj:
            data = line.strip().split(',')
            #assert len(features) == len(data), f"{len(features)} features, should be {len(data)}"
            if len(features) != len(data):
                print(f"WARNING: {len(features)} features, should be {len(data)}")
            labeled = dict()
            for k,v in zip(features,data):
                if k in labeled:
                    labeled[k] += f",{v}"
                else:
                    labeled[k] = v
            observations.append(labeled)

    return observations
     


def parse_line(line):
    """
    Reads a single line of the arff format, prior to data
    expected format:
    """
    if not line.strip():
        return ("BLANK",)

    try:
        line_type, rest = line.split(' ', 1)
    except ValueError:
        line_type = line.strip()


    if line_type == "@attribute":
        feature, value_type = rest.rsplit(' ', 1)
        return ("ATTRIBUTE", feature, value_type)

    if line_type == "@relation":
        return ("RELATION",)

    if line_type == "@data":
        return ("DATA",)


def parse_feature(feature):
    """extract the type and value of a feature, setting aside the
    incidental numbering"""
    try:
        feat_type, feat = feature.split(' ', 1)
        m = re.match(r".+?\[(.*)\]'", feat)
        return (feat_type.strip("'"), m.group(1))
    except ValueError: # not a standard feature
        return (feature.strip("'"),)
    


if __name__ == "__main__":
    main()
