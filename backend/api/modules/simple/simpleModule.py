from common.ModuleBase import ModuleBase

class SimpleModule(ModuleBase):

    def __init__(self, module_name, nice_name, app, description):
        super().__init__(module_name, nice_name, app, description)

    def _overfitting(self, data_set): # return (bool, model)
        pass

    def _import_model(self, file_path):
        pass

    def _save_model(self, model, file_path):
        pass

    def _import_data_set(self, file_path): # return (bool, data_set)
        pass