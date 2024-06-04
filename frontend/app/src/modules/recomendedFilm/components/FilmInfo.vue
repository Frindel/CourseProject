<template>
    <div class="film">
        <div class="film__name">{{ film.title }}</div>
        <div class="film__statistics">
            <div class="statistics">
                <div class="statistic__header">Год выпуска</div>
                <div class="statistic__value">{{ film.release_date }}</div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    props: ['film']
}
</script>
<style>
.film__name{
    font-size: 18px;
    font-weight: 600;
    font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    
}

.statistic__header{
    font-size: 18px;
    font-weight: 400;
    font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    margin-right: 5px;
}
.film__statistics{
    display: flex;
    flex-direction: column;
}
.statistics{
    display: flex;
    justify-content: left;

}

.statistic__value{
    font-size: 18px;
    font-weight: 100;
    font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
}
</style>