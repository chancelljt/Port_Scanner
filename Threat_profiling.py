import json

def load_threat_feed_database(file_path):
    try:
        with open(file_path, 'r') as file:
            threat_db = [json.loads(line) for line in file]
        return threat_db
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Unable to parse the data in '{file_path}'.")
        return []

def generate_threat_summary(threat_db):
    attack_types_count = {}
    attacking_countries_count = {}
    victim_countries_count = {}

    for entry in threat_db:
        attack_type = entry['attack_type']
        attacking_country = entry['attacking_country']
        victim_country = entry['victim_country']

        # Count attack types
        attack_types_count[attack_type] = attack_types_count.get(attack_type, 0) + 1

        # Count attacking countries
        attacking_countries_count[attacking_country] = attacking_countries_count.get(attacking_country, 0) + 1

        # Count victim countries
        victim_countries_count[victim_country] = victim_countries_count.get(victim_country, 0) + 1

    # Sort the dictionaries by the count in descending order
    sorted_attack_types = sorted(attack_types_count.items(), key=lambda x: x[1], reverse=True)
    sorted_attacking_countries = sorted(attacking_countries_count.items(), key=lambda x: x[1], reverse=True)
    sorted_victim_countries = sorted(victim_countries_count.items(), key=lambda x: x[1], reverse=True)

    return sorted_attack_types, sorted_attacking_countries, sorted_victim_countries

pass

def main():
    # Load the threat feed database from the file
    threat_db = load_threat_feed_database('threat_intel_db.txt')
    print(threat_db)  # Add this line to check the data

    # Check if threat_db is not empty
    if threat_db:
        # Generate the threat summary
        attack_types_summary, attacking_countries_summary, victim_countries_summary = generate_threat_summary(threat_db)

        # Print the summary
        print("----- Threat Summary -----")
        print("Most Common Attack Types:")
        for attack_type, count in attack_types_summary[:5]:  # Display the top 5 attack types
            print(f"{attack_type}: {count} occurrences")

        print("\nTop Attacking Countries:")
        for country, count in attacking_countries_summary[:5]:  # Display the top 5 attacking countries
            print(f"{country}: {count} attacks")

        print("\nMost Targeted Victim Countries:")
        for country, count in victim_countries_summary[:5]:  # Display the top 5 victim countries
            print(f"{country}: {count} attacks")
    else:
        print("Error: Unable to load the threat feed database.")

if __name__ == "__main__":
    main()