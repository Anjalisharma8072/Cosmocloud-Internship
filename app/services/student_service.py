from app.models.student import Student
from app.schemas.student_schema import StudentCreate, StudentUpdate
from app.database import Database
from bson import ObjectId
from typing import List, Optional


class StudentService:
    @staticmethod
    async def create_student(student: StudentCreate) -> Student:
        db = Database.db
        student_dict = student.model_dump()
        result = await db.students.insert_one(student_dict)
        student_dict['_id'] = str(result.inserted_id)
        return Student(**student_dict)

    @staticmethod
    async def get_all_students(
        skip: int = 0,
        limit: int = 10
    ) -> List[Student]:
        db = Database.db
        cursor = db.students.find().skip(skip).limit(limit)
        students = await cursor.to_list(length=limit)
        return [Student(**{**student, '_id': str(student['_id'])}) for student in students]

    @staticmethod
    async def get_student_by_id(student_id: str) -> Optional[Student]:
        db = Database.db
        student = await db.students.find_one({"_id": ObjectId(student_id)})
        return Student(**{**student, '_id': str(student['_id'])}) if student else None

    @staticmethod
    async def update_student(student_id: str, student_data: StudentUpdate) -> Optional[Student]:
        db = Database.db
        student_dict = {
            k: v for k, v in student_data.model_dump().items() if v is not None}

        if not student_dict:
            return None

        result = await db.students.update_one(
            {"_id": ObjectId(student_id)},
            {"$set": student_dict}
        )

        if result.modified_count:
            updated_student = await db.students.find_one({"_id": ObjectId(student_id)})
            return Student(**{**updated_student, '_id': str(updated_student['_id'])})
        return None

    @staticmethod
    async def delete_student(student_id: str) -> bool:
        db = Database.db
        result = await db.students.delete_one({"_id": ObjectId(student_id)})
        return result.deleted_count > 0
