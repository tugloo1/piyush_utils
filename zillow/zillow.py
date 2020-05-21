import os
import json


class ZillowAnalyzer(object):
    def __init__(self, main_folder: str):
        self.main_folder = main_folder
        self.listing_status_map = self.read_in_saved_listings()
        """ Each listing can have the following status: like, ignore, unseen
        """

    def read_in_saved_listings(self):
        path = os.path.join(self.main_folder, 'listings.json')
        with open(path, 'r') as f:
            listing_map = json.loads(f.read())
        return listing_map

    def print_unseen_listings(self):
        count = 0
        for listing in self.listing_status_map:
            if self.listing_status_map[listing]['status'] == 'unseen':
                count += 1
                print(listing)
        print(count)

    def process_input_file(self):
        path = os.path.join(self.main_folder, 'input.txt')
        with open(path, 'r') as f:
            file_content = f.readlines()
            for line in file_content:
                self.process_line(line.rstrip())

    def process_line(self, line: str):
        line = line.split(' ')
        listing = line[0]
        if len(line) == 1:
            if listing in self.listing_status_map:
                return
            else:
                self.listing_status_map[listing] = {'status': 'unseen'}
        elif len(line) == 2:
            status = line[1]
            if status not in {"like", "ignore"}:
                raise Exception('FUHHH')

            if listing in self.listing_status_map:
                assert self.listing_status_map[listing]['status'] == status
            else:
                self.listing_status_map[listing] = {'status': status}
        else:
            raise Exception('uh oh')

    def generate_consolidating_listing_file(self):
        pass


if __name__ == '__main__':
    z = ZillowAnalyzer('assets')
    z.process_input_file()
    z.print_unseen_listings()
