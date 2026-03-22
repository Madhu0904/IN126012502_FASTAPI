from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Medical Appointment System")

# =========================
# DATABASE
# =========================
patients = []
doctors = []
appointments = []

# =========================
# MODELS
# =========================
class Patient(BaseModel):
    name: str
    age: int
    gender: str

class Doctor(BaseModel):
    name: str
    specialization: str
    available: bool = True

class Appointment(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    status: str = "booked"


# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"message": "Medical Appointment API Running"}


# =========================
# PATIENTS APIs
# =========================

@app.post("/patients")
def add_patient(p: Patient):
    patient = p.dict()
    patient["id"] = len(patients) + 1
    patients.append(patient)
    return patient

@app.get("/patients")
def get_patients():
    return patients

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    for p in patients:
        if p["id"] == patient_id:
            return p
    raise HTTPException(404, "Patient not found")

@app.put("/patients/{patient_id}")
def update_patient(patient_id: int, data: Patient):
    for p in patients:
        if p["id"] == patient_id:
            p.update(data.dict())
            return p
    raise HTTPException(404, "Patient not found")

@app.delete("/patients/{patient_id}")
def delete_patient(patient_id: int):
    for p in patients:
        if p["id"] == patient_id:
            patients.remove(p)
            return {"message": "Patient deleted"}
    raise HTTPException(404, "Patient not found")


# =========================
# DOCTORS APIs
# =========================

@app.post("/doctors")
def add_doctor(d: Doctor):
    doctor = d.dict()
    doctor["id"] = len(doctors) + 1
    doctors.append(doctor)
    return doctor

@app.get("/doctors")
def get_doctors():
    return doctors

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    raise HTTPException(404, "Doctor not found")

@app.get("/doctors/available")
def get_available_doctors():
    return [d for d in doctors if d["available"]]

@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            return d
    raise HTTPException(status_code=404, detail="Doctor not found")

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    for d in doctors:
        if d["id"] == doctor_id:
            doctors.remove(d)
            return {"message": "Doctor deleted"}
    raise HTTPException(404, "Doctor not found")


# =========================
# APPOINTMENTS APIs
# =========================

@app.post("/appointments")
def book_appointment(a: Appointment):

    # check patient
    if not any(p["id"] == a.patient_id for p in patients):
        raise HTTPException(404, "Patient not found")

    # check doctor
    doctor = next((d for d in doctors if d["id"] == a.doctor_id), None)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if not doctor["available"]:
        raise HTTPException(400, "Doctor not available")

    appointment = a.dict()
    appointment["id"] = len(appointments) + 1

    appointments.append(appointment)
    return appointment


@app.get("/appointments")
def get_appointments():
    return appointments


@app.get("/appointments/{appointment_id}")
def get_appointment(appointment_id: int):
    for a in appointments:
        if a["id"] == appointment_id:
            return a
    raise HTTPException(404, "Appointment not found")


@app.get("/appointments/search")
def search_appointments(
    patient_id: int = Query(None),
    doctor_id: int = Query(None)
):
    result = appointments

    if patient_id:
        result = [a for a in result if a["patient_id"] == patient_id]

    if doctor_id:
        result = [a for a in result if a["doctor_id"] == doctor_id]

    return result


@app.patch("/appointments/{appointment_id}")
def update_status(appointment_id: int, status: str):
    for a in appointments:
        if a["id"] == appointment_id:
            a["status"] = status
            return a
    raise HTTPException(404, "Appointment not found")


@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int):
    for a in appointments:
        if a["id"] == appointment_id:
            appointments.remove(a)
            return {"message": "Appointment cancelled"}
    raise HTTPException(404, "Appointment not found")



# Pagination
@app.get("/appointments/page")
def paginate_appointments(
    page: int = Query(1, ge=1),
    limit: int = Query(2, ge=1)
):
    start = (page - 1) * limit
    end = start + limit

    total = len(appointments)

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": -(-total // limit),
        "data": appointments[start:end]
    }


# Filter by status
@app.get("/appointments/status")
def filter_by_status(status: str):
    return [a for a in appointments if a["status"] == status]


# Get appointments for doctor
@app.get("/doctors/{doctor_id}/appointments")
def doctor_appointments(doctor_id: int):
    return [a for a in appointments if a["doctor_id"] == doctor_id]


# Get appointments for patient
@app.get("/patients/{patient_id}/appointments")
def patient_appointments(patient_id: int):
    return [a for a in appointments if a["patient_id"] == patient_id]