import pandas as pd

def csv_to_markdown_sample(csv_file_path, sample_size=5):
    df = pd.read_csv(csv_file_path)
    return df.head(sample_size).to_markdown()