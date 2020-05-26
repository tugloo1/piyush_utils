import os
import json


class ZillowAnalyzer(object):
    defaults = {'pets': 'unknown', 'floor': 0, 'rent': 0, 'area': None, 'target': 0,
                'trader-joes': 0, 'marukai': 0}

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
        to_sort = []
        for listing in self.listing_status_map:
            if self.listing_status_map[listing]['status'] == 'unseen':
                count += 1
                to_sort.append(listing)
        to_sort.sort()
        print('\n'.join(to_sort))
        print(count)
        return count

    def print_liked_listings(self):
        count = 0
        to_sort = []
        for listing in self.listing_status_map:
            if self.listing_status_map[listing]['status'] == 'like':
                count += 1
                to_sort.append(listing)
        to_sort.sort()
        print('\n'.join(to_sort))
        print(count)

    def print_liked_listings_with_unknown_pet_status(self):
        count = 0
        to_sort = []
        for listing in self.listing_status_map:
            info = self.listing_status_map[listing]
            if info['status'] == 'like' and info['pets'] == 'unknown':
                count += 1
                to_sort.append(listing)
        to_sort.sort()
        print('\n'.join(to_sort))
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
            if listing in self.listing_status_map and self.listing_status_map[listing] == 'offline':
                raise Exception('oh boi')
            elif listing in self.listing_status_map:
                return
            else:
                self.listing_status_map[listing] = {'status': 'unseen'}
        elif len(line) == 2:
            status = line[1]
            if status not in {"like", "ignore", "offline", "candidate"}:
                raise Exception('FUHHH')

            if listing in self.listing_status_map:
                if self.listing_status_map[listing]['status'] != 'unseen':
                    assert self.listing_status_map[listing]['status'] == status
            self.listing_status_map[listing] = {'status': status}
        else:
            raise Exception('uh oh')

    def iterate_through_liked(self):
        for listing in self.listing_status_map:
            info = self.listing_status_map[listing]
            if info['status'] == 'like':
                yield listing, info

    def attach_contact_status_to_liked(self):
        for listing in self.listing_status_map:
            info = self.listing_status_map[listing]
            if info['status'] != 'like':
                continue
            for d, value in self.defaults.items():
                if d not in info:
                    info[d] = value

    def show_missing_info(self):
        for listing, info in self.iterate_through_liked():
            found_missing_info = False
            for key, value in self.defaults.items():
                if key == 'contacted':
                    continue
                if info[key] == value:
                    if not found_missing_info:
                        print(listing)
                    found_missing_info = True
                    print('Need to fix ' + key)

    def generate_consolidating_listing_file(self):
        self.attach_contact_status_to_liked()
        path = os.path.join(self.main_folder, 'listings.json')
        with open(path, 'w') as f:
            json.dump(self.listing_status_map, indent=4, sort_keys=True, fp=f)

    def get_info_string(self, listing):
        string = '{0} {1} {2} TJ: {3}, TGT: {4}'
        info = self.listing_status_map[listing]
        string = string.format(listing, info['floor'], info['rent'], info['trader-joes'], info['target'])
        return string

    def generate_listings_by_area_and_rent(self):
        culver_city, sawtelle = [], []
        for listing in self.listing_status_map:
            info = self.listing_status_map[listing]
            if info['status'] != 'like':
                continue
            if info['rent'] == 0:
                raise Exception('zero rent for ' + listing)
            area = info['area']
            if area == 'culver city':
                culver_city.append(listing)
            elif area == 'sawtelle':
                sawtelle.append(listing)
            else:
                raise Exception('NOOOO')
        culver_city.sort(key=lambda x: x[2])
        sawtelle.sort(key=lambda x: x[2])
        print('Culver City apartments')
        print("\n".join([self.get_info_string(i) for i in culver_city]))
        print('\nSawtelle Apartments')
        print("\n".join([self.get_info_string(i) for i in sawtelle]))
        print(len(culver_city) + len(sawtelle))


if __name__ == '__main__':
    z = ZillowAnalyzer('assets')
    z.process_input_file()
    z.generate_consolidating_listing_file()
    count = z.print_unseen_listings()
    if count > 0:
        raise Exception('')
    z.attach_contact_status_to_liked()
    # z.print_liked_listings()
    # z.print_liked_listings_with_unknown_pet_status()
    z.generate_listings_by_area_and_rent()
    # z.show_missing_info()