# WP1: Data Ingestion and Structural Review
# Skript 1: Laden des CT-RATE Datensatzes mit der Hugging Face Bibliothek

# Zuerst installieren wir die notwendige Bibliothek.
# Das muss nur einmal pro Conda-Umgebung gemacht werden.
# Wir können es direkt im Skript tun, aber es ist besser, es einmalig im Terminal zu machen.
# Führe also im Terminal aus: pip install datasets

from datasets import load_dataset
import pandas as pd

# Der Name des Datensatzes auf Hugging Face
DATASET_NAME = "ibrahimhamamci/CT-RATE"

print("Lade den CT-RATE Datensatz...")

# Lade die Metadaten-Konfiguration des Datensatzes
# 'metadata' ist der Name der Konfiguration, den wir in der JSON gesehen haben
metadata_dataset = load_dataset(DATASET_NAME, "metadata")

# Lade die Berichte-Konfiguration des Datensatzes
# 'reports' ist der Name der anderen Konfiguration
reports_dataset = load_dataset(DATASET_NAME, "reports")

print("Datensatz erfolgreich geladen!")

print("\n--- Metadaten-Info ---")
print(metadata_dataset)

print("\n--- Berichte-Info ---")
print(reports_dataset)

print("\n--- Ein Beispiel aus den Trainings-Berichten ---")
# Wir schauen uns das erste Element der Trainingsdaten an
print(reports_dataset['train'][0])

print("\n--- Ein Beispiel aus den Trainings-Metadaten ---")
print(metadata_dataset['train'][0])

# Optional: Konvertiere einen Teil der Daten in einen Pandas DataFrame für einfachere Handhabung
# Das ist sehr nützlich für die erste Analyse!
print("\nErstelle einen Pandas DataFrame von den Trainings-Berichten...")
df_reports = pd.DataFrame(reports_dataset['train'])
print("DataFrame erstellt. Hier sind die ersten 5 Zeilen:")
print(df_reports.head())
