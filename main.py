import json
import pandas as pd


data = r'input_data/2023 DE_case_dataset.gz.parquet'
# input_data reduction
columns = ['uuid', 'holes']
# ingest input_data
# timestamp reads and skip them
# loop rows
# display output
# filter to show only relevant orders

def ingest_data(data):
    df = pd.read_parquet(data, columns=columns)
    count_rows_processed = 0
    count_has_unreachable_hole_warning = 0
    count_has_unreachable_hole_error = 0

    # QA: check if uniq
    # print(df['uuid'].is_unique)
    for index, item in df.iterrows():
        has_unreachable_hole_warning = False
        has_unreachable_hole_error = False
        if item.holes is not pd.NA:
            # print('Row has holes')
            clean_str=item.holes.replace('true', 'true').replace('false', 'false')
            hole_list = json.loads(clean_str)
            # QA: Beautify jsons
            # https: // codebeautify.org / string - to - json - online
            for hole in hole_list:
                hole_len = hole['length']
                hole_rad = hole['radius']
                if hole_len > hole_rad * 2 * 10:
                    has_unreachable_hole_warning = True

                if hole_len > hole_rad * 2 * 40:
                    has_unreachable_hole_error = True

            if has_unreachable_hole_warning:
                count_has_unreachable_hole_warning += 1
            if has_unreachable_hole_error:
                count_has_unreachable_hole_error += 1

            df['has_unreachable_hole_warning'] = has_unreachable_hole_warning
            df['has_unreachable_hole_error'] = has_unreachable_hole_error

        else:
            df['has_unreachable_hole_warning'] = False
            df['has_unreachable_hole_error'] = False

        count_rows_processed+=1

    return df, count_rows_processed, count_has_unreachable_hole_warning, count_has_unreachable_hole_error

if __name__ == '__main__':
    enriched_df, count_rows_processed, count_has_unreachable_hole_warning, count_has_unreachable_hole_error = ingest_data(data)
    data_df = pd.read_parquet(data)
    df_merge = pd.merge(data_df, enriched_df, on='uuid')
    print('Rows processed: '+str(count_rows_processed)+', Warnings: '+str(count_has_unreachable_hole_warning)+' Errors: '+str(count_has_unreachable_hole_error))
    df_merge.to_parquet(r'output/processed_parts.parquet', index=False)
