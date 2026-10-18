import os
import json
from google import genai

SYSTEM_PROMPT = """
Kamu adalah asisten pencatat keuangan. Ekstrak pesan transaksi pengguna menjadi JSON murni tanpa teks lain.
Format JSON wajib:
{
  "tipe": "pengeluaran" atau "pemasukan",
  "kategori": "makanan" / "transportasi" / "tagihan" / "hiburan" / "lainnya",
  "nominal": angka_saja,
  "keterangan": "deskripsi singkat"
}
"""

def ekstrak_transaksi(teks_pesan):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\nPesan: {teks_pesan}"
    )
    
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)