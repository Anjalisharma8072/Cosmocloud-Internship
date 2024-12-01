from fastapi import APIRouter, HTTPException, Path, Query, status
from typing import List, Optional
from app.models.student import Student
from app.schemas.student_schema import StudentCreate, StudentUpdate
from app.services.student_service import StudentService


router  = APIRouter(prefix="/students" , tags=["students"])


@router.post("/",response_model=Student,status_code=status.HTTP_201_CREATED)
async def create_student(student:StudentCreate):
    return await StudentService.create_student(student)

@router.get("/",response_model=List[Student])
async def get_students(
    skip: int  = Query(0,ge = 0),
    limit: int = Query(10,ge=1 , le = 100)
):
    return await StudentService.get_all_students(skip,limit)

@router.get("/{student_id}" , response_model=Student)
async def get_student(
    student_id: str = Path(...,
                           description="The ID of the student to retrieve")
):
    student = await StudentService.get_student_by_id(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Student not found"
        )
    return student


@router.patch("/{student_id}", response_model=Student)
async def update_student(
    student_id: str = Path(..., description="The ID of the student to update"),
    student_data: StudentUpdate = None
):
    updated_student = await StudentService.update_student(student_id, student_data)
    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found or no update data provided"
        )
    return updated_student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str = Path(..., description="The ID of the student to delete")
):
    deleted = await StudentService.delete_student(student_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
