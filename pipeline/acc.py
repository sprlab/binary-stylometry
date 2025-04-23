import sys

results_file=open(sys.argv[1],'r+').read()
def parse_weka(weka_output, with_confidence=False):
    """
    Parses the predictions made by weka to determine how effective the attack
    is. Has two modes: by default, simply returns the proportion of authors
    who are misclassified. If the optional boolean flag with_confidence is
    given, then instead it returns the arithmetic mean of the percentage
    chance the classifier assigns to the incorrect answer(s)

    i.e. an output of 0 means perfect classification, while an output of 1
    means complete misclassification
    """
    lines = weka_output.split('\n')
    data = lines[5:] # unclear if this is a safe assumption - TODO
    num_errors = 0
    total = 0
    obj_vals = list()
    for line in data:
        if not line:
            break

        words = line.split()
        total += 1
        confidence = words[-1]
        if len(words) == 4: # correct classification
            obj_vals.append(1-float(confidence))
        elif len(words) == 5: # misclassification
            num_errors += 1 
            obj_vals.append(float(confidence))
        else:
            print("data ended, terminating")
            break

    if with_confidence:
        print(obj_vals)
        return sum(obj_vals)/len(obj_vals)
    else:

        return ( 1 - (num_errors / total)) *100

print(results_file)
print(parse_weka(results_file),"(%) accuracy")