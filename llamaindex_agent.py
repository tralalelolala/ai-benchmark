import asyncio
import os
from dotenv import load_dotenv
from llama_index.core.agent import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.google_genai import GoogleGenAI

# Memuat variabel dari file .env
load_dotenv()


# Definisi Custom Tool
def calculate_profit(revenue: float, cost: float) -> float:
  """Menghitung total profit bersih dari pendapatan dan modal."""
  return float(revenue - cost)


profit_tool = FunctionTool.from_defaults(fn=calculate_profit)

# Inisialisasi LLM menggunakan Gemini
llm = GoogleGenAI(model="models/gemini-3.8-flash")

# Inisialisasi Agent
agent = FunctionAgent(
    tools=[profit_tool],
    llm=llm,
    system_prompt=(
        "Anda adalah analis data yang bertugas menghitung profit dan membuat"
        " laporan ringkas."
    ),
    verbose=True,
)


async def main():
  print("--- Menjalankan LlamaIndex dengan Gemini ---")
  # Menggunakan await karena berbasis async workflow
  response = await agent.run(
      "Analisis data penjualan produk berikut: Pendapatan = 15000000, Modal ="
      " 9000000. Hitung profit bersihnya dan susun laporan ringkas."
  )
  print("\n--- Hasil LlamaIndex ---")
  print(response)


if __name__ == "__main__":
  asyncio.run(main())