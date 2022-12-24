from fastapi import Header, HTTPException, status

async def get_token_header(internal_token: str = Header(...)):
    if internal_token != "allowed":
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)