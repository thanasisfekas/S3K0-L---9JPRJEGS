import pandas as pd
import os

class Shift:
    def __init__(self, id, name, surname, date, time_begin, time_end):
        self.new_shift= {
            "id": [id],
            "first_name": [name],
            "last_name": [surname],
            "date": [date],
            "start": [time_begin],
            "end": [time_end]}

        self.save_shift()


    def save_shift(self):
        new_df = pd.DataFrame(self.new_shift)

        if os.path.exists("scheduledShifts.csv"):
            try:
                existing_df = pd.read_csv("scheduledShifts.csv")
                updated_df = pd.concat([existing_df, new_df], ignore_index=True)
                updated_df.to_csv("scheduledShifts.csv", index=False)
                print(f"Shift appended successfully file.")
            except Exception as e:
                print(f"Error updating CSV file: {e}")
        else:
            try:
                new_df.to_csv("scheduledShifts.csv", index=False)
                print(f"File created and shift saved successfully.")
            except Exception as e:
                print(f"Error creating CSV file: {e}")
