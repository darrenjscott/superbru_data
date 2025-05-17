import requests
import time

# Returns a list of competitions you can search through
def get_comps(config):
    base_api_url = config["base_api_url"]
    headers = config["api_headers"]

    # Get list of all competitions
    # We need the 'id' to pull fixtures
    url_comps = base_api_url + 'competitions.json'
    querystring_comps = {"include":"rounds"}
    
    response = requests.get(url_comps,
                            headers=headers, 
                            params=querystring_comps)
    comps_json = response.json()
    comps_list = comps_json["competitions"]
    return comps_list


# Gets the matches which were played in a particular competition
def get_fixtures(comp_id, config):
    base_api_url = config["base_api_url"]
    headers = config["api_headers"]

    url_fixtures = base_api_url + 'fixtures-results.json'
    querystring_fixtures = {"comp": comp_id}
    response = requests.get(url_fixtures,
                            headers=headers,
                            params=querystring_fixtures)
    fixtures = response.json()
    return fixtures["fixtures-results"]["matches"]




# This works in stages. We first have to get the competiton ID, then pull the
# matches from there
def get_matches(config):
    # Get correct competition details
    competition_name = "scottish premiership"
    competitions_list = get_comps(config) 
    scottish_prem_comp = [comp for comp in competitions_list
                          if comp['generic-name'].lower() == competition_name]
    
    # scottish_prem_comp also contains keys
    # ('generic-name', 'id', 'type', 'full-name')
    scotprem_id = scottish_prem_comp[0]["id"]
    
    # Pull the fixtures (this is a list of matches)
    fixtures = get_fixtures(scotprem_id, config)

    # Get all matches in the Scottish premier league
    base_api_url = config["base_api_url"]
    url_matches = base_api_url + "match.json"
    headers = config["api_headers"]

    match_details = dict()
    num_fixtures = len(fixtures)
    for idx, fixture in enumerate(fixtures):
        fix_id = fixture['id']
        querystring = {"match": fix_id}
        response = requests.get(url_matches,
                                headers=headers,
                                params=querystring)
        specific_match_json = response.json()
        match_details[fix_id] = specific_match_json
        if idx >= 12:
            break

        # Slow this down due to the rate limit of API calls
        print(f"Extracted {idx+1} of {num_fixtures} matches.")
        time.sleep(3)

    return match_details
