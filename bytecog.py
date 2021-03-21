import argparse
import matplotlib.pyplot as plt
import numpy as np

from utils import get_file_entropy, get_file_chunk_entropy, get_value_sorted, calculate_similarity, CHUNK_SIZE

def byteCog():
        try:
            arg_parser = argparse.ArgumentParser(description='Determine whether an unknown provided sample is similar to a known sample')

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

            args = arg_parser.parse_args()

        except Exception as exc:
            print(exc)
            return

        # Calculate similiarity & graphs

        known_file = open(args.known, 'rb').read()
        unknown_file = open(args.unknown, 'rb').read()

        known_file_entropy = get_file_entropy(args.known)
        unknown_file_entropy = get_file_entropy(args.unknown)

        if known_file:
            k_y = get_file_chunk_entropy(known_file)[0] # Entropy
            k_x = get_file_chunk_entropy(known_file)[1] # Offset

            for x, y in zip(k_x, k_y):
                if y == np.min(k_y):
                    min_x = x

                    FRONT = known_file[min_x - CHUNK_SIZE:min_x]
                    BACK = known_file[min_x:min_x + CHUNK_SIZE]
                    known_file_extracted_content = FRONT + BACK

                    plt.plot(min_x, np.min(k_y), marker="o")
                    plt.annotate(f"Lowest Entropy (Known File) ({args.known}) [{args.identifier}]", (min_x, np.min(k_y)), ha="center", va="top")

            plt.plot(k_x, k_y, label='Known File Entropy')
            plt.axis()

        if unknown_file:
            u_y = get_file_chunk_entropy(unknown_file)[0] # Entropy
            u_x = get_file_chunk_entropy(unknown_file)[1] # Offset

            for x, y in zip(u_x, u_y):
                if y == np.min(u_y):
                    min_x = x

                    FRONT = unknown_file[min_x - CHUNK_SIZE:min_x]
                    BACK = unknown_file[min_x:min_x + CHUNK_SIZE]
                    unknown_file_extracted_content = FRONT + BACK

                    plt.plot(min_x, np.min(u_y), marker="o")
                    plt.annotate(f"Lowest Entropy (Unknown File) ({args.unknown})", (min_x, np.min(u_y)), ha="center", va="top")

            plt.plot(u_x, u_y, label='Unknown File Entropy')

        contrast = {}

        if known_file and unknown_file:
            # Calculate drift
            for y_k, y_u, x_k, x_u in zip(k_y, u_y, k_x, u_x):
                drift_entropy = abs(y_k - y_u)
                if x_k == x_u: # Check if offsets are the same, if some weird case occurs
                    contrast[x_u] = float(drift_entropy)

        DRIFT_THRESHOLD = (abs(known_file_entropy - unknown_file_entropy) / 2) / 10
        if DRIFT_THRESHOLD > 0:
            print(f"[+] Using DRIFT_THRESHOLD of {DRIFT_THRESHOLD}")
        else:
            print(f"[-] Expected DRIFT_THRESHOLD above 0, but got {DRIFT_THRESHOLD}")
            return

        abnormal_drift = {}
        for offset, entropy_drift in get_value_sorted(contrast).items():
            if entropy_drift >= DRIFT_THRESHOLD:
                abnormal_drift[offset] = entropy_drift

        abnormal_drifts = len(abnormal_drift.keys())
        if abnormal_drifts > 0:
            print(f"\n[+] Found {abnormal_drifts} abnormal entropy drifts:")
        else:
            print("\n[-] No abnormal entropy drifts were found!")

        top_entropy_drift = 0
        if abnormal_drift.values():
            top_entropy_drift = max(abnormal_drift.values())

        for offset, entropy_drift in abnormal_drift.items():
            print(f" - Offset: {offset} | Entropy Drift: {entropy_drift}")
        print()

        similarity = calculate_similarity(args.known, args.unknown, top_entropy_drift, 2)

        print(f"[+] Similarity of {args.identifier} sample: {similarity}%")

        if known_file_extracted_content and unknown_file_extracted_content:
            print(known_file_extracted_content)
            print()
            print()
            print(unknown_file_extracted_content)

        plt.legend()
        plt.title('Chunk Entropy Graph')
        plt.show()

byteCog()
