from domain.repositories.text_management_repository import TextManagementRepository

class TextManagementService:
    def __init__(self):
        self.repository = TextManagementRepository()

    def get_all_variables(self):
        return self.repository.get_all_variables()

    def get_variable_by_id(self, variable_id):
        return self.repository.get_variable_by_id(variable_id)

    def create_variable(self, variable_data):
        return self.repository.create_variable(variable_data)

    def update_variable(self, variable_id, variable_data):
        return self.repository.update_variable(variable_id, variable_data)

    def delete_variable(self, variable_id):
        return self.repository.delete_variable(variable_id)