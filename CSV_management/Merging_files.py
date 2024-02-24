import glob
import pandas as pd

def merging_files():

    need_merge = False

    if need_merge:
        folder_path = 'TXT'
        file_pattern = f'{folder_path}/*.csv'
        file_list = glob.glob(file_pattern)
        print('Files list: ', file_list)

        # Creating dataframe from multiple CVS-s in order to add last column Filename
        data_frames = [pd.read_csv(file).assign(Filename=file) for file in file_list]
        print('Dataframes from each csv: ', data_frames)

        for file, dataframe in zip(file_list, data_frames):       # Writing dataframe to each CSV
            dataframe_from_csv.to_csv(file, index=False)

        merged_df = pd.concat(data_frames, ignore_index=True)
        print('Merged dataframes: ', merged_df.head())

        merged_df.to_csv(f'TXT/merged_data.csv', index=False)  # Writing merged CSV


merging_files()