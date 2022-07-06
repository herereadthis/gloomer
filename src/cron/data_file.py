import os
import pandas as pd

import utils

class DataFile:

    def __init__(self, log_path=None, base_file_name=None, report=None, unique_key = None):
        self.log_path = log_path
        self.proposed_file_name = f'{base_file_name}_{utils.get_daystamp_name()}.csv'
        self.file_path = os.path.abspath(os.path.join(self.log_path, self.proposed_file_name))
        self.report_dataframe = pd.DataFrame([report])
        self.unique_key = unique_key
    
    def __str__(self):
        s = {
            'log_path': self.log_path,
            'proposed_file_name': self.proposed_file_name,
            'file_path': self.file_path,
            'report_dataframe': self.report_dataframe,
            'unique_key': self.unique_key
        }
        return str(s)


    def get_last_entry_cell(self) -> str:
        df = pd.read_csv(self.file_path)
        return df.loc[df.index[-1], self.unique_key]
    
    def save_data(self):
        only_files = [f for f in os.listdir(self.log_path) if os.path.isfile(os.path.join(self.log_path, f))]

        if (self.proposed_file_name in only_files):
            last_observation_key = self.get_last_entry_cell()
            current_observation_key = self.report_dataframe.loc[0, self.unique_key]
            if (last_observation_key == current_observation_key):
                print('last report already recorded!')
            else:
                print('adding new report to existing file!')
                DataFile.save_append(reports=self.report_dataframe, path=self.file_path)
        else:
            print(f'new_file_path: {self.file_path}')
            DataFile.save(reports=self.report_dataframe, path=self.file_path)

    @staticmethod
    def save(reports: pd.DataFrame, path: str) -> None:
        reports.to_csv(path, index=False)

    @staticmethod
    def save_append(reports: pd.DataFrame, path: str) -> None:
        reports.to_csv(path, index=False, mode='a', header=False)
