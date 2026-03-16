#!/usr/bin/env python3
"""
Generate 2026 NCAA Tournament seed entries for MNCAATourneySeeds.csv and WNCAATourneySeeds.csv.
Maps team names to Kaggle TeamIDs using MTeams.csv, WTeams.csv, and spelling files.
"""

import csv
import os

BASE_DIR = "/Users/prince/Developer/Personal/MarchMadness/march-machine-learning-mania-2026"

def load_teams(filepath):
    """Load TeamID -> TeamName mapping from MTeams.csv or WTeams.csv."""
    teams = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            tid = int(row['TeamID'])
            teams[tid] = row['TeamName']
    return teams

def load_spellings(filepath):
    """Load alternate spellings -> TeamID mapping."""
    spellings = {}
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            spelling = row['TeamNameSpelling'].strip().lower()
            tid = int(row['TeamID'])
            spellings[spelling] = tid
    return spellings

def build_name_to_id(teams, spellings):
    """Build a comprehensive name -> TeamID lookup."""
    lookup = {}
    # Add official names (lowercase)
    for tid, name in teams.items():
        lookup[name.lower()] = tid
    # Add all alternate spellings
    for spelling, tid in spellings.items():
        lookup[spelling] = tid
    return lookup

def find_team_id(name, lookup, label=""):
    """Find a TeamID for a given team name, trying various transformations."""
    # Direct lookup
    key = name.strip().lower()
    if key in lookup:
        return lookup[key]

    # Common transformations to try
    alternatives = [
        key,
        key.replace("'", "'"),
        key.replace("'", "`"),
        key.replace(" ", "-"),
        key.replace(".", ""),
        key.replace("st.", "st"),
        key.replace("state", "st"),
    ]

    for alt in alternatives:
        if alt in lookup:
            return lookup[alt]

    return None

def main():
    # Load men's data
    m_teams = load_teams(os.path.join(BASE_DIR, "MTeams.csv"))
    m_spellings = load_spellings(os.path.join(BASE_DIR, "MTeamSpellings.csv"))
    m_lookup = build_name_to_id(m_teams, m_spellings)

    # Load women's data
    w_teams = load_teams(os.path.join(BASE_DIR, "WTeams.csv"))
    w_spellings = load_spellings(os.path.join(BASE_DIR, "WTeamSpellings.csv"))
    w_lookup = build_name_to_id(w_teams, w_spellings)

    # =========================================================================
    # MEN'S TOURNAMENT - 2026
    # Region letters: W=East(region1), X=West(region2), Y=South(region3), Z=Midwest(region4)
    # Based on examining historical data patterns
    # =========================================================================

    # Map of user-provided team name -> lookup key (for names that need manual mapping)
    men_name_map = {
        "Duke": "duke",
        "UConn": "uconn",
        "Michigan State": "michigan state",
        "Kansas": "kansas",
        "St. John's": "st john's",
        "Louisville": "louisville",
        "UCLA": "ucla",
        "Ohio State": "ohio state",
        "TCU": "tcu",
        "UCF": "ucf",
        "South Florida": "south florida",
        "Northern Iowa": "northern iowa",
        "Cal Baptist": "cal baptist",
        "North Dakota State": "north dakota state",
        "Furman": "furman",
        "Siena": "siena",
        # Midwest
        "Michigan": "michigan",
        "Iowa State": "iowa state",
        "Virginia": "virginia",
        "Alabama": "alabama",
        "Texas Tech": "texas tech",
        "Tennessee": "tennessee",
        "Kentucky": "kentucky",
        "Georgia": "georgia",
        "Saint Louis": "saint louis",
        "Santa Clara": "santa clara",
        "Miami (OH)": "miami (oh)",
        "SMU": "smu",
        "Akron": "akron",
        "Hofstra": "hofstra",
        "Wright State": "wright state",
        "Tennessee State": "tennessee state",
        "UMBC": "umbc",
        "Howard": "howard",
        # West
        "Arizona": "arizona",
        "Purdue": "purdue",
        "Gonzaga": "gonzaga",
        "Arkansas": "arkansas",
        "Wisconsin": "wisconsin",
        "BYU": "byu",
        "Miami (FL)": "miami (fl)",
        "Villanova": "villanova",
        "Utah State": "utah state",
        "Missouri": "missouri",
        "Texas": "texas",
        "NC State": "nc state",
        "High Point": "high point",
        "Hawaii": "hawaii",
        "Kennesaw State": "kennesaw state",
        "Queens": "queens (nc)",
        "LIU": "liu",
        # South
        "Florida": "florida",
        "Houston": "houston",
        "Illinois": "illinois",
        "Nebraska": "nebraska",
        "Vanderbilt": "vanderbilt",
        "North Carolina": "north carolina",
        "Saint Mary's": "saint mary's",
        "Clemson": "clemson",
        "Iowa": "iowa",
        "Texas A&M": "texas a&m",
        "VCU": "vcu",
        "McNeese": "mcneese",
        "Troy": "troy",
        "Penn": "penn",
        "Idaho": "idaho",
        "Prairie View A&M": "prairie view a&m",
        "Lehigh": "lehigh",
    }

    # Define the bracket: (region_letter, seed_num, team_name)
    # W = East, X = West, Y = South, Z = Midwest
    men_seeds = []

    # EAST REGION (W)
    east_teams = [
        (1, "Duke"), (2, "UConn"), (3, "Michigan State"), (4, "Kansas"),
        (5, "St. John's"), (6, "Louisville"), (7, "UCLA"), (8, "Ohio State"),
        (9, "TCU"), (10, "UCF"), (11, "South Florida"), (12, "Northern Iowa"),
        (13, "Cal Baptist"), (14, "North Dakota State"), (15, "Furman"), (16, "Siena"),
    ]
    for seed, team in east_teams:
        men_seeds.append(("W", f"{seed:02d}", team))

    # MIDWEST REGION (Z)
    midwest_teams = [
        (1, "Michigan"), (2, "Iowa State"), (3, "Virginia"), (4, "Alabama"),
        (5, "Texas Tech"), (6, "Tennessee"), (7, "Kentucky"), (8, "Georgia"),
        (9, "Saint Louis"), (10, "Santa Clara"),
    ]
    for seed, team in midwest_teams:
        men_seeds.append(("Z", f"{seed:02d}", team))
    # Play-in games
    men_seeds.append(("Z", "11a", "Miami (OH)"))
    men_seeds.append(("Z", "11b", "SMU"))
    midwest_teams2 = [
        (12, "Akron"), (13, "Hofstra"), (14, "Wright State"), (15, "Tennessee State"),
    ]
    for seed, team in midwest_teams2:
        men_seeds.append(("Z", f"{seed:02d}", team))
    men_seeds.append(("Z", "16a", "UMBC"))
    men_seeds.append(("Z", "16b", "Howard"))

    # WEST REGION (X)
    west_teams = [
        (1, "Arizona"), (2, "Purdue"), (3, "Gonzaga"), (4, "Arkansas"),
        (5, "Wisconsin"), (6, "BYU"), (7, "Miami (FL)"), (8, "Villanova"),
        (9, "Utah State"), (10, "Missouri"),
    ]
    for seed, team in west_teams:
        men_seeds.append(("X", f"{seed:02d}", team))
    men_seeds.append(("X", "11a", "Texas"))
    men_seeds.append(("X", "11b", "NC State"))
    west_teams2 = [
        (12, "High Point"), (13, "Hawaii"), (14, "Kennesaw State"), (15, "Queens"),
    ]
    for seed, team in west_teams2:
        men_seeds.append(("X", f"{seed:02d}", team))
    men_seeds.append(("X", "16", "LIU"))

    # SOUTH REGION (Y)
    south_teams = [
        (1, "Florida"), (2, "Houston"), (3, "Illinois"), (4, "Nebraska"),
        (5, "Vanderbilt"), (6, "North Carolina"), (7, "Saint Mary's"),
        (8, "Clemson"), (9, "Iowa"), (10, "Texas A&M"), (11, "VCU"),
        (12, "McNeese"), (13, "Troy"), (14, "Penn"), (15, "Idaho"),
    ]
    for seed, team in south_teams:
        men_seeds.append(("Y", f"{seed:02d}", team))
    men_seeds.append(("Y", "16a", "Prairie View A&M"))
    men_seeds.append(("Y", "16b", "Lehigh"))

    # =========================================================================
    # WOMEN'S TOURNAMENT - 2026
    # =========================================================================

    women_name_map = {
        "UConn": "uconn",
        "Vanderbilt": "vanderbilt",
        "Ohio State": "ohio state",
        "North Carolina": "north carolina",
        "Maryland": "maryland",
        "Notre Dame": "notre dame",
        "Illinois": "illinois",
        "Iowa State": "iowa state",
        "Syracuse": "syracuse",
        "Colorado": "colorado",
        "Fairfield": "fairfield",
        "Murray State": "murray state",
        "Western Illinois": "western illinois",
        "Howard": "howard",
        "High Point": "high point",
        "UTSA": "utsa",
        # Region 2
        "UCLA": "ucla",
        "LSU": "lsu",
        "Duke": "duke",
        "Minnesota": "minnesota",
        "Ole Miss": "ole miss",
        "Baylor": "baylor",
        "Texas Tech": "texas tech",
        "Oklahoma State": "oklahoma state",
        "Princeton": "princeton",
        "Villanova": "villanova",
        "Nebraska": "nebraska",
        "Richmond": "richmond",
        "Gonzaga": "gonzaga",
        "Green Bay": "green bay",
        "Charleston": "charleston",
        "Jacksonville": "jacksonville",
        "California Baptist": "california baptist",
        # Region 3
        "Texas": "texas",
        "Michigan": "michigan",
        "Louisville": "louisville",
        "West Virginia": "west virginia",
        "Kentucky": "kentucky",
        "Alabama": "alabama",
        "North Carolina State": "nc state",
        "Oregon": "oregon",
        "Virginia Tech": "virginia tech",
        "Tennessee": "tennessee",
        "Rhode Island": "rhode island",
        "James Madison": "james madison",
        "Miami (OH)": "miami (oh)",
        "Vermont": "vermont",
        "Holy Cross": "holy cross",
        "Missouri State": "missouri state",
        "SF Austin": "sf austin",
        # Region 4
        "South Carolina": "south carolina",
        "Iowa": "iowa",
        "TCU": "tcu",
        "Oklahoma": "oklahoma",
        "Michigan State": "michigan state",
        "Washington": "washington",
        "Georgia": "georgia",
        "Clemson": "clemson",
        "USC": "usc",
        "Virginia": "virginia",
        "Arizona State": "arizona state",
        "South Dakota State": "south dakota state",
        "Colorado State": "colorado state",
        "Idaho": "idaho",
        "UC San Diego": "uc san diego",
        "Fairleigh Dickinson": "fairleigh dickinson",
        "Southern": "southern",
        "Samford": "samford",
    }

    women_seeds = []

    # REGION 1 (W)
    r1_teams = [
        (1, "UConn"), (2, "Vanderbilt"), (3, "Ohio State"), (4, "North Carolina"),
        (5, "Maryland"), (6, "Notre Dame"), (7, "Illinois"), (8, "Iowa State"),
        (9, "Syracuse"), (10, "Colorado"), (11, "Fairfield"), (12, "Murray State"),
        (13, "Western Illinois"), (14, "Howard"), (15, "High Point"), (16, "UTSA"),
    ]
    for seed, team in r1_teams:
        women_seeds.append(("W", f"{seed:02d}", team))

    # REGION 2 (X)
    r2_teams = [
        (1, "UCLA"), (2, "LSU"), (3, "Duke"), (4, "Minnesota"),
        (5, "Ole Miss"), (6, "Baylor"), (7, "Texas Tech"), (8, "Oklahoma State"),
        (9, "Princeton"), (10, "Villanova"),
    ]
    for seed, team in r2_teams:
        women_seeds.append(("X", f"{seed:02d}", team))
    women_seeds.append(("X", "11a", "Nebraska"))
    women_seeds.append(("X", "11b", "Richmond"))
    r2_teams2 = [
        (12, "Gonzaga"), (13, "Green Bay"), (14, "Charleston"), (15, "Jacksonville"),
        (16, "California Baptist"),
    ]
    for seed, team in r2_teams2:
        women_seeds.append(("X", f"{seed:02d}", team))

    # REGION 3 (Y)
    r3_teams = [
        (1, "Texas"), (2, "Michigan"), (3, "Louisville"), (4, "West Virginia"),
        (5, "Kentucky"), (6, "Alabama"), (7, "North Carolina State"), (8, "Oregon"),
        (9, "Virginia Tech"), (10, "Tennessee"), (11, "Rhode Island"),
        (12, "James Madison"), (13, "Miami (OH)"), (14, "Vermont"), (15, "Holy Cross"),
    ]
    for seed, team in r3_teams:
        women_seeds.append(("Y", f"{seed:02d}", team))
    women_seeds.append(("Y", "16a", "Missouri State"))
    women_seeds.append(("Y", "16b", "SF Austin"))

    # REGION 4 (Z)
    r4_teams = [
        (1, "South Carolina"), (2, "Iowa"), (3, "TCU"), (4, "Oklahoma"),
        (5, "Michigan State"), (6, "Washington"), (7, "Georgia"), (8, "Clemson"),
        (9, "USC"),
    ]
    for seed, team in r4_teams:
        women_seeds.append(("Z", f"{seed:02d}", team))
    women_seeds.append(("Z", "10a", "Virginia"))
    women_seeds.append(("Z", "10b", "Arizona State"))
    r4_teams2 = [
        (11, "South Dakota State"), (12, "Colorado State"), (13, "Idaho"),
        (14, "UC San Diego"), (15, "Fairleigh Dickinson"),
    ]
    for seed, team in r4_teams2:
        women_seeds.append(("Z", f"{seed:02d}", team))
    women_seeds.append(("Z", "16a", "Southern"))
    women_seeds.append(("Z", "16b", "Samford"))

    # =========================================================================
    # Resolve all team IDs
    # =========================================================================

    print("=" * 60)
    print("MEN'S TOURNAMENT - Resolving Team IDs")
    print("=" * 60)

    men_rows = []
    men_unmatched = []
    for region, seed, team in men_seeds:
        lookup_key = men_name_map.get(team, team.lower())
        tid = find_team_id(lookup_key, m_lookup, team)
        if tid is None:
            # Try the original team name directly
            tid = find_team_id(team, m_lookup, team)
        if tid is not None:
            seed_str = f"{region}{seed}"
            men_rows.append(f"2026,{seed_str},{tid}")
            print(f"  MATCHED: {team:30s} -> TeamID {tid} (Seed {region}{seed})")
        else:
            men_unmatched.append((region, seed, team))
            print(f"  *** UNMATCHED: {team} (Seed {region}{seed})")

    print()
    print("=" * 60)
    print("WOMEN'S TOURNAMENT - Resolving Team IDs")
    print("=" * 60)

    women_rows = []
    women_unmatched = []
    for region, seed, team in women_seeds:
        lookup_key = women_name_map.get(team, team.lower())
        tid = find_team_id(lookup_key, w_lookup, team)
        if tid is None:
            tid = find_team_id(team, w_lookup, team)
        if tid is not None:
            seed_str = f"{region}{seed}"
            women_rows.append(f"2026,{seed_str},{tid}")
            print(f"  MATCHED: {team:30s} -> TeamID {tid} (Seed {region}{seed})")
        else:
            women_unmatched.append((region, seed, team))
            print(f"  *** UNMATCHED: {team} (Seed {region}{seed})")

    # =========================================================================
    # Summary
    # =========================================================================
    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Men's: {len(men_rows)} matched, {len(men_unmatched)} unmatched")
    print(f"Women's: {len(women_rows)} matched, {len(women_unmatched)} unmatched")

    if men_unmatched:
        print("\nMen's Unmatched Teams:")
        for region, seed, team in men_unmatched:
            print(f"  {region}{seed}: {team}")

    if women_unmatched:
        print("\nWomen's Unmatched Teams:")
        for region, seed, team in women_unmatched:
            print(f"  {region}{seed}: {team}")

    # =========================================================================
    # Append to CSV files
    # =========================================================================
    if men_rows:
        men_csv = os.path.join(BASE_DIR, "MNCAATourneySeeds.csv")
        with open(men_csv, 'r') as f:
            existing = f.read()
        # Check if 2026 data already exists
        if "2026," in existing:
            print("\nWARNING: 2026 data already exists in MNCAATourneySeeds.csv. Removing old 2026 entries first.")
            lines = existing.strip().split('\n')
            lines = [l for l in lines if not l.startswith("2026,")]
            existing = '\n'.join(lines) + '\n'

        with open(men_csv, 'w') as f:
            f.write(existing.rstrip('\n') + '\n')
            for row in men_rows:
                f.write(row + '\n')
        print(f"\nAppended {len(men_rows)} men's seed entries to {men_csv}")

    if women_rows:
        women_csv = os.path.join(BASE_DIR, "WNCAATourneySeeds.csv")
        with open(women_csv, 'r') as f:
            existing = f.read()
        if "2026," in existing:
            print("\nWARNING: 2026 data already exists in WNCAATourneySeeds.csv. Removing old 2026 entries first.")
            lines = existing.strip().split('\n')
            lines = [l for l in lines if not l.startswith("2026,")]
            existing = '\n'.join(lines) + '\n'

        with open(women_csv, 'w') as f:
            f.write(existing.rstrip('\n') + '\n')
            for row in women_rows:
                f.write(row + '\n')
        print(f"Appended {len(women_rows)} women's seed entries to {women_csv}")

    # =========================================================================
    # Verify output
    # =========================================================================
    print()
    print("=" * 60)
    print("VERIFICATION - Men's 2026 Seeds")
    print("=" * 60)
    for row in men_rows:
        parts = row.split(',')
        tid = int(parts[2])
        name = m_teams.get(tid, "UNKNOWN")
        print(f"  {parts[1]:6s} -> {name} (ID: {tid})")

    print()
    print("=" * 60)
    print("VERIFICATION - Women's 2026 Seeds")
    print("=" * 60)
    for row in women_rows:
        parts = row.split(',')
        tid = int(parts[2])
        name = w_teams.get(tid, "UNKNOWN")
        print(f"  {parts[1]:6s} -> {name} (ID: {tid})")

if __name__ == "__main__":
    main()
