import csv
import os

from fastapi import HTTPException, status, UploadFile

from services.api_client import APIClient


class FileProcessor:

    def __init__(self):
        self.file_path = 'data/folha_de_ponto.csv'
        self.directory = 'data'
        self.api_client = APIClient()

    async def list_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    row_dict = dict(funcionario_id=row[0], data=row[1], hora_entrada=row[2], hora_saida=row[3])
                    self.api_client.send_data(row_dict)
            return {"detail": "Arquivo de ponto processado com sucesso!"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo de ponto inexistente!")

    def create_file(self):
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['funcionario_id', 'data', 'hora_entrada', 'hora_saida'])
                return {"mensagem": f"Arquivo {self.file_path} criado com sucesso."}
        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Arquivo de ponto já existe")

    async def add_data_to_file(self, data: dict):
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([data["funcionario_id"], data["data"], data["hora_entrada"], data["hora_saida"]])
                return {"mensagem": f"Registro de ponto inserido com sucesso: {data}"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo de ponto inexistente, por favor acessar"
                                       " a rota de criar o arquivo.")

    async def delete_data(self, selected_line: int):
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r') as file:
                lines = file.readlines()

            if selected_line < 1 or selected_line >= len(lines):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Linha selecionada inválida.")

            with open(self.file_path, mode='w') as file:
                for index, line in enumerate(lines):
                    if index != selected_line:
                        file.write(line)
            return {"mensagem": "Registro de ponto selecionado deletado."}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Arquivo de ponto inexistente.")

    async def upload_file(self, file: UploadFile):
        if file.filename.endswith('.csv'):
            try:
                contents = await file.read()
                decoded_file = contents.decode("utf-8").splitlines()

                csv_reader = csv.DictReader(decoded_file)
                for row in csv_reader:
                    self.api_client.send_data(row)
                return {"mensagem": f"Arquivo {file.filename} de ponto processado com sucesso"}
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail=f"Falha ao processar o arquivo CSV de ponto: {str(e)}")

        else:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Apenas arquivo CSV")
