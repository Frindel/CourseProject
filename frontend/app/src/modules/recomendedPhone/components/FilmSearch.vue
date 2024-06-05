<template>
    <div>
        <div class="container">
        <h1>Найдите свой идеальный смартфон</h1>
        <div id="survey-form">
            <div class="question">
                <p>1. Выберите операционную систему.</p>
                <input type="radio" id="osIos" name="os" value="1" v-model="os">
                <label for="osIos">iOS</label><br>
                <input checked type="radio" id="osAndroid" name="os" value="0" v-model="os">
                <label for="osAndroid">Android</label><br>
            </div>

            <div class="question">
                <label for="priceRange">2. Введите диапозон цены или максимальную сумму.</label><br>
                <input v-model="price" type="text" id="priceRange" placeholder="Введите цену">
            </div>

            <div class="question">
                <label for="batteryCapacity">3. Какой объём аккумулятора?</label><br>
                <input v-model="batteryCapacity" type="text" id="batteryCapacity" name="batteryCapacity" placeholder="Введите диапазон мощности батареии мАч">
            </div>

            <div class="question">
                <label for="operativeMemory">4. Какой объём оперативной памяти?</label><br>
                <input v-model="operativeMemory" type="text" id="operativeMemory" name="operativeMemory" placeholder="Введите значение/я желаемой оперативной памяти">
            </div>

            <div class="question">
                <label for="internalMemory">5. Какой объём встренной памяти?</label><br>
                <input v-model="internalMemory" type="text" id="internalMemory" name="internalMemory" placeholder="Введите желаемый объём встроенной памяти">
            </div>

            <button v-on:click="searchFilms">Отправить</button>
        </div>

        <h2>Результаты поиска</h2>
        <ul id="results-list">
            <!-- Пример результата -->
            <li class="result-item" v-for="phone in results">
                <h3>{{ phone.Model }}</h3>
                <p>Price: {{ phone.Price }} руб.</p>
            </li>
            
        </ul>
    </div>
    </div>
</template>
<script>
import { useRecomendedPhoneStore } from '../storage'

export default {
    data(){
        return {
            moduleStorage: useRecomendedPhoneStore(),
            results: [],
            
            os: undefined,
            price: undefined,
            batteryCapacity: undefined,
            operativeMemory: undefined,
            internalMemory: undefined,
        }
    },
    
    methods: {
        async searchFilms()
        {
            let phones = await this.moduleStorage.phones({
                os: this.os,
                price: this.price,
                batteryCapacity: this.batteryCapacity,
                operativeMemory: this.operativeMemory,
                internalMemory: this.internalMemory,
            });

            this.results = phones;

            this.price = undefined;
            this.batteryCapacity = undefined;
            this.operativeMemory = undefined;
            this.internalMemory = undefined;
        }
    }
}
</script>
<style scoped>
    .container {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    background-color: #fff;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    color: #333;
}

.question {
    margin-bottom: 20px;
}

.question p, .question label {
    font-weight: bold;
    color: #555;
}

label {
    margin-left: 10px;
    color: #333;
}

input[type="text"] {
    width: 100%;
    padding: 10px;
    margin-top: 5px;
    margin-bottom: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
}

button {
    display: block;
    width: 100%;
    padding: 10px;
    background-color: #7613b0;
    color: white;
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
}

button:hover {
    background-color: #10a3d8;
}

h2 {
    margin-top: 50px;
    text-align: center;
    color: #333;
}

#results-list {
    list-style-type: none;
    padding: 0;
}

.result-item {
    padding: 15px;
    border: 1px solid #ddd;
    margin-bottom: 10px;
    border-radius: 5px;
    background-color: #f9f9f9;
}

.result-item h3 {
    margin: 0;
    color: #333;
}

.result-item p {
    margin: 5px 0;
    color: #666;
}

</style>