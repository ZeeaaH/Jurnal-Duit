import os
import json
from google import genai
from google.genai import types

SYSTEM_PROMPT = """
Kamu adalah asisten pencatat keuangan. Ekstrak pesan transaksi pengguna menjadi JSON murni.
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
        model="gemini-3.6-flash",
        contents=f"{SYSTEM_PROMPT}\nPesan: {teks_pesan}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    
    return json.loads(response.text)
