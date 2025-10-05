import pandas as pd

def remove_duplicate_urls(csv_file):
    try:
        # Read the csv file
        df = pd.read_csv(csv_file, encoding='ISO-8859-1')

        # Check if 'url' and 'label' columns exist
        if 'url' in df.columns and 'label' in df.columns:
            # Find duplicate rows based on 'url' column
            duplicate_urls = df[df.duplicated(subset='url', keep=False)]

            # Print duplicate URLs with their labels
            if not duplicate_urls.empty:
                print("Duplicate URLs:")
                for index, row in duplicate_urls.iterrows():
                    print(f"URL: {row['url']}, Label: {row['label']}")

            # Remove duplicate rows based on 'url' column
            df = df.drop_duplicates(subset='url', keep='first')

            # Save the updated dataframe to the same csv file
            df.to_csv(csv_file, index=False)
            print("Duplicate URLs removed and saved to " + csv_file)
        else:
            print("The csv file does not have 'url' and 'label' columns.")
    except FileNotFoundError:
        print("The csv file does not exist.")
    except pd.errors.EmptyDataError:
        print("The csv file is empty.")
    except pd.errors.ParserError:
        print("Error parsing the csv file.")

# Call the function with the csv file name
remove_duplicate_urls('D:\\offline_dataset\\mix\\p.csv')