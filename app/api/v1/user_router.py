from fastapi import APIRouter, UploadFile, File, Depends
from app.use_cases.user.user_use_case import UserUseCase
from app.domain.user import NewUser, User
from app.di.container import container
from app.core.settings import settings

# 設定路由前綴為 /api/v1
router = APIRouter(prefix="/api/v1", tags=["users"])

def get_user_use_case() -> UserUseCase:
    """依賴項函數，提供 UserUseCase 實例"""
    return container.user_use_case()

@router.post("/create_user")
def create_user(user: NewUser, use_case: UserUseCase = Depends(get_user_use_case)):
    return use_case.create_user(user)

@router.delete("/delete_user")
def delete_user(user: User, use_case: UserUseCase = Depends(get_user_use_case)):
    return use_case.delete_user(user)

@router.get("/get_added_user")
def get_added_user(use_case: UserUseCase = Depends(get_user_use_case)):
    added_user_list = use_case.get_added_user()
    res = [d.model_dump() for d in added_user_list]
    return res

@router.get("/get_all_users")
def get_all_users(use_case: UserUseCase = Depends(get_user_use_case)):
    all_users = use_case.get_all_users()
    res = [{'is_new': isinstance(d, NewUser), **d.model_dump()} for d in all_users]
    return res

@router.post("/add_multiple_users_from_csv")
def add_multiple_users_from_csv(
    file: UploadFile = File(...),
    use_case: UserUseCase = Depends(get_user_use_case)
):
    temp_file_path = f"{settings.csv_upload_path}/{file.filename}"
    with open(temp_file_path, "wb") as f:
        f.write(file.file.read())
    users = use_case.load_users_from_csv(temp_file_path)
    print(f"users: {users}")
    return use_case.add_multiple_users(users)

@router.get("/calc_average_age_of_user_grouped_by_first_char_of_name")
def calc_average_age_of_user_grouped_by_first_char_of_name(
    use_case: UserUseCase = Depends(get_user_use_case)
):
    return use_case.calc_average_age_grouped_by_first_char_of_name()
