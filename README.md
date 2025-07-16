# 🛠️ DFM Warning Processor

This project reads part data from a `.parquet` file, checks for previously processed entries using UUIDs, evaluates each part for manufacturing warnings and errors based on hole geometry, and writes both results and UUID logs to disk.

---

## 📌 What It Does

- Reads input data from a `.parquet` file where each row represents a manufactured part.
- Uses a `uuid_history.txt` log file to **skip previously processed parts**.
- Processes each part to check for:
  - `has_unreachable_hole_warning`: when hole length exceeds `radius * 2 * 10`
  - `has_unreachable_hole_error`: when hole length exceeds `radius * 2 * 40`
- Appends newly processed UUIDs to the log file.
- Writes the enriched results to a new output `.parquet` file.

---

## 📂 File Structure

.
├── input_data/

│ ├── 2023 DE_case_dataset.gz.parquet

├── log/

│ ├── uuid_history.txt

├── output/
│ └── processed_parts.parquet

├── main.py # Main script

└── README.md
