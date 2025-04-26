from fastapi import APIRouter, UploadFile, File
from app.use_cases.user.user_use_case import UserUseCase
from app.infrastructure.repositories.user_repository_csv import UserCSVRepository
from app.domain.user import NewUser, User
from app.core.settings import settings
from app.infrastructure.services.csv_user_parser import CsvUserParserService

router = APIRouter()

# Initialize implementations and inject UseCase
repo = UserCSVRepository()
user_data_loader = CsvUserParserService()
use_case = UserUseCase(repo, user_data_loader)

# Initialize users
init_users = use_case.init_users(settings.csv_path)
use_case.add_multiple_users(init_users)

@router.post("/create_user")
def create_user(user: NewUser):
    return use_case.create_user(user)

@router.delete("/delete_user")
def delete_user(user: User):
    return use_case.delete_user(user)

@router.get("/get_added_user")
def get_added_user():
    added_user_list = use_case.get_added_user()
    res = [d.model_dump() for d in added_user_list]
    return res

@router.get("/get_all_users")
def get_all_users():
    return use_case.get_all_users()

@router.post("/add_multiple_users_from_csv")
def add_multiple_users_from_csv(file: UploadFile = File(...)):
    temp_file_path = f"{settings.csv_upload_path}/{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(file.file.read())
    users = use_case.load_users_from_csv(temp_file_path)
    return use_case.add_multiple_users(users)

@router.get("/calc_average_age_of_user_grouped_by_first_char_of_name")
def calc_average_age_of_user_grouped_by_first_char_of_name():
    return use_case.calc_average_age_grouped_by_first_char_of_name()
