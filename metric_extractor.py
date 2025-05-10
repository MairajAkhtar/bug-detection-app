import lizard
import csv
import os

def extract_metrics(project_path, output_csv):
    features = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(('.py', '.java', '.cpp', '.c', '.js')):
                file_path = os.path.join(root, file)
                analysis = lizard.analyze_file(file_path)
                total_loc = analysis.nloc
                lloc = sum(f.length for f in analysis.function_list)
                total_functions = len(analysis.function_list)
                tna = 0  # Not available from lizard
                pua = 0  # Not available from lizard
                nle = 0  # Not available from lizard
                tlloc = lloc
                tnlpm = sum(f.cyclomatic_complexity for f in analysis.function_list)
                tloc = total_loc
                nlpm = tnlpm // total_functions if total_functions else 0
                nlm = lloc // total_functions if total_functions else 0
                tnlm = lloc
                imports = sum(1 for line in open(file_path, encoding="utf-8", errors="ignore") if 'import' in line)
                tnos = lloc
                nos = lloc // total_functions if total_functions else 0
                nl = tnlpm
                features.append([
                    total_loc, lloc, tna, total_functions, pua, tlloc, nle, tnlpm,
                    tloc, nlpm, nlm, tnlm, imports, tnos, nos, nl
                ])
    with open(output_csv, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "TCLOC", "LLOC", "TNA", "NM", "PUA", "TLLOC", "NLE", "TNLPM",
            "TLOC", "NLPM", "NLM", "TNLM", "NOI", "TNOS", "NOS", "NL"
        ])
        writer.writerows(features)
