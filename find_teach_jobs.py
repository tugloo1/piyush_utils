import requests
import datetime

region_loader_url = 'https://www.edjoin.org/Home/LoadSearchRegions?states=24'
filter_county_names = {"Los Angeles": 19, "Orange": 30}



class FindTeachingJobs(object):
    def __init__(self, input_regions):
        self.input_regions = input_regions
        self.output_ds = {region: {} for region in self.input_regions}

    def get_regions_available(self):
        response = requests.get(region_loader_url)
        data = response.json()['data']
        to_return = []
        for county in data:
            if county["countyName"] in filter_county_names:
                to_return.append(county)
        return to_return

    def get_districts(self, county_id):
        organizations_url = 'https://www.edjoin.org/Home/LoadDistricts?countyID=' + str(county_id)
        organizations = requests.get(organizations_url)
        to_return = organizations.json()['data']
        return to_return

    def get_job_links_for_district(self, district_id, num_of_jobs):
        job_search_url = 'https://www.edjoin.org/Home/LoadJobs?rows=10&page={0}&sort=postingDate&order=DESC&keywords=&searchType=&states=&regions=&jobTypes=&days=0&catID=0&onlineApps=false&recruitmentCenterID=0&stateID=0&regionID=0&districtID={1}&countyID=0&searchID=0'
        page = 1
        jobs = []
        while num_of_jobs > 0:
            response = requests.get(job_search_url.format(str(page), str(district_id)))
            data_output = response.json()["data"]
            jobs += data_output
            num_of_jobs = num_of_jobs - 10
            page += 1
        return jobs

    def process_ed_join(self):
        for region, region_id in self.input_regions.items():
            districts = self.get_districts(region_id)
            for district in districts:
                district_name = district["districtName"]
                district_id = district["districtID"]
                print("Processing " + district_name)
                self.output_ds[region][district_name] = {}
                job_links = self.get_job_links_for_district(district_id, district["numberPostings"])
                for job_link in job_links:
                    postingID, job_title= job_link["postingID"], job_link["positionTitle"]
                    self.output_ds[region][district_name][postingID] = job_title

    def do_the_thing(self):
        self.process_ed_join()
        lines = []
        for region, region_details in self.output_ds.items():
            lines.append("Job Postings for {0} County".format(region))
            for district_name, job_posting_dict in region_details.items():
                lines.append("\t" + district_name)
                for job_posting_id, job_posting_title in job_posting_dict.items():
                    lines.append("\t\thttps://www.edjoin.org/Home/DistrictJobPosting/{0} -> {1}".format(job_posting_id, job_posting_title))
        print("\n".join(lines))
        now = datetime.datetime.now()
        file_name = "job-results-{0}-{1}-{2}-{3}-{4}.txt".format(now.year, now.month, now.day, now.hour, now.minute)
        with open(file_name, 'w') as f:
            f.writelines("\n".join(lines))
        print("Done writing to " + file_name)



if __name__ == '__main__':
    #filter_county_names = {"Los Angeles": 19, "Orange": 30}
    filter_county_names = {"Orange": 30}
    FindTeachingJobs(filter_county_names).do_the_thing()
