import os
from crewai import Agent, Crew, Process, Task
from crewai.tools import tool
from dotenv import load_dotenv

# Memuat variabel dari file .env (mengambil GEMINI_API_KEY)
load_dotenv()

# Mengatur environment variable agar CrewAI menggunakan model Gemini secara global
# CrewAI mendeteksi litel/litellm, kita set model Gemini-nya di sini:
os.environ["OPENAI_API_BASE"] = (
    "https://generativelanguage.googleapis.com/v1beta/openai/"
)
os.environ["OPENAI_API_KEY"] = os.getenv(
    "GEMINI_API_KEY"
)  # Memanfaatkan key Gemini
os.environ["OPENAI_MODEL_NAME"] = "gemini-3.8-flash"


# Definisi Custom Tool untuk kalkulasi profit
@tool("Kalkulator Profit")
def calculate_profit(revenue: float, cost: float) -> float:
  """Menghitung total profit bersih dari pendapatan dan modal."""
  return revenue - cost


# Inisialisasi Agent
analyst_agent = Agent(
    role="Financial Data Analyst",
    goal="Menganalisis data penjualan produk dan menghitung profit secara presisi.",
    backstory=(
        "Anda adalah analis data senior yang sangat teliti dalam menghitung"
        " margin keuntungan."
    ),
    tools=[calculate_profit],
    verbose=True,
    memory=False,
)

# Definisi Task
analysis_task = Task(
    description=(
        "Analisis data penjualan produk berikut: Pendapatan = 15000000,"
        " Modal = 9000000. Gunakan tool kalkulator untuk mencari profit"
        " bersih, lalu buat laporan ringkas."
    ),
    expected_output=(
        "Laporan ringkas berisi total pendapatan, modal, profit bersih, dan"
        " kesimpulan performa."
    ),
    agent=analyst_agent,
)

# Membentuk Crew dan Menjalankan Eksekusi
crew = Crew(
    agents=[analyst_agent],
    tasks=[analysis_task],
    process=Process.sequential,
)

if __name__ == "__main__":
  print("--- Menjalankan CrewAI dengan Gemini ---")
  result = crew.kickoff()
  print("\n--- Hasil CrewAI ---")
  print(result)