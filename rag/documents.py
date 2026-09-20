from typing import Any
import pandas as pd

def build_who_documents(df: pd.DataFrame) -> list[dict[str,Any]]:
    documents = []
    for _, row in df.iterrows():
        content = f"""
Parameter: {row["Parameter"]}

Category: {row["Category"]}

Dataset Module:
{row["Dataset_Module"]}

Chemical Symbol or Formula:
{row["Chemical_Symbol_or_Formula"]}

Unit: {row["Unit"]}

WHO Guideline Value:
{row["WHO_Guideline_Value"]}

Guideline Type:
{row["Guideline_Type"]}

Health Implications and Significance:
{row["Health_Implications_and_Significance"]}

Major Sources:
{row["Major_Sources"]}

WHO Remarks and Notes:
{row["WHO_Remarks_and_Notes"]}
""".strip()

        metadata = {
            "jurisdiction": "WHO",
            "parameter": str(row["Parameter"]),
            "category": str(row["Category"]),
            "dataset_module": str(row["Dataset_Module"]),
            "unit": str(row["Unit"]),
            "source": "WHO Drinking Water Quality Standards",
        }

        documents.append(
            {
                "content": content,
                "metadata": metadata,
            }
        )
    return documents

def build_nsdwq_documents(df: pd.DataFrame) -> list[dict[str,Any]]:
    documents = []
    for _, row in df.iterrows():
        content = f"""
Parameter: {row["Parameter"]}

Sample Feature:
{row["Sample_Feature"]}

Units:
{row["Unit"]}

Pakistan NSDWQ Limit:
{row["Pakistan_NSDWQ_Limit"]}

Notes:
{row["Notes"]}
""".strip()

        metadata = {
            "jurisdiction": "NSDWQ",
            "parameter": str(row["Parameter"]),
            "unit": str(row["Unit"]),
            "source": "Pakistan NSDWQ Standards",
        }

        documents.append(
            {
                "content": content,
                "metadata": metadata,
            }
        )
    return documents

if __name__ == "__main__":
    from ingestion import load_nsdwq_data, load_who_data

    who_df = load_who_data()
    nsdwq_df = load_nsdwq_data()
    who_documents = build_who_documents(who_df)
    nsdwq_documents = build_nsdwq_documents(nsdwq_df)

    print (f"WHO documents: {len(who_documents)}")
    print (f"NSDWQ documents: {len(nsdwq_documents)}")
    print()

    print("Example WHO Documents:")
    print (who_documents[0]["content"])
    print()
    print("Metadata:")
    print(who_documents[0]["metadata"])


