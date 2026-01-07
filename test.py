print("Hallo Welt! Das Python-Skript funktioniert.")
print("Teste die Importe...")

try:
    import pandas as pd
    print("✅ Pandas wurde erfolgreich importiert.")
except ImportError as e:
    print(f"❌ Fehler beim Import von Pandas: {e}")

try:
    from datasets import load_dataset
    print("✅ Datasets wurde erfolgreich importiert.")
except ImportError as e:
    print(f"❌ Fehler beim Import von Datasets: {e}")

print("Test beendet.")