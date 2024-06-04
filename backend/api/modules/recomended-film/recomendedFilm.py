from common.ModuleBase import ModuleBase
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

class RecomendedFilm(ModuleBase):

    def __init__(self, module_name, nice_name, app, description):
        super().__init__(module_name, nice_name, app, description)

    def _overfitting(self, data_set):
        self.model = TfidfVectorizer(stop_words='english')
        data_set['overview_clean'] = data_set['overview_clean'].fillna('')
        self.model.fit_transform(data_set['overview_clean'])
        if len(self.model.vocabulary_) > 0:
            print("Модель успешно обучилась.")
            return (True, self.model)
        else:
            print("Ошибка: Модель не обучилась. Пустой словарь.")
            return (False, self.model)

    def _import_model(self, directory_path):
        try:
            self.model = joblib.load(f'{directory_path}/model.joblib')
            if self.model is not None:
                print("Модель успешно импортирована.")
                return (True, self.model)
            else:
                print("Ошибка: Модель не была импортирована.")
                return (False, self.model)
        except Exception as e:
            print(f"Произошла ошибка при импорте модели: {e}")
            return (False, None)
        

    def _save_model(self, model, directory_path):
        joblib.dump(model, f'{directory_path}/model.joblib')

    def _import_data_set(self, file_path): # return (bool, data_set)
        data_set = None
        data_set = pd.read_csv(file_path)
        if data_set is not None:
            print("Датасет успешно импортирован.")
            return (True, data_set)
        else:
            print("Ошибка: Датасет не был импортирован.")
            return (False, data_set)