from fastapi import FastAPI


from reps.database_reps.database_services import create_db


import routers.month as month_router
import routers.user as user_router
import routers.day as day_router
import routers.appointment as appointment_router
import routers.reservation as reservation_router
import routers.service as service_router
import routers.pages as pages_router


create_db()


app = FastAPI()

app.include_router(user_router.router)
app.include_router(service_router.router)
app.include_router(month_router.router)
app.include_router(day_router.router)
app.include_router(appointment_router.router)
app.include_router(reservation_router.router)
app.include_router(pages_router.router)

