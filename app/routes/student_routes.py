from fastapi import APIRouter, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from app.schemas.student_schema import StudentCreate, StudentUpdate
from app.services.student_service import StudentService


router = APIRouter(tags=["students"])


@router.post("/students")
async def create_student(student: StudentCreate):
    try:
        new_student = await StudentService.create_student(student)
        return JSONResponse(content={"id": new_student.id}, status_code=201)
    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong", "error": e}, status_code=400)


@router.get("/students")
async def get_students(
    country: str = Query(None, min_length=2, max_length=50), age: int = Query(None)
):
    try:
        student_data = await StudentService.get_all_students(country, age)
        student_dicts = [
            {k: v for k, v in student.items() if k in ["name", "age"]} for student in student_data
        ]
        return JSONResponse(content={"data": student_dicts}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong", "error": e}, status_code=400)


@router.get("/students/{student_id}")
async def get_student(
    student_id: str = Path(...,
                           description="The ID of the student to retrieve")
):
    try:
        if not student_id:
            return JSONResponse(content={"message": "Student ID is required"}, status_code=400)
        student = await StudentService.get_student_by_id(student_id)
        if not student:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )
        return JSONResponse(content={k: v for k, v in student.items() if k != "_id"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong", "error": e}, status_code=400)


@router.patch("/students/{student_id}")
async def update_student(
    student_id: str = Path(..., description="The ID of the student to update"),
    student_data: StudentUpdate = None,
):
    try:
        if not student_id:
            return JSONResponse(content={"message": "Student ID is required"}, status_code=400)
        updated_student = await StudentService.update_student(student_id, student_data)
        if not updated_student:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Student not found or no update data provided",
            )
        return JSONResponse(content={}, status_code=204)
    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong", "error": e}, status_code=400)


@router.delete("/students/{student_id}")
async def delete_student(
    student_id: str = Path(..., description="The ID of the student to delete")
):
    try:
        if not student_id:
            return JSONResponse(content={"message": "Student ID is required"}, status_code=400)
        deleted = await StudentService.delete_student(student_id)
        if not deleted:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Student not found"
            )
        return JSONResponse(content={}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"message": "Something went wrong", "error": e}, status_code=400)
