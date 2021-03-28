import argparse

import time
import uuid

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.distance import directed_hausdorff

from utils.entropy_utils import get_file_entropy, get_file_chunk_entropy, CHUNK_SIZE
from utils.general_utils import get_value_sorted, list_tuple_merger
from utils.string_utils import jaro_distance, string_to_boolean
from utils.log_utils import write_log_message

main_prefix = 'BYTECOG | '

def byteCogBanner():
    print("""
======================================================
|      ____          __         ______               |
|     / __ ) __  __ / /_ ___   / ____/____   ____    |
|    / __  |/ / / // __// _ \ / /    / __ \ / __ \   |
|   / /_/ // /_/ // /_ /  __// /___ / /_/ // /_/ /   |
|  /_____/ \__, / \__/ \___/ \____/ \____/ \__, /    |
|         /____/                          /____/     |
|                                                    |
|                    Version: 0.3                    |
|               Author: IlluminatiFish               |
======================================================
    """)


def byteCogStartup():
    byteCogBanner()
    try:
        arg_parser = argparse.ArgumentParser(
            description='Determine whether an unknown provided sample is similar to a known sample')

        arg_parser.add_argument('-k',
                                '--known',
                                action='store',
                                required=True,
                                help='The file path to the known sample')

        arg_parser.add_argument('-u',
                                '--unknown',
                                action='store',
                                required=True,
                                help='The file path to the unknown sample')

        arg_parser.add_argument('-i',
                                '--identifier',
                                action='store',
                                required=True,
                                help='The antivirus identifier of the known file')

        arg_parser.add_argument('-v',
                                '--visual',
                                action='store',
                                required=True,
                                help='If you want to show a visual representation of the file entropy')

        args = arg_parser.parse_args()


    except Exception as exc:
        print(exc)
        return


    visual_valid_args = ['true', 'false']
    if args.visual.lower() not in visual_valid_args:
        print("[+] The -v VISUAL argument must be a boolean")
        return
    else:
        use_visual = string_to_boolean(args.visual.lower())


    log_file_name = str('bytecog-log-' + str(uuid.uuid4())) + '.bclog'
    print(f'[=] Log file name: {log_file_name}')

    start = time.time()
    # Calculate similarity & graphs
    try:
        known_file = open(args.known, 'rb').read()
        unknown_file = open(args.unknown, 'rb').read()

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Loaded files into analysis!', log_file_name)

        known_file_entropy = get_file_entropy(args.known)
        unknown_file_entropy = get_file_entropy(args.unknown)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Calculated entropy for both files', log_file_name)

        if known_file:
            prefix = 'KNOWN FILE | '

            k_y = get_file_chunk_entropy(known_file)[0]  # Entropy
            k_x = get_file_chunk_entropy(known_file)[1]  # Offset

            write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Calculated chunked entropy and offset data', log_file_name)
            write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Attempting to calculate lowest entropy point in graph', log_file_name)

            for x, y in zip(k_x, k_y):
                if y == np.min(k_y):
                    min_x = x

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Found lowest entropy offset chunk in graph {str(min_x)}', log_file_name)

                    FRONT = known_file[min_x - CHUNK_SIZE:min_x]
                    BACK = known_file[min_x:min_x + CHUNK_SIZE]

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Calculated front & back buffers of the content found at the lowest entropy point', log_file_name)

                    known_file_extracted_content = FRONT + BACK

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Found content at lowest entropy point with front & back buffers', log_file_name)

                    if use_visual is True:
                        plt.plot(min_x, np.min(k_y), marker="o")
                        plt.annotate(f"Lowest Entropy (Known File) ({args.known}) [{args.identifier}]",
                                     (min_x, np.min(k_y)),
                                     ha="center", va="top")

                        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Plotted lowest entropy point on graph at ({str(min_x)}, {str(np.min(k_y))})', log_file_name)

            if use_visual is True:
                plt.plot(k_x, k_y, label='Known File Entropy')

                write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Plotting entropy graph', log_file_name)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Finished plotting known file entropy graph', log_file_name)

        if unknown_file:
            prefix = 'UNKNOWN FILE | '

            u_y = get_file_chunk_entropy(unknown_file)[0]  # Entropy
            u_x = get_file_chunk_entropy(unknown_file)[1]  # Offset

            write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Calculated chunked entropy and offset data', log_file_name)
            write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Attempting to calculate lowest entropy point in graph', log_file_name)

            for x, y in zip(u_x, u_y):
                if y == np.min(u_y):
                    min_x = x

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Found lowest entropy offset chunk in graph {str(min_x)}', log_file_name)

                    FRONT = unknown_file[min_x - CHUNK_SIZE:min_x]
                    BACK = unknown_file[min_x:min_x + CHUNK_SIZE]

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Calculated front & back buffers of the content found at the lowest entropy point', log_file_name)

                    unknown_file_extracted_content = FRONT + BACK

                    write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Found content at lowest entropy point with front & back buffers', log_file_name)

                    if use_visual is True:
                        plt.plot(min_x, np.min(u_y), marker="o")
                        plt.annotate(f"Lowest Entropy (Unknown File) ({args.unknown})", (min_x, np.min(u_y)),
                                     ha="center",
                                     va="top")

                        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Plotting entropy graph', log_file_name)

            if use_visual is True:
                plt.plot(u_x, u_y, label='Unknown File Entropy')

                write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + f'Plotting entropy graph', log_file_name)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + prefix + 'Finished plotting known file entropy graph', log_file_name)

        contrast = {}

        if known_file and unknown_file:

            # Calculate drift
            for y_k, y_u, x_k, x_u in zip(k_y, u_y, k_x, u_x):
                drift_entropy = abs(y_k - y_u)

                if x_k == x_u:  # Check if offsets are the same, if some weird case occurs
                    contrast[x_u] = float(drift_entropy)

                    if drift_entropy > 0: # Do not clog up the log file if drift entropy is 0
                        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + f'Calculating drift entropy of each entropy offset point ({y_k}, {y_u}) (Drift: {drift_entropy})', log_file_name)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Calculating drift threshold for our scenario', log_file_name)

        drift_threshold = (abs(known_file_entropy - unknown_file_entropy) / 2) / 10

        write_log_message(
            f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + f'Calculated drift threshold -> {drift_threshold}',
            log_file_name)

        if drift_threshold > 0:
            print(f"[+] Using DRIFT_THRESHOLD of {drift_threshold}")
        else:
            print(f"[-] Expected DRIFT_THRESHOLD above 0, but got {drift_threshold}")
            return

        abnormal_drift = {}

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Detecting abnormal entropy drifts between both files/graphs', log_file_name)

        for offset, entropy_drift in get_value_sorted(contrast).items():
            if entropy_drift >= drift_threshold:
                abnormal_drift[offset] = entropy_drift

        abnormal_drifts = len(abnormal_drift.keys())
        if abnormal_drifts > 0:
            print(f"\n[+] Found {abnormal_drifts} abnormal entropy drifts:")
        else:
            print("\n[-] No abnormal entropy drifts were found!")

        for offset, entropy_drift in abnormal_drift.items():
            print(f" - Offset: {offset} | Entropy Drift: {entropy_drift}")
        print()

        difference = None

        if known_file_extracted_content and unknown_file_extracted_content:
            """
                NOTE: Not really needed for the usage, just some debug I guess.
            """
            print('[+] The known file content extracted:\n')
            print(known_file_extracted_content)
            print("\n" * 2)
            print('[+] The unknown file content extracted:\n')
            print(unknown_file_extracted_content)

            """
                Implements a string distance metric algorithm, Jaro-Winkler in this case to verify 
                if the Hausdorff Distance is a valid percentage for the similarity between each sample
            """

            if known_file_extracted_content != unknown_file_extracted_content:

                write_log_message('[{time.time()}]' + main_prefix + 'Extracted contents are not similar to each other',
                                  log_file_name)

                try:
                    known_file_extracted_content_string = known_file_extracted_content.decode()
                    unknown_file_extracted_content_string = unknown_file_extracted_content.decode()
                except UnicodeDecodeError:
                    print(
                        "\n[+] Failed to decode extracted content from bytes to string..\n[+] Attempting to cast to string object")
                    known_file_extracted_content_string = str(known_file_extracted_content)
                    unknown_file_extracted_content_string = str(unknown_file_extracted_content)

                write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Attempting to calculate adjusted similarity score between both files',
                                  log_file_name)

                if known_file_extracted_content_string is not None and unknown_file_extracted_content_string is not None:
                    jaro_span = jaro_distance(known_file_extracted_content_string,
                                              unknown_file_extracted_content_string)

                    difference = (1 - jaro_span) * 100

        res_a = list_tuple_merger(k_x, k_y)
        res_b = list_tuple_merger(u_x, u_y)

        line_1 = np.array(res_a)
        line_2 = np.array(res_b)

        d_h_u_v = directed_hausdorff(line_1, line_2)[0]
        d_h_v_u = directed_hausdorff(line_2, line_1)[0]

        general_hausdorff_distance = max(d_h_u_v, d_h_v_u)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Calculated Hausdorff Distance of both files', log_file_name)

        if difference is not None:
            similarity = 100 - ((general_hausdorff_distance / len(unknown_file)) * 100) - difference
        else:
            similarity = 100 - ((general_hausdorff_distance / len(unknown_file)) * 100)

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + f'Applying Hausdorff & Jaro-Winkler to get an adjusted similarity score of {similarity}%', log_file_name)

        if similarity == 100:
            print(
                f'\n[+] Appears the unknown sample {args.unknown} provided is exactly the same as the known sample {args.known}')

        elif similarity == 0:
            print(
                f'\n[+] Appears the unknown sample {args.unknown} provided is completely different to the known sample {args.known}')

        else:
            print(
                f'\n[+] The unknown sample {args.unknown} is {similarity}% similar to the {args.known} sample ({args.identifier})')

        end = time.time()
        total_time = round(end - start, 3)

        print(f"[+] Finished analysis in {total_time} seconds")

        write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + f'Analysis finished completed in {total_time} seconds!', log_file_name)

        if use_visual is True:
            plt.legend()
            plt.title('Chunk Entropy Graph')
            plt.show()

            write_log_message(f'[{time.strftime("%Y-%m-%d %H:%M:%S")}] ' + main_prefix + 'Showing plotted graph',
                              log_file_name)



    except Exception as exception:
        print(f"[+] Error: {type(exception).__name__}\n\nTraceback:\n  - {exception}")


byteCogStartup()
