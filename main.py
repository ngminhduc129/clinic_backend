from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pyodbc

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CẤU HÌNH ĐÃ SỬA ---
DB_CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=clinic_db.mssql.somee.com;" 
    "Database=clinic_db;"
    "UID=nmd129_SQLLogin_3;" # Đã sửa thành số 3 theo ảnh của bạn
    "PWD=Minhduc129;" 
    "TrustServerCertificate=yes;"
    "Encrypt=yes;"                # Nên có để bảo mật kết nối
)

def get_db_connection():
    try:
        return pyodbc.connect(DB_CONNECTION_STRING)
    except Exception as e:
        # Dòng này sẽ giúp VS Code hiện lỗi đỏ lòm để bạn biết lý do
        print(f"❌ LỖI KẾT NỐI DATABASE: {e}")
        raise e

class PatientCreate(BaseModel):
    name: str
    gender: str
    phone: str
    address: str

@app.get("/patients")
def get_patients():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, patient_code, name, gender, phone, address FROM patients")
        columns = [column[0] for column in cursor.description]
        patients = [dict(zip(columns, row)) for row in cursor.fetchall()]
        conn.close()
        return patients
    except Exception as e:
        print(f"❌ LỖI LẤY DANH SÁCH: {e}")
        return {"error": str(e)}

@app.post("/patients")
def add_patient(patient: PatientCreate):
    try:
        print(f"--- ĐANG LƯU VÀO SOMEE: {patient.name} ---")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO patients (name, gender, phone, address) VALUES (?, ?, ?, ?)",
            patient.name, patient.gender, patient.phone, patient.address
        )
        conn.commit()
        conn.close()
        return {"message": "Thêm bệnh nhân thành công!"}
    except Exception as e:
        print(f"❌ LỖI THÊM BỆNH NHÂN: {e}")

        return {"error": str(e)}
