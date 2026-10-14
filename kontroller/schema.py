import pandas as pd
import pandera.pandas as pa
import sys

filnamn = sys.argv[1] if len(sys.argv) > 1 else "data/kundbas.csv"

df = pd.read_csv(filnamn)

schema = pa.DataFrameSchema({
    "kund_id": pa.Column(int, nullable=False, unique=True),
    "alder": pa.Column(int, pa.Check.between(18, 110)),
    "region": pa.Column(str, pa.Check.isin(["Mitt", "Norr", "Syd", "Väst", "Stockholm"])),
    "abonnemang": pa.Column(str, pa.Check.isin(["Bas", "Standard", "Premium"])),
    "manadskostnad": pa.Column(float, pa.Check.ge(0)),
    "data_gb_per_manad": pa.Column(float, pa.Check.ge(0)),
    "supportarenden_12m": pa.Column(int, pa.Check.ge(0)),
    "avslutat": pa.Column(int, pa.Check.isin([0, 1])),
    "manader_som_kund": pa.Column(int, pa.Check.ge(0))
})

try:
    schema.validate(df, lazy=True)
    print("Data kontroll godkänd, inga fel")

except pa.errors.SchemaErrors as e:
    print(f"Datakontroll failade:\n{e.failure_cases}")
    raise

