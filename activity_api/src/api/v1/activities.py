"""Эндпоинты обработки событий."""
from fastapi import APIRouter, Depends, Request, status

from src.api.v1.schemes.spawn_point import SpawnPointScheme
from src.api.v1.schemes.transform_schemes import \
    transform_point_scheme_to_model
from src.auth.request import subscription_required
from src.services.activity.activity_service import ActivityService

router = APIRouter()


@router.post('/spawn-point',
             dependencies=[Depends(subscription_required)],
             status_code=status.HTTP_201_CREATED,
             )
async def send_activity(spawn_point: SpawnPointScheme,
                        request: Request,
                        activity_service: ActivityService = Depends(),
                        ) -> dict:
    """Отправить spawn-point в хранилище."""
    spawn_point_model = transform_point_scheme_to_model(scheme=spawn_point)
    spawn_point_model.user_id = request.state.user_id
    await activity_service.send_spawn_point(point=spawn_point_model)
    return {'message': 'ok'}
