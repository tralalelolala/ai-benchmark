import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

# Memuat variabel dari file .env
load_dotenv()


# Definisi Custom Tool
@tool
def calculate_profit(revenue: float, cost: float) -> float:
  """Menghitung total profit bersih dari pendapatan dan modal."""
  return revenue - cost


tools = [calculate_profit]

# Inisialisasi LLM menggunakan Gemini Flash
llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash", temperature=0)

# Mengikat tools langsung ke model (pendekatan standar baru LangChain)
llm_with_tools = llm.bind_tools(tools)

if __name__ == "__main__":
  print("--- Hasil LangChain dengan Gemini ---")

  prompt = (
      "Analisis data penjualan produk berikut: Pendapatan = 15000000, Modal ="
      " 9000000. Panggil tool kalkulator untuk menghitung profit bersihnya,"
      " lalu berikan ringkasan laporannya."
  )

  # Memanggil model
  response = llm_with_tools.invoke(prompt)

  print("\nRespon Model:")
  print(response.content)

  # Jika model memanggil fungsi (tool call)
  if response.tool_calls:
    print("\nTool yang Dipanggil:", response.tool_calls)
    # Eksekusi tool secara manual berdasarkan argumen dari model
    for tool_call in response.tool_calls:
      if tool_call["name"] == "calculate_profit":
        result = calculate_profit.invoke(tool_call["args"])
        print(f"Hasil Eksekusi Tool: {result}")