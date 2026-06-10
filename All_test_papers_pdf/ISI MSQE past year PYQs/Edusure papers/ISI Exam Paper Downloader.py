import os
import asyncio
import aiohttp
import aiofiles

# Data containing the file information
# Some solution links are marked as 'None' because they were not available on the website.
papers_data = [
    {
        "year": "1998",
        "paper_name": "ISI 1998 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1RtRENaj-QHYNEZ2ZCvijQ1TNWhWCfAUr",
        "solution_name": "Solution ISI 1998 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "1999",
        "paper_name": "ISI 1999 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1prLmEnL22pKS_uIskjIfws2MWXQnNrOi",
        "solution_name": "Solution ISI 1999 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2000",
        "paper_name": "ISI 2000 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1FJNx7-TAesCIfedSdu8swKD5kGlJ9B0t",
        "solution_name": "Solution ISI 2000 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2001",
        "paper_name": "ISI 2001 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1GCqIJhLfN7srW_lBUWcQVVfe8P9qYlyP",
        "solution_name": "Solution ISI 2001 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2002",
        "paper_name": "ISI 2002 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=11Qou1k8oHmGZUvYHqw-VM9mtruiNouZu",
        "solution_name": "Solution ISI 2002 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2003",
        "paper_name": "ISI 2003 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1I3jDx9evfhlxC0HFpvS_tLfLYkwADoWa",
        "solution_name": "Solution ISI 2003 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2004",
        "paper_name": "ISI 2004 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1o04vkcK9bf9PVqV0LSfQmkKroaDlCo6U",
        "solution_name": "Solution ISI 2004 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2005",
        "paper_name": "ISI 2005 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=13gd2hfT5J5YLqdFPzLFKhoP0w21VEptX",
        "solution_name": "Solution ISI 2005 Paper.pdf",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/11/ISI-2005.pdf",
    },
    {
        "year": "2006",
        "paper_name": "ISI 2006 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=12jVLLpeKd7hfTV1jjr-EONaLbX47XFXg",
        "solution_name": "Solution ISI 2006 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2007",
        "paper_name": "ISI 2007 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1z39tjS_3zBkvJfXGFS9UMukZ3Uemgosn",
        "solution_name": "Solution ISI 2007 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2007.jpg",
    },
    {
        "year": "2008",
        "paper_name": "ISI 2008 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1fTSeBhv4v5opOOo19VlgGqAoPdeCKd1B",
        "solution_name": "Solution ISI 2008 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2008.jpg",
    },
    {
        "year": "2009",
        "paper_name": "ISI 2009 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1ZQ2tJvXaO9eDIS4tq4TA3cBLGvLAhE4v",
        "solution_name": "Solution ISI 2009 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2009.jpg",
    },
    {
        "year": "2010",
        "paper_name": "ISI 2010 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1dCvxCqZ5W1p1-bfaUXAf88Que8i97zX4",
        "solution_name": "Solution ISI 2010 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2010.jpg",
    },
    {
        "year": "2011",
        "paper_name": "ISI 2011 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1M6BDbzOxVA1xofDXQvF7BmsRzW4MCVF9",
        "solution_name": "Solution ISI 2011 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2011.jpg",
    },
    {
        "year": "2012",
        "paper_name": "ISI 2012 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1qOOJoQh5r3c-HavMylGFkpb1O1QVHtk3",
        "solution_name": "Solution ISI 2012 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2012.jpg",
    },
    {
        "year": "2013",
        "paper_name": "ISI 2013 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1VULhrSOO2gCA8YLnOqeWQlaI0vwidD-_",
        "solution_name": "Solution ISI 2013 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2013.jpg",
    },
    {
        "year": "2014",
        "paper_name": "ISI 2014 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1IVL33iUtWFYBGrnI1iFuYb8KQykcsy15",
        "solution_name": "Solution ISI 2014 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2014.jpg",
    },
    {
        "year": "2015",
        "paper_name": "ISI 2015 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1Q-jtM6vhFlwmia5m0sVmnq4MXw_M3nnh",
        "solution_name": "Solution ISI 2015 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2015.jpg",
    },
    {
        "year": "2016",
        "paper_name": "ISI 2016 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1IUSOhqVAkkloWDRgD4EeC1nLu7IWGEP_",
        "solution_name": "Solution ISI 2016 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2016.jpg",
    },
    {
        "year": "2017",
        "paper_name": "ISI 2017 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1YnDoXEPHKRoMOPVZarXajGXucBlwDtnG",
        "solution_name": "Solution ISI 2017 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2017.jpg",
    },
    {
        "year": "2018",
        "paper_name": "ISI 2018 Paper.pdf",
        "paper_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2018-1.pdf",
        "solution_name": "Solution ISI 2018 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2018.jpg",
    },
    {
        "year": "2019",
        "paper_name": "ISI 2019 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1w0132yxYVSkL3ZDWqVL5C2AYAi89ErFe",
        "solution_name": "Solution ISI 2019 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2019.jpg",
    },
    {
        "year": "2020",
        "paper_name": "ISI 2020 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1moErUt3XlpPplg-hh8MmVT7xZwxLfPEs",
        "solution_name": "Solution ISI 2020 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2020.jpg",
    },
    {
        "year": "2021",
        "paper_name": "ISI 2021 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1MEuc7ux6_lu-lkLkRUGjw2FbhErNA90V",
        "solution_name": "Solution ISI 2021 Paper.jpg",
        "solution_url": "https://edusure.in/wp-content/uploads/2022/10/ISI-2021.jpg",
    },
    {
        "year": "2023",
        "paper_name": "ISI 2023 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1JwFbPO05cj8t5d1FaBzeYaBlGfNFDCoQ",
        "solution_name": "Solution ISI 2023 Paper.pdf",
        "solution_url": "https://drive.google.com/uc?export=download&id=1YEbzZfm8R5iBh4hX9ppFnsdY6SK599V",
    },
    {
        "year": "2024",
        "paper_name": "ISI 2024 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1eaocXqkvqDGWa89jZ90LlfJDMjIEYefk",
        "solution_name": "Solution ISI 2024 Paper.pdf",
        "solution_url": None,
    },
    {
        "year": "2025",
        "paper_name": "ISI 2025 Paper.pdf",
        "paper_url": "https://drive.google.com/uc?export=download&id=1ofU2b5OkiM-5wImvcjSW2pr5QiRUqBk9",
        "solution_name": "Solution ISI 2025 Paper.pdf",
        "solution_url": "https://drive.google.com/uc?export=download&id=1IyITDffc_jgSCx4U_I8nTjYDi-BO4OuW",
    },
]

# The directory where you want to save the files.
# IMPORTANT: This script uses the path you provided.
# Make sure this is the correct path on your system.
DOWNLOAD_DIR = r"D:\Desktop\ISI MSQE\New folder"

async def download_file(session, url, file_name, directory):
    """
    Asynchronously downloads a file from a URL to a specified directory.
    
    Args:
        session (aiohttp.ClientSession): The client session for making requests.
        url (str): The URL of the file to download.
        file_name (str): The name to save the file as.
        directory (str): The directory to save the file in.
    """
    # Skip if the URL is not available
    if not url:
        print(f"Skipping '{file_name}' - No URL provided.")
        return

    # Create the full path for the file
    file_path = os.path.join(directory, file_name)
    
    try:
        # Asynchronously send a request to the URL
        print(f"Starting download for {file_name}...")
        async with session.get(url) as response:
            # Check if the request was successful
            if response.status == 200:
                # Asynchronously write the content to the file
                async with aiofiles.open(file_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
                print(f"Successfully downloaded '{file_name}'")
            else:
                print(f"Failed to download '{file_name}'. Status code: {response.status}")
                
    except Exception as e:
        print(f"An error occurred while trying to download '{file_name}': {e}")

async def main():
    """
    Main asynchronous function to create the directory and download all files concurrently.
    """
    # Create the download directory if it doesn't exist
    print(f"Ensuring directory exists: {DOWNLOAD_DIR}")
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    # Create a list to hold all the download tasks
    tasks = []
    
    # Use a single session for all requests for efficiency
    async with aiohttp.ClientSession() as session:
        # Loop through all the paper data to create download tasks
        for item in papers_data:
            # Create a task for the question paper
            if item["paper_url"]:
                task_paper = download_file(session, item["paper_url"], item["paper_name"], DOWNLOAD_DIR)
                tasks.append(task_paper)
            
            # Create a task for the solution
            if item["solution_url"]:
                task_solution = download_file(session, item["solution_url"], item["solution_name"], DOWNLOAD_DIR)
                tasks.append(task_solution)
        
        # Run all the download tasks concurrently
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # To run this script, you need to install aiohttp and aiofiles:
    # pip install aiohttp aiofiles
    
    # Run the main asynchronous function
    asyncio.run(main())
