import os
import time
import json
# Start time counter
start_time = time.time()

# Read the URLs and city names from the JSON file
with open('urls_delegaciones.json', 'r') as urls_file:
    urls_data = json.load(urls_file)

# Lista de scripts a ejecutar
script_files = ['demo.py', 'pdf_csv.py', 'merge_csv.py']

# Create a dictionary to store the results for each delegacion
results = {}
for city, url in urls_data.items():
    # Execute each link.py script for the URL
    # The script will save the results as a JSON file
    os.system(f'python links.py "{url}"')
    with open('urls.json', 'r') as urls_file:
        urls_data = json.load(urls_file)
        results[city] = urls_data

    # Execute demo.py script with the city name

    os.system(f'python demo.py "{city}"')
    # Execute pdf_csv.py script with the city name
    os.system(f'python pdf_csv.py "{city}"')
    # Execute merge_csv.py script
    os.system(f'python merge_csv.py')
    # Execute merge_csv.py script
    os.system(f'python merge_csv.py')


# Save the overall results as a JSON file
with open('overall_results.json', 'w') as overall_results_file:
    json.dump(results, overall_results_file, indent=4)

# End time counter
end_time = time.time()

# Date and time when the script started and finished
start_date = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(start_time))
end_date = time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(end_time))

# Total time taken in a txt file
with open('time_taken.txt', 'w') as time_taken_file:
    time_taken_file.write(f'Total time taken: {end_time - start_time} seconds')
    time_taken_file.write(f'Start time: {start_date}')
    time_taken_file.write(f'End time: {end_date}')