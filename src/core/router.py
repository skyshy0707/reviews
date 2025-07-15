from fastapi import APIRouter, Depends

from core import crud, schemes

class Router:

    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        pass

class ServerAPI(Router):

    def setup_routes(self):

        @self.router.post(
            "/reviews",
            response_model=schemes.Review
        )
        def create_review(review: schemes.ReviewCreate):
            return crud.create_review(review)
        
        @self.router.get(
            "/reviews",
            response_model=schemes.create_pagination_response_model(schemes.Review)
        )
        def reviews(params: schemes.SearchReviews = Depends()):
            return crud.search_reviews(params)
        
api = ServerAPI()