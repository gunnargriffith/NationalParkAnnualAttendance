#Copy of just the scrapper and file creation code for the package


def run_scraper():
    import os
    import pandas as pd
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    import glob
    import shutil
    import requests
    from dotenv import load_dotenv

    # Load environment variables from .env
    load_dotenv()
    api_key = os.getenv('API_KEY')

    url = "https://developer.nps.gov/api/v1/parks"
    params = {
        'api_key': api_key,
        'limit': 496
    }
    r = requests.get(url, params=params)
    data = r.json()

    #Check status code
    if r.status_code != 200:
        print(f"Error: Received status code {r.status_code}")

    #Make the df as needed
    df = pd.json_normalize(data['data'])
    df = df[df['fullName'].str.contains("National Park")]
    df = df[df['parkCode'] != 'npnh'] #Not a park, but a collection of sites (NO POPULATION)
    df = df[df['parkCode'] != 'seki'] #Not a park, but a collection of sites (NO POPULATION)

    CSVDictionary = {}

    #The park codes from df
    park_codes = []
    for code in df['parkCode']:
        park_codes.append(code.upper())



    for park_code in park_codes:
        print(f"Processing {park_code}...")
        
        # 1. Setup portable download folder
        download_dir = os.path.join(os.getcwd(), "downloads")
        os.makedirs(download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        prefs = {
            "download.default_directory": download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True
        }
        options.add_experimental_option("prefs", prefs)

        # IMPORTANT: only create driver ONCE
        driver = webdriver.Chrome(options=options)

        # 2. Open page
        url = f"https://irma.nps.gov/Stats/SSRSReports/Park%20Specific%20Reports/Annual%20Park%20Recreation%20Visitation%20(1904%20-%20Last%20Calendar%20Year)?Park={park_code}"
        driver.get(url)

        time.sleep(5)

        # 3. Find CSV button in iframes
        iframes = driver.find_elements(By.TAG_NAME, "iframe")

        clicked = False

        for i, frame in enumerate(iframes):
            driver.switch_to.frame(frame)

            try:
                csv_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'CSV')]"))
                )

                driver.execute_script("arguments[0].click();", csv_link)

                print(f"Clicked CSV in iframe {i}")
                clicked = True
                break

            except:
                driver.switch_to.default_content()

        driver.switch_to.default_content()

        
        # 4. Wait for download to finish
        timeout = 25
        start = time.time()

        latest_file = None

        while time.time() - start < timeout:
            files = glob.glob(os.path.join(download_dir, "*.csv"))
            if files:
                latest_file = max(files, key=os.path.getmtime)
                break
            time.sleep(1)

        
        # 5. Rename the downloaded file to park-specific name
        new_file_path = os.path.join(download_dir, f"{park_code}.csv")
        shutil.move(latest_file, new_file_path)

        driver.quit()

        # 6. Load CSV safely
        df = pd.read_csv(
            new_file_path,
            skiprows=3   # skips Title + blank lines
        )

        # clean numbers
        df["RecreationVisitors"] = (
            df["RecreationVisitors"].str.replace(",", "").astype(int)
        )

        CSVDictionary[park_code] = df

        # delete file
        file_path = os.path.join(download_dir, f"{park_code}.csv")

        os.remove(file_path)


    from pathlib import Path
    import json

    # Create path to data folder
    data_path = Path("data")
    data_path.mkdir(exist_ok=True)  # ensures folder exists

    # Save dataframe
    df.to_csv(data_path / "parks_df.csv", index=False)

    # Convert dictionary safely
    safe_dict = {
        k: v.to_dict(orient="records")
        for k, v in CSVDictionary.items()
    }

    # Save dictionary
    with open(data_path / "csv_dictionary.json", "w") as f:
        json.dump(safe_dict, f, indent=4)



    return df, CSVDictionary



#run_scraper()