from fastapi import APIRouter


router = APIRouter(
    prefix='/user',
    tags=['Users']
)


@router.get('/')
def get_user():
    return 'asdfasdf'