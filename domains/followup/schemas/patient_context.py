from typing import TypedDict


class PatientContext(TypedDict, total=False):
    patient_name: str
    doctor_name: str
    treatment_name: str
    treatment_date: str