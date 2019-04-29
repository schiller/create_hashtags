import argparse
from pprint import pprint
from app import HashtagMaker, list_dir, read_file


def get_parser():
    '''Get the parser of command line parameters'''
    parser = argparse.ArgumentParser(description='Create Hashtags.')
    parser.add_argument('dir', help='Directory containing text files')
    parser.add_argument('-c', '--count', type=int, default=10,
                        help='Number of most common words')
    return parser


def main():
    args = get_parser().parse_args()

    hm = HashtagMaker()

    entries = list_dir(args.dir)
    for filename, filepath in entries:
        text = read_file(filepath)
        hm.load_document(filename, text)

    hashtags = hm.get_most_common(args.count)

    pprint(hashtags)


if __name__ == "__main__":
    main()
