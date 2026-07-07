from fastapi import UploadFile, HTTPException


class Validator:

    @staticmethod
    def validate_pdf(file: UploadFile):

        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are allowed."
            )

        return True