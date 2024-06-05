from common.ModuleBase import ModuleBase
import joblib
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

class RecomendedPhone(ModuleBase):

    def __init__(self, module_name, nice_name, app, description):
        super().__init__(module_name, nice_name, app, description)

    def _overfitting(self, data_set):  # return (bool, model)
        return (True, {})
        if self._check_dataset(data_set):
            data_set = self._preprocess_data(data_set)
            X = data_set[['price_class', 'battery_class', 'operative_memory_class', 'memory_class', 'screen_gerz_class']]
            y = data_set['os_class']

            # Разделение данных на обучающие и тестовые наборы
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Масштабирование данных
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)

            # Обучение модели дерева решений
            self.model = DecisionTreeClassifier(max_depth=5, random_state=42)
            self.model.fit(X_train, y_train)

            return (True, self.model)
        else:
            print("Ошибка: Модель не обучилась.")
            return (False, None)

    def _import_model(self, file_path):
        self.model = None
        self.model = joblib.load(file_path)
        if self.model is not None:
            print("Модель успешно импортирована.")
            return (True, self.model)
        else:
            print("Ошибка: Модель не была импортирована.")
            return (False, self.model)

    def _save_model(self, model, directory_path):
        pass

    def _import_data_set(self, file_path): # return (bool, data_set)
        data_set = None
        data_set = pd.read_csv(file_path)
        if data_set is not None:
            print("Датасет успешно импортирован.")
            return (True, data_set)
        else:
            print("Ошибка: Датасет не был импортирован.")
            return (False, data_set)